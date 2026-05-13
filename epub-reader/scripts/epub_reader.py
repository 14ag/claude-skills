"""
epub_reader.py

TOC-first epub navigation tool for AI agents

Commands
  toc  <epub>            output chapter map as JSON
  info <epub>            output book metadata as JSON
  read <epub> <ref>      read chapter by 1-based index id or partial title
  search <epub> <query>  list chapters with titles matching query

Optional flags for read command
  --full                 skip the 8000 char preview truncation

Exit codes
  0  success
  1  bad arguments
  2  file not found or bad zip
  3  parse failure
"""

import sys
import json
import zipfile
from xml.etree import ElementTree as ET
from html.parser import HTMLParser
from pathlib import PurePosixPath


# xml namespace URIs used in epub container and content files
NS = {
    'container': 'urn:oasis:names:tc:opendocument:xmlns:container',
    'opf':       'http://www.idpf.org/2007/opf',
    'dc':        'http://purl.org/dc/elements/1.1/',
    'ncx':       'http://www.daisy.org/z3986/2005/ncx/',
    'xhtml':     'http://www.w3.org/1999/xhtml',
    'epub':      'http://www.idpf.org/2007/ops',
}


def _ns(prefix, tag):
    # build a Clark-notation qualified name from a prefix and local tag
    return '{%s}%s' % (NS[prefix], tag)


class _TextExtractor(HTMLParser):
    # strips HTML tags and returns plain readable text
    # skips script and style element content entirely

    _BLOCK = {'p','h1','h2','h3','h4','h5','h6','li','br','div','tr','td','th'}
    _SKIP  = {'script','style','head'}

    def __init__(self):
        super().__init__()
        self._buf  = []
        # tracks nesting depth inside skipped elements
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        t = tag.lower()
        if t in self._SKIP:
            self._skip += 1
        if t in self._BLOCK:
            self._buf.append('\n')

    def handle_endtag(self, tag):
        if tag.lower() in self._SKIP:
            self._skip -= 1

    def handle_data(self, data):
        if self._skip == 0:
            self._buf.append(data)

    def result(self):
        import re
        raw = ''.join(self._buf)
        # collapse 3 or more consecutive newlines into 2
        return re.sub(r'\n{3,}', '\n\n', raw).strip()


def _html_to_text(raw_bytes):
    # decode bytes then strip HTML to plain text
    # falls back to latin-1 when utf-8 fails
    try:
        src = raw_bytes.decode('utf-8', errors='replace')
    except Exception:
        src = raw_bytes.decode('latin-1', errors='replace')
    p = _TextExtractor()
    p.feed(src)
    return p.result()


def _open_zip(path):
    # open epub as a zip archive
    # exits with code 2 on missing file or bad zip format
    try:
        return zipfile.ZipFile(path, 'r')
    except FileNotFoundError:
        sys.exit('[error] file not found: %s' % path)
    except zipfile.BadZipFile:
        sys.exit('[error] not a valid epub zip: %s' % path)


def _get_opf_path(zf):
    # read META-INF/container xml to locate the OPF manifest file path
    try:
        data = zf.read('META-INF/container.xml')
    except KeyError:
        sys.exit('[error] META-INF/container xml missing - not a valid epub')
    root = ET.fromstring(data)
    rf = root.find('.//' + _ns('container', 'rootfile'))
    if rf is None:
        sys.exit('[error] no rootfile element in container xml')
    return rf.get('full-path', '')


def _parse_opf(zf, opf_path):
    """
    Parse the OPF file.
    Returns (meta, manifest, spine, ncx_href, nav_href, opf_dir)
      meta      - dict of dc metadata values
      manifest  - dict id -> {href full_href media_type properties}
      spine     - list of manifest ids in reading order
      ncx_href  - full path to toc ncx or None
      nav_href  - full path to nav xhtml or None
      opf_dir   - directory prefix for resolving hrefs
    """
    try:
        data = zf.read(opf_path)
    except KeyError:
        sys.exit('[error] OPF file not found in epub: %s' % opf_path)

    root    = ET.fromstring(data)
    opf_dir = str(PurePosixPath(opf_path).parent)
    if opf_dir == '.':
        opf_dir = ''

    # extract dublin core metadata fields
    meta     = {}
    meta_el  = root.find(_ns('opf', 'metadata'))
    if meta_el is None:
        meta_el = root.find('metadata')
    dc_fields = ('title', 'creator', 'language', 'publisher', 'identifier', 'date')
    if meta_el is not None:
        for field in dc_fields:
            el = meta_el.find(_ns('dc', field))
            if el is not None and el.text:
                meta[field] = el.text.strip()

    # build manifest from all item elements
    manifest     = {}
    manifest_el  = root.find(_ns('opf', 'manifest'))
    if manifest_el is None:
        manifest_el = root.find('manifest')
    ncx_href     = None
    nav_href     = None

    if manifest_el is not None:
        for item in manifest_el:
            iid   = item.get('id', '')
            href  = item.get('href', '').replace('\\', '/')
            mtype = item.get('media-type', '')
            props = item.get('properties', '')
            full  = (opf_dir + '/' + href).lstrip('/') if opf_dir else href
            manifest[iid] = {
                'href':       href,
                'full_href':  full,
                'media_type': mtype,
                'properties': props,
            }
            if mtype == 'application/x-dtbncx+xml':
                # epub 2 NCX table of contents
                ncx_href = full
            if 'nav' in props.split():
                # epub 3 navigation document
                nav_href = full

    # read spine to get ordered list of content item ids
    spine    = []
    spine_el = root.find(_ns('opf', 'spine'))
    if spine_el is None:
        spine_el = root.find('spine')
    toc_attr = None
    if spine_el is not None:
        toc_attr = spine_el.get('toc')
        for itemref in spine_el:
            idref  = itemref.get('idref', '')
            linear = itemref.get('linear', 'yes')
            if linear != 'no' and idref:
                spine.append(idref)

    # spine toc attribute may point to ncx when media-type search failed
    if ncx_href is None and toc_attr and toc_attr in manifest:
        ncx_href = manifest[toc_attr]['full_href']

    return meta, manifest, spine, ncx_href, nav_href, opf_dir


def _parse_ncx(zf, ncx_href):
    # parse EPUB 2 NCX toc file into a flat list of entries
    # each entry is {id title href src level}
    try:
        data = zf.read(ncx_href)
    except KeyError:
        return []

    root    = ET.fromstring(data)
    entries = []
    ncx_dir = str(PurePosixPath(ncx_href).parent)
    if ncx_dir == '.':
        ncx_dir = ''

    def _visit(el, level):
        # recursively walk navPoint elements
        eid    = el.get('id', '')
        lbl    = el.find('.//' + _ns('ncx', 'text'))
        title  = lbl.text.strip() if lbl is not None and lbl.text else ''
        cnt    = el.find(_ns('ncx', 'content'))
        src    = cnt.get('src', '') if cnt is not None else ''
        href = src.split('#')[0] if '#' in src else src
        full   = (ncx_dir + '/' + href).lstrip('/') if ncx_dir else href
        if title:
            entries.append({'id': eid, 'title': title, 'href': full, 'src': src, 'level': level})
        for child in el.findall(_ns('ncx', 'navPoint')):
            _visit(child, level + 1)

    navmap = root.find(_ns('ncx', 'navMap'))
    if navmap is not None:
        for np in navmap.findall(_ns('ncx', 'navPoint')):
            _visit(np, 1)

    return entries


def _parse_nav(zf, nav_href):
    # parse EPUB 3 nav xhtml toc into a flat list of entries
    # each entry is {id title href src level}
    try:
        data = zf.read(nav_href)
    except KeyError:
        return []

    root    = ET.fromstring(data)
    nav_dir = str(PurePosixPath(nav_href).parent)
    if nav_dir == '.':
        nav_dir = ''
    entries = []

    # locate the nav element whose epub type attribute contains toc
    toc_nav = None
    for el in root.iter(_ns('xhtml', 'nav')):
        etype = el.get(_ns('epub', 'type'), '')
        if 'toc' in etype.split():
            toc_nav = el
            break
    if toc_nav is None:
        toc_nav = root.find('.//' + _ns('xhtml', 'nav'))
    if toc_nav is None:
        return []

    def _walk_ol(ol_el, level):
        # walk ordered list elements recursively
        for li in ol_el.findall(_ns('xhtml', 'li')):
            a    = li.find(_ns('xhtml', 'a'))
            span = li.find(_ns('xhtml', 'span'))
            title = ''
            href  = ''
            if a is not None:
                href  = a.get('href', '').split('#')[0].replace('\\', '/')
                title = ''.join(a.itertext()).strip()
            elif span is not None:
                title = ''.join(span.itertext()).strip()
            full = (nav_dir + '/' + href).lstrip('/') if nav_dir and href else href
            if title and full:
                entries.append({
                    'id':    'nav-%d' % len(entries),
                    'title': title,
                    'href':  full,
                    'src':   href,
                    'level': level,
                })
            nested = li.find(_ns('xhtml', 'ol'))
            if nested is not None:
                _walk_ol(nested, level + 1)

    root_ol = toc_nav.find(_ns('xhtml', 'ol'))
    if root_ol is not None:
        _walk_ol(root_ol, 1)

    return entries


def _load_epub(epub_path):
    # open epub and return (zf meta manifest spine entries)
    # entries is the TOC list used for all navigation
    zf   = _open_zip(epub_path)
    opf  = _get_opf_path(zf)
    meta, manifest, spine, ncx_href, nav_href, _ = _parse_opf(zf, opf)

    entries = []

    # prefer EPUB 3 nav document over EPUB 2 NCX
    if nav_href:
        entries = _parse_nav(zf, nav_href)
    if not entries and ncx_href:
        entries = _parse_ncx(zf, ncx_href)

    # final fallback when no TOC file found - build from spine order
    if not entries:
        for i, iid in enumerate(spine):
            if iid in manifest:
                item = manifest[iid]
                entries.append({
                    'id':    iid,
                    'title': 'Section %d' % (i + 1),
                    'href':  item['full_href'],
                    'src':   item['href'],
                    'level': 1,
                })

    return zf, meta, manifest, spine, entries


def _find_entry(entries, ref):
    # resolve ref to a TOC entry
    # ref may be a 1-based integer index a full id string or a partial title
    try:
        idx = int(ref) - 1
        if 0 <= idx < len(entries):
            return entries[idx]
        sys.exit('[error] index %s out of range - valid range is 1 to %d' % (ref, len(entries)))
    except ValueError:
        pass

    # exact id match
    for e in entries:
        if e['id'] == ref:
            return e

    # case-insensitive partial title match
    rl = ref.lower()
    hits = [e for e in entries if rl in e['title'].lower()]
    if len(hits) == 1:
        return hits[0]
    if len(hits) > 1:
        lines = ['  %d: %s' % (entries.index(h) + 1, h['title']) for h in hits]
        sys.exit('[error] ambiguous match - run toc command to see all titles\n' + '\n'.join(lines))

    sys.exit('[error] no chapter found matching: %s' % ref)


def _read_file(zf, href):
    # read a file from the zip archive
    # tries exact path then basename fallback when exact path is absent
    href = href.replace('\\', '/')
    try:
        return zf.read(href)
    except KeyError:
        pass
    # fallback: search all names for matching basename
    base = href.split('/')[-1]
    for name in zf.namelist():
        if name.split('/')[-1] == base:
            return zf.read(name)
    sys.exit('[error] content file not found in epub: %s' % href)


# ---- command implementations ----

def cmd_toc(epub_path):
    # output full TOC as JSON with index id title href and indent level
    zf, meta, manifest, spine, entries = _load_epub(epub_path)
    out = {
        'source':        epub_path,
        'title':         meta.get('title', ''),
        'author':        meta.get('creator', ''),
        'total_entries': len(entries),
        'entries': [
            {
                'index': i + 1,
                'id':    e['id'],
                'title': e['title'],
                'href':  e['href'],
                'level': e['level'],
            }
            for i, e in enumerate(entries)
        ],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    zf.close()


def cmd_info(epub_path):
    # output book metadata and structural counts as JSON
    zf, meta, manifest, spine, entries = _load_epub(epub_path)
    out = {
        'title':          meta.get('title', ''),
        'author':         meta.get('creator', ''),
        'language':       meta.get('language', ''),
        'publisher':      meta.get('publisher', ''),
        'identifier':     meta.get('identifier', ''),
        'date':           meta.get('date', ''),
        'toc_entries':    len(entries),
        'spine_items':    len(spine),
        'manifest_items': len(manifest),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    zf.close()


def cmd_read(epub_path, ref, full=False):
    # locate chapter by ref then extract and print plain text content
    # truncates at 8999 chars unless --full flag is passed
    zf, meta, manifest, spine, entries = _load_epub(epub_path)
    entry   = _find_entry(entries, ref)
    raw     = _read_file(zf, entry['href'])
    text    = _html_to_text(raw)
    idx     = entries.index(entry) + 1
    total   = len(entries)
    header  = '=== %s  [%d of %d] ===' % (entry['title'], idx, total)
    print(header)
    print()
    limit = None if full else 8999
    if limit and len(text) > limit:
        print(text[:limit])
        print('\n[... %d chars remaining - rerun with --full to read all]' % (len(text) - limit))
    else:
        print(text)
    zf.close()


def cmd_search(epub_path, query):
    # search TOC titles for query and output matching entries as JSON
    zf, meta, manifest, spine, entries = _load_epub(epub_path)
    ql   = query.lower()
    hits = [e for e in entries if ql in e['title'].lower()]
    out  = {
        'query':         query,
        'total_matches': len(hits),
        'matches': [
            {'index': entries.index(e) + 1, 'id': e['id'], 'title': e['title'], 'href': e['href']}
            for e in hits
        ],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    zf.close()


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__)
        sys.exit(1)

    cmd  = args[0]
    path = args[1]

    if cmd == 'toc':
        cmd_toc(path)
    elif cmd == 'info':
        cmd_info(path)
    elif cmd == 'read':
        if len(args) < 3:
            sys.exit('[error] read requires a chapter reference argument')
        cmd_read(path, args[2], full='--full' in args)
    elif cmd == 'search':
        if len(args) < 3:
            sys.exit('[error] search requires a query argument')
        cmd_search(path, args[2])
    else:
        sys.exit('[error] unknown command: %s  valid commands are toc info read search' % cmd)


if __name__ == '__main__':
    main()
