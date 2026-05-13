# Commit Message Writing

Use this reference when the user asks for a git commit message or asks to
improve an existing one.

Also read:
- `references/writing-standards.md`

## Goal

Produce a Conventional Commit message that explains what changed and why,
without sounding inflated or generic.

> Source: https://www.conventionalcommits.org/en/v1.0.0/

## Workflow

1. Inspect the provided diff, summary, or changed files.
2. Choose the smallest accurate commit type:
   - `feat`
   - `fix`
   - `docs`
   - `style`
   - `refactor`
   - `perf`
   - `test`
   - `build`
   - `ci`
   - `chore`
3. Add a scope only when it helps the reader.
4. Write the subject in imperative mood.
5. Keep the first line concise and do not end it with a period.
6. If a body is useful, separate it from the subject with a blank line and
   explain the what and why rather than the implementation detail.
7. If the change is breaking, add `!` after the type or scope and include a
   `BREAKING CHANGE:` footer.

## Output Format

Return the commit message in a fenced Markdown block.

Example:

```text
fix(auth): Reject passwords longer than 32 chars

Validate password length before the login request so the page no longer crashes
when oversized input reaches the client-side form handler.
```

## Guardrails

- Do not claim files or behaviors that are not present in the supplied context.
- Do not invent ticket numbers or scopes.
- If the change set really contains multiple unrelated changes, say so and
  offer 2-3 commit split options instead of forcing one weak message.
