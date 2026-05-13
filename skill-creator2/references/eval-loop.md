# Eval Loop and Iteration

Run this sequence without stopping halfway.

## Workspace layout

Use `<skill-name>-workspace/` as sibling to the target skill directory.
Within it, use per-iteration folders:

- `iteration-1/`
- `iteration-2/`

Within each iteration, create per-eval folders as needed.

## Pre-run quality gate

Before launching runs, validate the prompt quality checklist:

- [ ] Every instruction is unambiguous
- [ ] Output format is explicit
- [ ] Edge cases are addressed or acknowledged
- [ ] Reasoning guidance appears where reasoning is needed
- [ ] Skill description is specific enough to trigger reliably

If any item fails, revise before running evals.

## Mandatory validation -> QA sequence

Before creating, editing, or evaluating, run this order from the target skill root:

1. `python -m scripts.quick_validate .`
2. Comprehensive QA against the target skill's `QA.txt`

Do not skip the QA step after validation.
A passing QA result means every question in the created or edited skill root
`QA.txt` is answered `yes` with evidence (file path + line number). If any answer is `no`, revise before proceeding. Present the QA grid (question | yes/no | evidence) to the user before continuing.

## Automated verification discovery (run before eval prompts)

Immediately after validation/QA, scan the source material for objective verification opportunities:

1. Can any provided code, data, or APIs be turned into an automated pass/fail or scoring script?
2. If yes, add the tool under `scripts/` with CLI args, logging, and clear output semantics.
3. Wire the script into the eval loop (when to run, how to read the result, what to do on failure).
4. Prefer objective machine checks over subjective rubrics when available.

## Step 1) Generate eval prompts

Create 2-3 realistic prompts and save to `evals/evals.json`.
Do not add assertions yet.

Also write `references/design-log.md` after first draft edits to preserve design rationale.

## Step 2) Launch with-skill and baseline runs

For each eval, launch both configurations in the same turn when subagents are available:

- `with_skill`
- baseline:
  - `without_skill` for new-skill development
  - `old_skill` snapshot baseline when improving an existing skill

Always snapshot old skill baseline before edits when doing improvement comparisons.

Each eval directory should include `eval_metadata.json`:

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name",
  "prompt": "user-like task prompt",
  "assertions": []
}
```

## Step 3) Draft assertions while runs execute

Use objective, discriminating assertions when possible.
Avoid assertions that pass on superficial output.

Update both:

- per-eval `eval_metadata.json`
- `evals/evals.json`

## Step 4) Capture timing and metrics

As run results arrive, save timing data into each run directory:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

If available, also preserve `metrics.json` from run outputs.

## Step 5) Grade outputs

Use `agents/grader.md` instructions.
Save grading to `grading.json` for each run.

`grading.json` expectation entries must use:

- `text`
- `passed`
- `evidence`

## Step 6) Aggregate benchmark

Run:

```bash
python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
```

Expect outputs:

- `benchmark.json`
- `benchmark.md`

If you generate benchmark JSON manually, follow `references/schemas.md` exactly.

## Step 7) Blind comparison pass

When paired outputs exist for the same eval prompt, run a blind comparison
before user review using `agents/comparator.md`.

Compare:

- primary skill output vs. baseline output for the same eval
- new skill vs. old skill snapshot when refining an existing skill

Save comparison artifacts alongside the iteration benchmark outputs.

## Step 8) Analyst pass

Read benchmark artifacts and add pattern-level insights using
`agents/analyzer.md` guidance.

Focus on:

- non-discriminating assertions
- high variance or flakiness
- time/token tradeoffs
- repeated failure patterns by eval type
- blind comparison winner/loser patterns when comparison artifacts exist

If blind comparison artifacts exist, use the same analyzer guidance to explain
winner strengths, loser weaknesses, and concrete improvement actions before user
review.

## Step 9) Generate user review view

Use `eval-viewer/generate_review.py` rather than custom HTML.
This step is mandatory before iteration edits unless the user explicitly opts out.

If environment supports local browser server:

```bash
python eval-viewer/generate_review.py <workspace>/iteration-N --skill-name "<name>" --benchmark <workspace>/iteration-N/benchmark.json --wait-for-submit --auto-close-tab
```

For iteration `N > 1`, include previous iteration workspace input.

In headless environments, use static HTML export mode.
In interactive server mode, `--wait-for-submit` blocks until review is submitted
with `status=complete`, then returns control to the running agent automatically.

## Step 10) Collect feedback and iterate

Read `feedback.json` after user review.
Empty feedback means no requested changes for that eval.

Prioritize changes where user feedback is specific and where benchmark data shows clear gaps.

## Iteration quality gates

Use this exact order.

### A) Before any create/edit/evaluate action (once per engagement)

1. Ensure target `QA.txt` exists.
2. Append any missing `assets/QA.txt` questions as-is.
3. Treat this merged `QA.txt` as mandatory for all subsequent QA passes.

### B) After each feature or edit

1. Run Comprehensive QA pass #1 against current `QA.txt`.
2. Check the skill description for trigger clarity and scope control.
3. Draft and append any missing skill-specific QA questions to `QA.txt`.
4. Run Comprehensive QA pass #2 against the expanded `QA.txt`.
5. Confirm every question in the target skill root `QA.txt` is answered `yes`.
6. Confirm pass #2 shows no objective regressions and preserves original intent.
7. Confirm `agents/grader.md`, `agents/comparator.md`, and `agents/analyzer.md`
   still align with the current workflow and outputs.
8. Run feature discoverability check.
9. Run integration check for conflicting or orphaned instructions.
10. Re-run evals in `iteration-(N+1)`.

If pass #2 fails or objective fit regresses, revise and repeat section B before
presenting results.

## Stop conditions

Stop iteration when one of these is true:

- User confirms satisfaction
- Feedback is consistently empty
- Further iterations show no meaningful improvement

## Agent workflow integration

All markdown files under `agents/` are part of the test workflow:

1. `agents/grader.md` for grading run outputs after validation and QA.
2. `agents/comparator.md` for blind A/B comparison whenever paired outputs exist.
3. `agents/analyzer.md` for benchmark pattern analysis and post-comparison
   improvement guidance before user review.

This sits inside the same continuous workflow as `quick_validate`, mandatory QA,
and user review.
