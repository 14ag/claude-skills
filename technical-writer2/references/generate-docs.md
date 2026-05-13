# Documentation Generation and Refinement

Use this reference when the user asks to create or improve repository
documentation such as `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`,
`SECURITY.md`, wiki pages, or GitHub community health files.

Also read:
- `references/writing-standards.md`
- `references/github-community-standards.md` when file placement or community
  profile behavior matters
- `references/ms-engineering-playbook-docs.md` when the user wants Microsoft or
  Azure DevOps wiki conventions

## Goal

Create accurate repository documentation from the actual project, not from
generic templates or guesswork.

## Step 1: Route the Request

Choose the narrowest documentation mode:

- `generate-new-docs`
- `improve-existing-docs`
- `generate-wiki-pages`
- `generate-community-health-files`

If the prompt is vague but clearly about repository docs, show this menu:

- `A` Generate new documentation
- `B` Improve existing documentation
- `C` Edit repository details
- `D` Compose or refine a GitHub issue
- `E` Write a commit message

## Step 2: Scan the Repository

Run a light but reliable scan before writing.

Collect:

- project name
- project description
- version
- license
- primary language and secondary languages
- package manager or build system
- install, run, and test commands
- existing docs
- configuration files and environment examples
- CI, lint, and formatter configs
- repository URL if available
- contributors if available from git history

Preferred evidence sources:

1. package manifests and lockfiles
2. existing documentation
3. source tree and entry-point files
4. git metadata

If important details are still missing after scanning, infer only what the
repository strongly supports. Ask one consolidated follow-up question only when
the missing detail would materially change the output.

## Step 3: Generate or Improve the Requested Artifact

### README.md

Include only sections supported by evidence:

1. project name
2. short description
3. key features
4. prerequisites
5. installation
6. usage or quick start
7. configuration
8. testing
9. project structure
10. contributing
11. license

Omit sections with no supporting evidence.

### CONTRIBUTING.md

Cover:

1. contribution flow
2. bug-reporting path
3. feature-request path
4. local development setup
5. test expectations
6. style or linting rules
7. pull-request workflow
8. commit message convention

### CHANGELOG.md

Use Keep a Changelog structure. Populate from tags and git history when
available. If no tags exist, create `Unreleased` only.

> Source: https://keepachangelog.com/en/1.1.0/

### CODE_OF_CONDUCT.md

Use Contributor Covenant v2.1 when a standard code of conduct is needed.

> Source: https://www.contributor-covenant.org/version/2/1/code_of_conduct/

### SECURITY.md

Include:

1. supported versions
2. reporting channel
3. expected response policy

### Wiki Pages

Use `docs/` as the source-of-truth folder when the repository needs extended
documentation. Create only pages that the repository can support with evidence.

Typical candidates:

- `Home.md`
- `Getting-Started.md`
- `Architecture.md`
- `API-Reference.md`
- `Configuration.md`
- `Development-Guide.md`
- `Troubleshooting.md`

## Step 4: Improvement Mode

When improving an existing document:

1. read the current file first
2. preserve correct human-written content
3. replace inaccurate, vague, or unsupported sections
4. add missing sections only when repository evidence supports them
5. keep changes idempotent and avoid overwriting unrelated prose

## Step 5: Output Placement

Use standard repository locations:

- `README.md` -> repository root
- `CONTRIBUTING.md` -> repository root or `.github/`
- `CHANGELOG.md` -> repository root
- `CODE_OF_CONDUCT.md` -> repository root or `.github/`
- `SECURITY.md` -> repository root or `.github/`
- issue templates -> `.github/ISSUE_TEMPLATE/`
- wiki pages -> `docs/`

Prefer the location that best matches GitHub community-health behavior when the
repository does not already establish a different convention.

## Step 6: Verification

Before finishing:

1. verify commands against the repository files that define them
2. verify file paths and links
3. verify version numbers against manifests or tags
4. remove any claim that cannot be grounded
5. note any remaining uncertainty explicitly instead of hiding it
