# GitHub Issue Writing

Use this reference when the user asks to write or refine:
- a GitHub issue
- a bug report
- a feature request
- a task or tracking issue
- issue templates
- issue forms

Also read:
- `references/writing-standards.md`

## Goal

Produce a GitHub-ready issue artifact that matches repository conventions and
uses the most specific structure available.

> Source: https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/quickstart
> Source: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates

## Step 1: Classify the Request

Choose the narrowest matching mode:

- `bug-report`
- `feature-request`
- `task-issue`
- `epic`
- `docs-issue`
- `template-authoring`
- `issue-form-authoring`

If the request describes a security vulnerability, do not draft a public bug
report first. Check `SECURITY.md` and direct the report to the private channel
described there.

## Step 2: Check Repository Conventions First

Before drafting, inspect these locations when available:

- `.github/ISSUE_TEMPLATE/`
- `.github/ISSUE_TEMPLATE/config.yml`
- `SECURITY.md`
- `CONTRIBUTING.md`

Rules:

1. If a matching issue template exists, use its headings and required fields as
   the primary structure.
2. If a matching issue form exists, answer its fields and convert the result
   into the final Markdown issue body.
3. If no template exists, use the default structures in this file.
4. If repository conventions conflict with generic best practices, prefer the
   repository conventions unless they omit critical information.

## Step 3: Gather Context Without Inventing Facts

Use repository evidence and the user's prompt to fill in:

- affected area or file path
- framework or runtime involved
- version or package manager details
- reproduction conditions
- likely impact

Allowed inference:

- inferring the framework from repository files
- inferring environment details from manifests or lockfiles
- inferring likely component names from file paths

Not allowed:

- inventing versions
- claiming a root cause without evidence
- inventing labels, milestones, or assignees

When a detail is still missing, either:
- leave it out, or
- mark it as an explicit assumption in the issue body when the user clearly
  wants a draft rather than a final filed issue

## Step 4: Draft the Right Output Shape

### Bug Report

Use this structure when no repository template exists:

```markdown
## Summary

## Steps to Reproduce
1.
2.
3.

## Expected Behavior

## Actual Behavior

## Impact

## Environment
```

Guidelines:

- Title should be specific and searchable.
- Steps must be concrete and ordered.
- Separate expected behavior from actual behavior.
- Add logs, screenshots, or code snippets only when the prompt provides them or
  the repository evidence justifies them.

### Feature Request

Use this structure when no repository template exists:

```markdown
## Problem

## Proposed Change

## Alternatives Considered

## Additional Context
```

Guidelines:

- Make the problem clear before proposing the solution.
- Keep the proposal concrete enough to discuss implementation tradeoffs.
- Mention alternatives only when there is enough information to do so honestly.

### Task Issue

Use for a bounded unit of work that does not need the full narrative of a bug
report or feature request.

```markdown
## Objective

## Scope

## Acceptance Criteria
- [ ]
- [ ]

## Notes
```

### Epic

Use when the work should be broken into several follow-up items.

```markdown
## Goal

## Background

## Workstreams
- [ ] Task 1
- [ ] Task 2

## Open Questions
```

When useful, note which items should become sub-issues after filing.

## Step 5: Support Metadata When the User Needs It

GitHub issues can also carry metadata such as labels, issue type, assignees,
projects, or milestones.

If the user asks for help preparing those fields, return them separately under a
`Suggested metadata` heading and only include values that are grounded in the
repository or prompt.

Example:

```markdown
Suggested metadata
- Labels: `bug`, `frontend`
- Issue type: `Bug`
- Milestone: `v1.4.0`
```

Do not pretend metadata exists if it cannot be inferred.

## Step 6: Author Templates and Issue Forms

When the user wants reusable issue authoring assets instead of a single issue,
create files under `.github/ISSUE_TEMPLATE/`.

### Markdown Template Rules

Use `.md` when the repository wants flexible free-form authoring.

Requirements:

- include valid YAML frontmatter
- use `name:` and `about:` keys
- provide clear section prompts

Minimal example:

```markdown
---
name: Bug report
about: Report a reproducible problem
title: "[Bug]: "
labels: bug
---
```

### Issue Form Rules

Use `.yml` when the repository wants structured inputs.

Requirements:

- include `name:` and `description:`
- use GitHub issue-form schema fields
- prefer required fields for reproduction details, expected behavior, and
  environment when the repository needs consistent reports

Useful fields:

- `markdown`
- `input`
- `textarea`
- `dropdown`
- `checkboxes`

Template chooser support:

- add `.github/ISSUE_TEMPLATE/config.yml` when the user wants custom chooser
  behavior, blank-issue control, or contact links

> Source: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository
> Source: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms

## Output Format

For single issues:
- return the final title and body in a fenced Markdown block

For templates or forms:
- write the repository file(s) in `.github/ISSUE_TEMPLATE/`
- if direct file edits are not requested, present the file content in fenced
  blocks and label each path clearly

## Quality Check

Before finalizing, verify:

- the issue type matches the request
- the title is specific
- the body contains only grounded facts or clearly labeled assumptions
- repository templates were checked first when available
- the output is ready to paste into GitHub without cleanup
