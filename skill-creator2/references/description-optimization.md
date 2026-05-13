# Description Optimization

Use this after the skill workflow is functionally stable.

## Goal

Improve trigger reliability while avoiding overfitting.

## Step 1) Build trigger eval set

Create about 20 queries with balanced positives and negatives:

- Should trigger: 8-10
- Should not trigger: 8-10

Use realistic, user-like prompts with concrete context.
Prefer near-miss negatives over obviously unrelated negatives.

Save format:

```json
[
  {"query": "...", "should_trigger": true},
  {"query": "...", "should_trigger": false}
]
```

## Step 2) User review of eval set

Use `assets/eval_review.html` to review/edit query quality with the user.
Replace placeholders and export final eval JSON.

## Step 3) Run optimization loop

Run:

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <one-shot|reasoning|balanced> \
  --max-iterations 5 \
  --verbose
```

Monitor progress and summarize iteration scores.

Use the same tier label consistently across the full optimization run.

## Step 4) Apply best result

Apply `best_description` from loop output to target `SKILL.md` frontmatter.
Report before/after description and score deltas.

## Hard requirements

A good description should:

- describe concrete user situations, not only capabilities
- include at least one realistic trigger phrase
- separate trigger scope from adjacent skills
- remain under platform limits

Use prompt-engineering guidance from
`references/prompt-engineering-best-practices.md` when refining wording.
