# Prompt Engineering Best Practices

Read this file before writing or revising prompt text inside any skill. Use it
to make prompt instructions deliberate, testable, and easy for the model to
follow.

## Role + Context framing

Open important prompts by orienting the model before you ask it to act.

- Start with the role the model should play only when that role changes how it
  should reason, prioritize, or communicate.
- Add the local context that affects execution: user goal, audience, source
  materials, environment limits, and what success looks like.
- Put the decisive context near the start of the prompt so it is hard to miss.

Preferred pattern:

```markdown
Role: You are a careful release engineer.
Context: You are updating an existing skill in a writable workspace. Preserve
current features, keep the frontmatter valid, and document any environment
limits.
```

## Task decomposition

Break complex work into explicit steps instead of one overloaded paragraph.

- Use numbered steps when the task has ordering, dependencies, or checkpoints.
- Give each step a single clear objective.
- Split multi-phase work into chains when one step's output feeds the next.
- Name decision points, fallback paths, and "stop and ask" conditions.

Preferred pattern:

```markdown
1. Read the existing files and summarize the current workflow.
2. Draft three candidate prompt structures for the core task.
3. Choose the strongest structure and explain why it fits.
4. Write the final prompt text and run the quality checklist.
```

## Constraint specification

State the rules that bound the work so the model does not guess.

- Name what must be included.
- Name what must be excluded.
- Say how to handle missing inputs, ambiguous requirements, and risky actions.
- If hidden assumptions could change the result, tell the model to surface them
  or ask a focused follow-up question instead of guessing.
- Distinguish hard constraints from preferences.
- Prefer concrete language over vague terms like "good", "clean", or
  "reasonable" without criteria.

Preferred pattern:

```markdown
Constraints:
- Preserve all existing workflow stages.
- Do not rename the skill.
- If a source is inaccessible, note that and continue with the remaining
  sources.
- Ask before any destructive or hard-to-reverse action.
```

## Output format enforcement

Define the final shape of the response or artifact explicitly.

- Specify section order, schema, headings, file names, and length limits.
- If a structured format matters, show the exact template.
- Keep examples short and representative.
- If the prompt mixes instructions, context, examples, and user inputs, wrap
  them in clear XML-style tags or other unambiguous delimiters.
- Match your prompt style to the desired output style when possible. For
  example, prompts written in clean prose are more likely to yield clean prose.

Preferred pattern:

```markdown
Output format:
- Create `references/design-log.md`
- Return a short summary with:
  1. What changed
  2. What was verified
  3. Any remaining blockers
```

## Chain-of-thought elicitation

Use reasoning instructions only when the task benefits from visible or explicit
intermediate thinking.

- For multi-step analysis, evaluation, debugging, planning, or tradeoff-heavy
  decisions, ask the model to think through the work before finalizing.
- For simple transformations, skip extra reasoning instructions and keep the
  prompt direct.
- When you need separation between reasoning and answer, ask for labeled
  sections or tagged intermediate outputs.
- Prefer prompt chains when the reasoning naturally breaks into distinct phases.
- Prefer light guidance like "reason through the tradeoffs" over brittle,
  hand-written reasoning scripts unless a fixed sequence is essential.

Preferred pattern:

```markdown
Reasoning:
- Think through the tradeoffs before choosing a prompt structure.
- Keep intermediate reasoning concise and focused on decisions that affect the
  final result.
- Then produce the final prompt and the rationale separately.
```

## Self-evaluation patterns

Add a self-check when the output can be verified against objective criteria.

- Ask the model to review its work against a short checklist before returning.
- Use concrete checks tied to the task, not generic "make it better" language.
- Place the self-check after the main task instructions so it validates the
  finished work.
- For subjective tasks, use the self-check to verify constraints and coverage,
  not taste.
- For long-context tasks, ask the model to quote or point to the relevant
  evidence before synthesizing, grading, or making a recommendation.

Preferred pattern:

```markdown
Before you finish, verify that:
- every required section is present
- the output format matches the requested template
- edge cases and failure paths are addressed
```

## Few-shot example patterns

Examples are useful when the desired structure or judgment style is hard to
describe cleanly.

- Use 2-5 concise examples when format, tone, or classification boundaries are
  easy to learn from demonstration.
- Make examples diverse enough to cover edge cases.
- Keep the example format identical to the expected output format.
- When examples include reasoning, keep the reasoning format consistent and
  clearly separated from the final answer.
- Avoid stale or conflicting examples; bad examples teach the wrong habit.

Preferred pattern:

```markdown
Example
Input: User wants a benchmark-only pass for an existing skill.
Output: Skip drafting changes, evaluate the current skill first, then recommend
revisions based on benchmark results.
```

## Anti-patterns to avoid

- Vague instructions that assume shared context the model does not have.
- "Kitchen sink" prompts that mix multiple goals without sequencing them.
- Output requests that imply a format but never define one.
- Overly broad trigger descriptions that name capabilities but not situations.
- Forcing chain-of-thought on trivial tasks where direct execution is clearer.
- Aggressive trigger language that causes tools, skills, or workflows to
  overfire when normal guidance would be enough.
- Relying on examples alone when constraints or failure handling should be
  stated explicitly.
- Asking for self-review without giving concrete criteria to check.

## Long-context packaging

When the prompt includes large documents, transcripts, or multiple artifacts:

- Put the long source material before the request and final task.
- Place the actual question near the end so it is easy for the model to anchor
  on the task after reading the context.
- Use tags like `<documents>`, `<document>`, `<instructions>`, and `<input>` so
  the model can distinguish source material from directives.
- Ask for quote extraction or evidence selection before synthesis when factual
  grounding matters.

## Quick authoring checklist

Before finalizing prompt text inside a skill, verify:

- the role is necessary and not decorative
- the context names the real operating conditions
- the task is decomposed into clear steps if it is multi-stage
- constraints cover exclusions and edge cases
- the output format is explicit
- the prompt uses tags or delimiters when it mixes multiple content types
- reasoning guidance appears only where the task truly needs it
- a self-check exists when the output can be judged against clear criteria
- long-context tasks ground claims in quoted or clearly referenced evidence
- hidden assumptions are surfaced instead of guessed
