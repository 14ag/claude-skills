---
name: epub-reader
description: "Use this skill when the user wants to read, navigate, extract, or summarize content from an epub ebook file. Trigger phrases include: 'read this epub', 'open this ebook', 'what does chapter X say', 'summarize this book', 'show me the table of contents', 'find the section about X in this epub', 'epub file', '.epub'. Always consult the TOC before reading any content. Do NOT use for PDF, DOCX, or other non-epub formats."
---

# epub-reader

Read and navigate epub ebook files using a TOC-first strategy.
An epub is a ZIP archive containing HTML chapter files organized by a manifest and table of contents.
Always map the book structure via the TOC before reading any chapter content.

## Workflow

Follow these steps in order for every epub reading task.

### Step 1 - Inspect the file

```bash
python scripts/epub_reader.py info <epub_path>
```

Output is JSON with title author language publisher and structural counts.
Present the book title and author to the user before proceeding.

### Step 2 - Load and display the TOC

```bash
python scripts/epub_reader.py toc <epub_path>
```

Output is JSON with an `entries` array.
Each entry has `index`, `id`, `title`, `href`, and `level`.
Present the TOC as a numbered list using the `title` and `index` fields.
The `href` field is the internal path used when reading.
Do not skip this step. The TOC is the navigation map for all subsequent reads.

### Step 3 - Read a chapter

```bash
python scripts/epub_reader.py read <epub_path> <ref>
```

`ref` is a 1-based index number, an exact TOC entry id, or a partial title string.
The script resolves the ref against the TOC and extracts plain text from the HTML file.
Output is truncated to 8999 chars by default.
To read the full chapter without truncation:

```bash
python scripts/epub_reader.py read <epub_path> <ref> --full
```

### Step 4 - Search the TOC (optional)

When the user asks about a topic and the chapter is not obvious from the TOC:

```bash
python scripts/epub_reader.py search <epub_path> "<query>"
```

Output lists all TOC entries whose titles match the query.
Use the returned index to run a `read` command.

## Decision rules

| User asks for | Action |
|---|---|
| Table of contents or chapter list | Run `toc` and present as numbered list |
| A specific chapter by name or number | Run `toc` first then `read` with matching index |
| A topic or keyword | Run `search` then `read` the best match |
| Book metadata or summary of what the book is | Run `info` and `toc` then synthesize |
| Full book content | Warn user that full extraction can be large then loop `read` over all entries |

## Error handling

| Error message | Cause | Fix |
|---|---|---|
| `not a valid epub zip` | File is not an epub or is corrupted | Ask user to verify the file |
| `META-INF/container xml missing` | File is not a valid epub container | Try running `file <path>` to confirm format |
| `content file not found in epub` | TOC entry href does not match zip contents | Run `toc` to get valid hrefs and retry |
| `ambiguous match` | Partial title matched multiple entries | Use the numeric index from `toc` output instead |
| `index N out of range` | Index exceeds total entry count | Check `total_entries` in `toc` output |

If `toc` returns zero entries, the epub has no readable TOC.
Fall back to reading by spine order using numeric index starting at 1.

## Script reference

See `references/epub-structure.md` for details on EPUB format internals, namespace constants, and edge cases the script handles.

Script location: `scripts/epub_reader.py`
Run from the skill root directory or pass absolute paths.
No external dependencies. Uses Python 3 stdlib only.
