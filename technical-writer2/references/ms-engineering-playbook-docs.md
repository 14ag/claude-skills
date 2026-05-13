# Microsoft and Azure DevOps Documentation Notes

Use this reference when the user explicitly wants Microsoft-style repository
documentation or when the project uses Azure DevOps wiki conventions.

> Source: https://microsoft.github.io/code-with-engineering-playbook/documentation/tools/wikis/
> Source: https://learn.microsoft.com/en-us/azure/devops/project/wiki/wiki-file-structure

## Core Principles

Microsoft's engineering guidance treats documentation as part of the codebase.
For this skill, that means:

- keep docs close to the code they describe
- update docs in the same change that updates behavior
- prefer discoverable, minimal, maintained documents over broad but stale prose

## Common Repository Artifacts

Typical repository-level docs include:

- `README.md`
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `docs/` for extended material
- `.github/` for issue and pull request templates

## Azure DevOps Wiki Structure

When the repository uses an Azure DevOps code wiki, prefer:

- one Markdown file per page
- `.order` files for navigation order
- predictable page names such as `Home.md`, `Getting-Started.md`,
  `Architecture.md`, and `Troubleshooting.md`

Constraints to remember:

- keep paths reasonably short
- avoid file names that start or end with `/`, `\`, `#`, or `.`
- keep navigation consistent between folders and links

## Cross-Platform Docs-as-Code Guidance

When the same docs should work in both GitHub and Azure DevOps:

- keep pages in `docs/`
- use normal relative Markdown links
- avoid platform-specific wiki-link syntax
- generate `.order` only when Azure DevOps support is needed
- generate `_Sidebar.md` only when GitHub wiki navigation is needed
