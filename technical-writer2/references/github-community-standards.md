# GitHub Community Standards

Use this reference when the task depends on GitHub's recognized repository
health files, placement rules, or issue-template behavior.

> Source: https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories
> Source: https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file

## Community Profile Checklist

GitHub's community profile checks for these repository assets:

| File | Valid locations | Notes |
|---|---|---|
| `README.md` | root, `docs/`, `.github/` | root is the usual default |
| `LICENSE` | root | keep at root |
| `CONTRIBUTING.md` | root, `docs/`, `.github/` | linked when contributors open issues or PRs |
| `CODE_OF_CONDUCT.md` | root, `docs/`, `.github/` | recognized by GitHub |
| `SECURITY.md` | root, `docs/`, `.github/` | shown from the Security tab |
| Issue templates | `.github/ISSUE_TEMPLATE/` | recommended |
| Pull request template | root, `docs/`, `.github/` | recommended |

## Placement Precedence

For community health files, GitHub resolves locations in this order:

1. `.github/<FILE>`
2. `docs/<FILE>`
3. `<root>/<FILE>`

Exception:
- `LICENSE` should remain in the repository root.

## README Expectations

> Source: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes

A repository README should help the reader answer:

- what the project does
- why the project is useful
- how to get started
- where to get help
- who maintains or contributes to the project

## CONTRIBUTING Expectations

> Source: https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors

When present, GitHub surfaces `CONTRIBUTING.md` while users open issues and pull
requests. The guide should cover:

- how to report bugs
- how to suggest features
- development setup
- coding conventions
- pull request process
- commit message expectations
- where to ask questions

## Code of Conduct

> Source: https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-code-of-conduct-to-your-project

GitHub recognizes standard code-of-conduct files and surfaces them in the
community profile. Contributor Covenant v2.1 is a common default.

## Security Policy

> Source: https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository

`SECURITY.md` should state:

- which versions receive security fixes
- how to report a vulnerability
- what response policy contributors can expect

## Issue Templates and Issue Forms

> Source: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates

Key rules:

- store issue templates in `.github/ISSUE_TEMPLATE/`
- Markdown templates use `.md`
- issue forms use `.yml`
- template chooser behavior can be customized with
  `.github/ISSUE_TEMPLATE/config.yml`

Community-profile eligibility:

- Markdown issue templates should include valid YAML frontmatter with `name:` and
  `about:`
- issue forms should include valid `name:` and `description:`

## Pull Request Template

Use `.github/PULL_REQUEST_TEMPLATE.md` or one of the other supported GitHub
locations when the repository wants a default PR body.

Typical sections:

- summary of changes
- related issue
- type of change
- testing performed
- checklist
