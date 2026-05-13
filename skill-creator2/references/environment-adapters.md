# Environment Adapters

The logical workflow stays the same across environments.
Adjust execution mechanics by environment.

## Claude Code (full feature path)

- Subagents available
- Parallel with-skill and baseline runs supported
- Grading, aggregation, viewer generation, and blind comparison supported
- Description optimization loop supported

## Claude.ai

- No subagents
- Run test cases sequentially
- Skip baseline comparison if independent baseline runs are not feasible
- If browser server cannot be opened, present outputs inline and collect feedback in chat
- Blind comparison is usually unavailable
- Package skill with local Python if filesystem access exists

For existing-skill updates in Claude.ai:

1. Preserve original skill name and directory naming.
2. Copy installed skill to writable location (for example `/tmp/<skill-name>/`) before editing.
3. Package from writable copy.

## Cowork or headless environments

- Subagents may be available, but browser display often is not
- Use static review output mode in `generate_review.py`
- Read downloaded `feedback.json` from filesystem
- Keep full eval loop and QA gates, even when presentation mechanism differs

## Failure handling

If tooling/environment constraints block part of the loop:

1. State the blocked step clearly.
2. Use nearest equivalent fallback path.
3. Keep evidence artifacts (`grading.json`, `benchmark.json`, `feedback.json`) consistent.
