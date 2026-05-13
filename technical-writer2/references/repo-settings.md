# Repository Metadata Editing

Use this reference when the user asks to update repository description,
homepage, or topics.

## Goal

Gather or infer repository metadata, then apply it safely through GitHub CLI
when the user wants automation.

## Workflow

1. Scan the repository for project name, languages, frameworks, package
   manifests, and existing public-facing descriptions.
2. Draft:
   - a concise repository description
   - a homepage URL if one is already evident from the project
   - up to 8 repository topics grounded in the detected stack and domain
3. If the user wants form-driven editing, run:

```powershell
pwsh -File scripts/launch-repo-settings.ps1 -SuggestedTopics "react,typescript,node" -OutputPath "./repo-settings.json"
```

4. Read `repo-settings.json`.
5. If GitHub CLI is available and the user asked for direct application, run:

```powershell
gh repo edit --description "<description>" --homepage "<homepage>"
gh api -X PUT /repos/{owner}/{repo}/topics -f names[]=topic1 -f names[]=topic2
```

## Topic Rules

- Prefer framework, runtime, platform, and domain topics over vague adjectives.
- Do not add duplicate or near-duplicate topics.
- Avoid topics that the repository does not clearly support.

## Failure Handling

- If the form launch fails, ask for all missing metadata in one message.
- If `gh` is unavailable, return the proposed description, homepage, and topics
  so they can be applied manually.
- If the repository owner and name cannot be determined, stop before API calls
  and surface the missing value clearly.
