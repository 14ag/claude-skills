# File Routing Index

Use this file to trace every non-root source file in `skill-creator` from a readable
entrypoint.

This index is a proxy router. It is intended for discoverability and QA checks.

## Reference docs

- `references/intake-and-triage.md`: intent capture, triage, QA-first intake
- `references/eval-loop.md`: eval execution, review loop, iteration gates
- `references/description-optimization.md`: trigger optimization flow
- `references/environment-adapters.md`: environment-specific execution rules
- `references/prompt-engineering-best-practices.md`: prompt construction rules
- `references/prompt-research-notes.md`: research evidence and design notes
- `references/schemas.md`: expected JSON structures

## Subagents

- `agents/grader.md`: grading instructions
- `agents/comparator.md`: blind comparison instructions
- `agents/analyzer.md`: benchmark/post-hoc analysis instructions

## Assets and review UI

- `assets/QA.txt`: baseline QA checklist source
- `assets/eval_review.html`: eval-set review/edit template
- `eval-viewer/generate_review.py`: review viewer generator
- `eval-viewer/viewer.html`: bundled review viewer UI template/runtime

## Scripts

- `scripts/run_loop.py`: iterative description optimization orchestrator
- `scripts/run_eval.py`: trigger-eval runner
- `scripts/improve_description.py`: description refinement helper
- `scripts/aggregate_benchmark.py`: benchmark aggregation utility
- `scripts/generate_report.py`: HTML optimization report generator
- `scripts/package_skill.py`: package builder
- `scripts/quick_validate.py`: structural validation utility
- `scripts/utils.py`: shared parsing/util helpers
- `scripts/__init__.py`: package marker for module execution

## Notes

- `__pycache__` files are generated artifacts and are intentionally excluded
  from routing requirements.
