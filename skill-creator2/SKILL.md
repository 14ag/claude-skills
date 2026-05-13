---
name: skill-creator2
description: Create, improve, and evaluate Claude skills with a QA-first workflow. Use when users ask to build a skill, improve this skill, refine this one, make this better, run benchmark-only validation, or optimize a skill description for reliable triggering.
---

# Skill Creator

A skill for creating new skills and iteratively improving existing skills.

## Fast Path: "Improve this skill" with no specs

When the user gives a vague refinement request (for example: "use skill-creator to refine this skill", "make this better"), do not start with broad spec questions. Run this QA-first intake path first.

1. Identify the target skill path and current name.
2. Snapshot the current skill before editing.
3. Ensure `QA.txt` exists in the target skill root. Append missing baseline checks from `assets/QA.txt`.
4. Run a comprehensive QA pass against that `QA.txt`.
5. Produce an improvement brief with prioritized issues, expected impact, and risk.
6. Present 2-3 concrete improvement options and recommend one.
7. If the user gives minimal direction, proceed with the recommended option.

Use this fast path as the default for underspecified improvement requests.

## Workflow Map

Use triage first, then follow the matching workflow.

| Situation | Path |
|---|---|
| Brand new skill | Capture Intent -> Write -> Test -> Iterate |
| Improving an existing skill with clear specs | Capture Intent -> Edit -> Test -> Iterate |
| Improving an existing skill, specs not provided | Run QA-first fast path, then continue with scoped improvements |
| QA or benchmarking only (mature skill) | Skip writing. Evaluate as-is first, then propose improvements |
| User wants to review outputs/results before more edits | Jump to eval loop review step and launch user review view first |
| User asks "is the new version actually better?" | Run blind comparison workflow |
| User asks to optimize triggering | Run description optimization workflow |
| User asks to package/install the skill | Run packaging workflow |

If the conversation already includes requirements, extract them before asking new questions.

## Feature Entry Points

Every major feature must be reachable from a concrete user cue.

| User cue | Feature | Entry action |
|---|---|---|
| "create a skill for X" | Skill creation | Start capture-intent flow |
| "improve this skill" (vague) | QA-first improvement intake | Run fast path before broad interviews |
| "edit this part of the skill" | Scoped refinement | Start existing-skill edit flow |
| "test/benchmark/QA this skill" | QA/benchmark-only mode | Evaluate as-is first |
| "show me outputs to review" or iteration eval in progress | User review workflow | Generate review viewer before more edits unless user opts out |
| "is new version better?" | Blind comparison | Run comparator + analyzer |
| "improve triggering" | Description optimization | Run trigger-eval optimization loop |
| "package it" / "I want the .skill file" | Packaging | Run package script and provide artifact path |
| Environment constraints (no subagents/headless) | Environment adapter | Switch to environment-specific reference workflow |

## Prompt Engineering Reference

Before writing or revising prompt text for any skill, read
`references/prompt-engineering-best-practices.md`.

This is required guidance. All prompt blocks should follow this default shape:

`role -> context -> task -> constraints -> output format`

Apply with judgment:

- Use reasoning guidance only when the task benefits from multi-step thinking.
- Add a self-check pattern for evaluative outputs.
- Use XML-style tags or clear delimiters when mixing instructions, examples, context, and dynamic input.
- For long-context tasks, ground outputs in quoted or clearly identified evidence.
- Surface hidden assumptions and ask for clarification when requirements are underspecified.

## Core Workflow

### 1) Capture Intent and Research

Read `references/intake-and-triage.md` before drafting or editing.

You must:

- Clarify the user goal, trigger conditions, output format, constraints, and success criteria.
- After scoping content, document the skill's conversational interface: (1) clarifying questions in priority order; (2) response template shape for the primary trigger; (3) out-of-scope or error cases as explicit dialogue policy the agent can act on.
- Research professional standards and official documentation relevant to the target domain before writing logic.
- For skills targeting hobbyist or practitioner communities, research the social platforms where that community is active (forums, subreddits, GitHub topic searches) to surface real pain points and ecosystem gaps that official docs omit. See `references/intake-and-triage.md` §5 for the platform lookup table and recording requirements.
- For skills that target multiple platforms, tool versions, or environments: enumerate every axis of variance before writing sections. Produce a compatibility matrix covering features, environment variables, paths, and supported versions per platform. A section written only for one platform variant and silently wrong on another is a QA failure, not a content gap.
- For each new or refined skill, draft 3 candidate core prompt formulations, pick the best, and record rationale in `references/design-log.md`.

### 2) Write or Edit the Skill

When writing `SKILL.md` for the target skill:

- Preserve skill name and directory when refining an existing skill.
- Keep frontmatter valid and description specific enough to trigger reliably.
- Keep instructions imperative and deterministic.
- Keep `SKILL.md` lean and router-like. Move heavy implementation details to `references/`.
- For every file placed in `scripts/`, add an entry in `SKILL.md` that states when to run it, the exact command, how to interpret its output, and what to do if it fails.
- Before finalising `SKILL.md`, scan the content for values users will look up repeatedly (paths, env vars, version strings, command flags). Consolidate those into lookup tables in `SKILL.md` instead of scattering them in prose or references/.

Progressive disclosure standard:

1. Metadata (`name`, `description`) should define what and when.
2. `SKILL.md` should route to the right reference files.
3. Scripts and references should hold heavy details and repeatable procedures.

### 3) Test and Evaluate

Read `references/eval-loop.md` and execute it as one continuous sequence.

The test/eval workflow includes:

- Run `python -m scripts.quick_validate .` from the target skill root.
- Immediately run mandatory QA against that skill's `QA.txt`.
- Treat QA as passing only when every question in the created or edited skill
  root `QA.txt` is answered `yes`.
- Run a negative-trigger smoke test with an obviously unrelated prompt to confirm the skill does not load; record the prompt and outcome in the workspace.
- Create realistic eval prompts and save `evals/evals.json`.
- Run with-skill and baseline runs in parallel where supported.
- Draft and refine assertions while runs execute.
- Use all `agents/*.md` workflows as part of testing: `agents/grader.md` for
  grading, `agents/comparator.md` for paired blind comparisons, and
  `agents/analyzer.md` for benchmark and post-comparison analysis.
- Grade outputs, aggregate benchmark data, and generate the review viewer.
- Trigger user review with eval-viewer auto-submit mode and wait for completion before additional edits.
- Collect user feedback and continue iteration.

### 4) Improve and Iterate

After each edit cycle, run the loop in `references/eval-loop.md`.

Required quality gates before presenting changes:

- Ensure QA bootstrap was completed before any create/edit/evaluate action:
  `QA.txt` exists and missing `assets/QA.txt` questions were appended as-is.
- After each edit, run Comprehensive QA pass #1 against current `QA.txt`.
- Then review description quality and append missing skill-specific QA checks.
- Run Comprehensive QA pass #2 against the expanded `QA.txt` to confirm
  improvement, no regressions, and preserved objective fit.
- Do not treat the QA stage as complete unless every question in the target
  skill root `QA.txt` is answered `yes`.
- Feature discoverability and integration checks for new phases.
- Keep the target skill's `SKILL.md` within practical router size limits.

Stop when:

- The user confirms satisfaction, or
- Feedback is consistently empty, or
- Additional iterations stop producing meaningful gains.
- When the user confirms satisfaction, explicitly ask them for recommendations to improve the skill-creator itself.

## Advanced: Blind Comparison

For rigorous A/B evaluation between two skill versions, use:

- `agents/comparator.md` for blind output comparison
- `agents/analyzer.md` for post-hoc winner/loser analysis

Use this when the user asks whether the new version is actually better.

## Description Optimization

After creation or improvement, offer to optimize skill triggering.

Read `references/description-optimization.md`.

Important rules:

- Description must describe concrete situations, not just capabilities.
- Include at least one realistic example trigger phrase.
- Evaluate both should-trigger and should-not-trigger cases.
- Prefer test-score-selected descriptions over train-only wins to reduce overfitting.

## Packaging and Delivery

When finalizing a skill, package with:

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

If the environment supports presenting files, provide the packaged `.skill` path.

## Environment Adapters

Read `references/environment-adapters.md` for environment-specific behavior:

- Claude Code (subagents and full loop)
- Claude.ai (no subagents)
- Cowork/headless environments

The high-level workflow remains the same; only execution mechanics differ.

## Reference Index

### Core references

- `references/intake-and-triage.md` - triage, QA-first vague-improvement intake, interview flow, design-log requirements
- `references/eval-loop.md` - test execution, grading, benchmark aggregation, review viewer, feedback loop, iteration gates
- `references/description-optimization.md` - trigger eval set design and optimization loop
- `references/environment-adapters.md` - Claude.ai and Cowork execution differences
- `references/file-routing-index.md` - complete non-root file routing map for discoverability/QA
- `references/schemas.md` - JSON schemas for eval and benchmark artifacts
- `references/prompt-engineering-best-practices.md` - required prompt construction rules
- `references/prompt-research-notes.md` - supporting research notes

### Subagent references

- `agents/grader.md` - grading assertions against outputs
- `agents/comparator.md` - blind A/B comparison
- `agents/analyzer.md` - benchmark and post-hoc analysis

### QA baseline

- `assets/QA.txt` - baseline QA checklist to merge into target skill `QA.txt`

## Operating Principles

- Be flexible with user preference while preserving evaluation rigor.
- Never use emojis.
- Avoid AI fluff and ambiguous language.
- Prefer deterministic steps over vague guidance.
- Use the highest available reasoning effort by default for design-critical work that reduces future user effort. Only trade down when the user explicitly prefers speed.
- Preserve existing features unless the user requests removal.
- Never skip QA just because a request is underspecified.
