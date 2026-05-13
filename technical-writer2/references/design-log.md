# Design Log

## Triage

- Path selected: existing skill, clear requested changes
- Target skill: `technical-writer`
- Requested changes:
  - make thorough refinements to the skill
  - make GitHub issue writing more explicit and easier to trigger

## Baseline Findings

Top issues before edits:

1. `SKILL.md` exposed only part of the implemented feature set and did not make
   issue writing feel first-class.
2. Commit-message and repository-settings flows were buried inside the
   documentation reference instead of being routed directly.
3. The QA file did not include the baseline `skill-creator` checklist.
4. Several reference files had encoding noise and uneven instruction density.
5. Script entry points existed but were not documented precisely in the router.

## Improvement Options

1. Router-only cleanup
   - Lowest risk
   - Improves discoverability, but leaves issue-writing depth mostly unchanged
2. Router plus GitHub issue overhaul
   - Good balance
   - Makes issue drafting and template authoring a first-class path
3. Full router decomposition with issue, commit, and metadata split
   - Recommended
   - Best for progressive disclosure, discoverability, and long-term maintenance

Selected option: 3

## Prompt Formulations Considered

### Candidate 1: Direct role/context framing

Role: You are a repository-focused technical writer.
Context: The user wants documentation, GitHub issues, or repo metadata for a
software project. Preserve repository facts and route to the narrowest task.
Task: Produce the requested artifact using the matching standards reference.
Constraints: Do not invent technical details. Keep prose direct. Load only the
needed reference files.
Output format: Write files when asked; otherwise return fenced Markdown.

### Candidate 2: Chained workflow prompt

1. Classify the request into docs, issues, commit messages, or repo settings.
2. Read the matching reference plus the shared writing standards.
3. Gather facts from the repo or supplied context.
4. Draft the artifact in the required structure.
5. Verify it contains only grounded claims before returning it.

### Candidate 3: Few-shot routing prompt

Example:
- Input: "write an issue about the login page crashing"
- Route: issue writer
- Output: bug-report title and body

Example:
- Input: "generate a README"
- Route: docs generator
- Output: repository documentation files

Example:
- Input: "write a commit message"
- Route: commit message writer
- Output: Conventional Commit

## Prompt Choice

Selected candidate: 2

Reason:
- The skill is a router with multiple distinct entry points.
- A chained workflow matches the real decision sequence better than a pure role
  prompt.
- It keeps the skill deterministic while still small enough to preserve context.

## Source Asset Audit

Non-documentation assets present:

- `scripts/launch-form.ps1`
- `scripts/launch-repo-settings.ps1`
- `scripts/form.html`
- `scripts/repo-settings.html`

Decisions:

- Keep both PowerShell launchers in `scripts/` and document exact usage in
  `SKILL.md`.
- Treat both HTML files as support assets, not primary routing documents.

## Research Notes

Official documentation reviewed for this refinement:

- GitHub community profile guidance
- GitHub issue template and issue form guidance
- GitHub issue quickstart guidance
- Conventional Commits specification

Key takeaways applied:

1. GitHub issue templates and issue forms should be treated as separate output
   shapes with different metadata requirements.
2. Issue drafting should account for repository templates before defaulting to a
   generic bug or feature structure.
3. Community-health file placement rules should stay centralized in a reference,
   not in the router.
