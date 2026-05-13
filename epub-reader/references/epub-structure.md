# epub-reader: epub Format Reference

## Container structure

An epub file is a ZIP archive.
The entry point is always `META-INF/container.xml`.
That file contains a `rootfile` element whose `full-path` attribute points to the OPF file.
The OPF file is the package document that defines all book content.

```
book.epub (ZIP)
  META-INF/
    container.xml          <- always here - points to OPF
  OEBPS/ (or any folder)
    content.opf            <- package document
    toc.ncx                <- EPUB 2 table of contents (optional in EPUB 3)
    nav.xhtml              <- EPUB 3 navigation document
    chapter1.xhtml
    chapter2.xhtml
    images/
      cover.jpg
```

## OPF package document

The OPF file has three key child elements.

### metadata

Contains Dublin Core fields:
- `dc:title` - book title
- `dc:creator` - author name
- `dc:language` - BCP-47 language code
- `dc:publisher` - publisher name
- `dc:identifier` - ISBN or UUID
- `dc:date` - publication date

### manifest

Lists every file in the epub as `item` elements with `id`, `href`, and `media-type`.
The `properties` attribute on an item signals special roles.
A `properties="nav"` item is the EPUB 3 navigation document.
An item with `media-type="application/x-dtbncx+xml"` is the EPUB 2 NCX toc file.

### spine

An ordered list of `itemref` elements referencing manifest item ids.
The spine defines reading order.
Items with `linear="no"` are supplementary and excluded from the main reading flow.
The spine `toc` attribute may reference the manifest id of the NCX file.

## Table of contents variants

### EPUB 2 - toc.ncx

Uses the `http://www.daisy.org/z3986/2005/ncx/` namespace.
The main element is `navMap` which contains nested `navPoint` elements.
Each `navPoint` has an `id`, a `navLabel/text` child for the title, and a `content` child whose `src` attribute is the chapter href.
Nesting depth maps to the `level` field in the script output.

### EPUB 3 - nav.xhtml

Uses XHTML with an `epub:type` attribute to mark sections.
The TOC is a `nav` element whose `epub:type` contains `toc`.
Inside is an `ol` list of `li` elements each containing an `a` or `span`.
Nested `ol` elements inside `li` create sub-chapters.
The script prefers the EPUB 3 nav when both exist.

### Spine fallback

When neither NCX nor nav is found the script builds a TOC from the spine item order.
Entries are titled `Section N` where N is the 1-based position.

## Path resolution

All hrefs in the NCX and nav are relative to the file that contains them.
The OPF directory prefix must be prepended to get the correct zip member path.
Fragment identifiers after `#` in hrefs are stripped when locating files.
Some epub producers use backslashes in hrefs which the script normalizes to forward slashes.

## Namespace constants used by the script

| Prefix | URI |
|---|---|
| container | urn:oasis:names:tc:opendocument:xmlns:container |
| opf | http://www.idpf.org/2007/opf |
| dc | http://purl.org/dc/elements/1.1/ |
| ncx | http://www.daisy.org/z3986/2005/ncx/ |
| xhtml | http://www.w3.org/1999/xhtml |
| epub | http://www.idpf.org/2007/ops |

## HTML to text extraction

Chapter content files are XHTML.
The script uses Python stdlib `html.parser.HTMLParser`.
Block-level elements (p h1-h6 li div br tr td th) emit a newline before their content.
Content inside `script` and `style` elements is suppressed.
Three or more consecutive newlines are collapsed to two.

## Known edge cases

Some epub producers omit the NCX entirely in EPUB 2 files and rely only on the spine.
Some producers embed the OPF at the root of the zip rather than in a subdirectory.
The script handles the root case by checking if the opf dir is empty and skipping the prefix.
Some chapter files are XHTML with no namespace which ElementTree parses without the xhtml prefix tags.
The TOC search in that case falls back to the first `nav` element found anywhere in the tree.
