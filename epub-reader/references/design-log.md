# epub-reader Design Log

## Prompt formulation candidates

Three candidate core prompt structures were evaluated before writing SKILL.md.

### Candidate 1 - Direct role and context framing

```
Role: You are an epub document navigator.
Context: The user wants to read content from an epub ebook file.
An epub is a ZIP archive containing HTML content organized by a manifest and TOC.
Task: Always consult the TOC before reading any content.
Use the TOC map to locate the correct file then extract its plain text.
```

Strength: clear orientation for the agent.
Weakness: does not communicate the sequential dependency between steps.
The agent may skip the TOC step if the chapter number is obvious from context.

### Candidate 2 - Chained workflow prompt

```
When reading an epub follow these steps in order:
1 Run toc to extract and display the chapter map
2 Identify the target section from the TOC output
3 Run read with the chapter ref to retrieve content
4 Present the extracted text to the user
```

Strength: sequential ordering enforces the TOC-first constraint.
Weakness: requires a decision table to handle different user intents.

### Candidate 3 - Few-shot pattern

```
Example
Input: read chapter 3 of this epub
Step 1: python scripts/epub_reader.py toc book.epub
Step 2: find entry with index 3 in output
Step 3: python scripts/epub_reader.py read book.epub 3
Output: plain text of chapter 3
```

Strength: concrete and easy to follow.
Weakness: does not cover search or info commands and does not explain the why behind TOC-first.

### Selected formulation

Candidate 2 was selected as the primary structure for SKILL.md.

Rationale: the epub reading task is inherently sequential with a hard dependency.
The TOC must be read before any chapter can be located.
A chained workflow prompt makes this dependency explicit and resistant to agent shortcutting.
The decision table supplements it to handle the variety of user intents without making the chain too long.

## Community research

Epub reading is used by developers building ebook tools, researchers extracting text for NLP, and AI agents summarizing books.
Common pain points found in community discussions:

1 EPUB 2 vs EPUB 3 format differences break naive parsers that assume one TOC format
2 Relative path resolution from OPF directory is a frequent source of KeyError bugs
3 HTML chapter files often have non-standard namespace declarations that break ElementTree
4 Fragment identifiers in NCX hrefs cause file-not-found errors when used as zip paths
5 Some epub files embed OPF at the zip root instead of in a subdirectory

All five pain points are addressed in the script design.

## Dependency decision

The script intentionally uses Python 3 stdlib only.
No lxml beautifulsoup or ebooklib dependency.
Rationale: skills must work in the sandbox environment without pip install.
The stdlib html.parser and ElementTree are sufficient for well-formed XHTML content.
