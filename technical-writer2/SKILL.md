---
name: technical-writer2
description: >
  Technical writing router for software repositories. Use when the user asks to
  create or improve README, CONTRIBUTING, CHANGELOG, SECURITY, wiki, or
  community health files; draft or refine GitHub issues, bug reports, feature
  requests, task issues, or issue templates/forms; edit repository description,
  homepage, or topics; or write Conventional Commit messages. Do not use for
  code implementation, debugging, or general prose unrelated to a software
  project.
---

# Technical Writer

This skill handles repository-facing technical writing for software projects.
Keep this file lean. Read only the reference files needed for the current task.

## Operating Rules

1. Identify the narrowest writing job that fully answers the user.
2. Read `references/writing-standards.md` for every prose task longer than a
   sentence.
3. Load only the task-specific reference that matches the request.
4. Preserve existing repository facts. Do not invent features, commands, file
   paths, versions, or workflows.
5. If the request is unrelated to software-project writing, do not force this
   skill.

## Capability Map

### 1. Documentation Generation and Refinement

Use this path when the user asks to create or improve repository docs such as
`README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `SECURITY.md`, wiki pages, or
GitHub community health files.

Read:
- `references/generate-docs.md`
- `references/github-community-standards.md` when placement or community health
  rules matter
- `references/ms-engineering-playbook-docs.md` when the repository uses Azure
  DevOps, a code wiki, or the user explicitly wants Microsoft-style docs

### 2. GitHub Issue Writing

Use this path when the user asks to write or refine:
- a GitHub issue
- a bug report
- a feature request
- a task or tracking issue
- issue templates or issue forms

Read:
- `references/issue-writer.md`

This is a first-class skill capability. Prefer this path for prompts like
"write an issue about the login page crashing", "turn this into a feature
request", or "create bug and feature request templates".

### 3. Commit Message Writing

Use this path when the user asks to write, rewrite, or improve a git commit
message.

Read:
- `references/commit-messages.md`

### 4. Repository Metadata Editing

Use this path when the user asks to update repository description, homepage, or
topics, especially when the task should flow through a small launch form and
GitHub CLI automation.

Read:
- `references/repo-settings.md`

## Intent Routing

If the request is vague but clearly about repository writing, present this menu:

- `A` Generate new documentation
- `B` Improve existing documentation
- `C` Edit repository details
- `D` Compose or refine a GitHub issue
- `E` Write a commit message

If the user already named the artifact they want, skip the menu and route
directly to the matching reference.

## Script Entry Points

### `scripts/launch-form.ps1`

Run only when documentation generation is blocked by missing high-impact
metadata that cannot be inferred from the repository.

Command:
```powershell
pwsh -File scripts/launch-form.ps1 -MissingFields "name,description" -OutputPath "./doc-metadata.json"
```

Interpretation:
- On success, read `doc-metadata.json` and continue the documentation workflow.
- On failure or no submission, fall back to one consolidated clarification
  message instead of repeated questions.

### `scripts/launch-repo-settings.ps1`

Run when the user wants to edit repository description, homepage, or topics
through the local form before applying changes with GitHub CLI.

Command:
```powershell
pwsh -File scripts/launch-repo-settings.ps1 -SuggestedTopics "react,typescript,node" -OutputPath "./repo-settings.json"
```

Interpretation:
- On success, read `repo-settings.json`, then apply the values with GitHub CLI
  if the user asked for automation.
- On failure or no submission, provide the fields to edit manually and do not
  assume values.

Supporting assets:
- `scripts/form.html`
- `scripts/repo-settings.html`

## Output Policy

- Keep generated prose aligned with `references/writing-standards.md`.
- When the task maps to a repository file, write or update the file in the
  correct repository location.
- When the task is a GitHub issue or commit message, return the final content in
  a fenced Markdown block unless the user explicitly asked for direct file
  edits.
