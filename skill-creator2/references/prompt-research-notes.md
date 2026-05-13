# Prompt Research Notes

Working notes for the March 24, 2026 update that strengthened `skill-creator`
with prompt-engineering guidance.

## Sources consulted

- Anthropic prompt engineering docs:
  `docs.anthropic.com/.../claude-prompting-best-practices`
- Anthropic prompt chaining docs:
  `docs.anthropic.com/.../prompt-engineering/chain-prompts`
- OpenAI prompting guide:
  `platform.openai.com/docs/guides/prompting`
- DAIR Prompt Engineering Guide:
  `promptingguide.ai/techniques/prompt_chaining`
- LangSmith docs:
  `docs.smith.langchain.com/`
- Marketplace/library snapshots used only as secondary signals:
  FlowGPT, PromptHero, AIPRM

## Stable patterns that repeated across sources

### Structural patterns

- Strong prompts consistently separate role, context, task, constraints, and
  output format.
- The browser pass reinforced that prompts mixing instructions, context,
  examples, and variable inputs are more robust when those parts are wrapped in
  explicit XML-style tags or delimiters.
- Complex tasks are more reliable when split into prompt chains or explicit
  numbered subtasks instead of one dense instruction block.
- High-performing templates often keep examples in a short, scan-friendly block
  rather than embedding them throughout the instructions.

### Instruction clarity techniques

- Define the audience, goal, and success criteria up front.
- Prefer positive directives ("write in prose paragraphs") over only negative
  prohibitions ("do not use bullets").
- Name ambiguities directly: inputs, edge cases, missing data behavior, and
  escalation conditions.
- If user input carries unstated assumptions, strong prompts either ask a
  follow-up question or run an assumption-check pass before committing.
- Use explicit delimiters or XML-style tags when passing multiple artifacts or
  when reasoning/output must be separated cleanly.

### Evaluation and QA patterns

- Prompt systems improve faster when every change is paired with an eval or
  review pass.
- Self-check instructions are useful when the task has objective criteria:
  "before finishing, verify against these checks".
- Human review remains important for subjective outputs, but objective
  assertions should be stated in a way a grader can test deterministically.
- On long-context tasks, a quote-first step ("pull the relevant evidence
  before synthesizing") showed up as a reliable grounding pattern.

### Reasoning patterns

- Reasoning should be elicited selectively, not reflexively.
- For genuinely multi-step tasks, prompting the model to think through the work
  or using chained prompts improves traceability and accuracy.
- For simpler tasks, over-prescribing reasoning can add noise, latency, or
  brittle behavior.

### Output formatting patterns

- Reliable prompts specify the final artifact shape: schema, section order,
  tone, length bounds, and file expectations.
- Examples and tags help when the output must match a strict structure.
- Prompt wording should mirror the desired response style.
- For long prompts, source material first and the actual question near the end
  is a recurring layout pattern.

## Marketplace observations

- Marketplace prompts often succeed by being explicit about persona, goals,
  audience, and output structure.
- Community hubs surface recurring "assumption checker", "self-checking", and
  "role prompting" patterns, which suggests these are durable prompt families
  rather than one-off tricks.
- The weaker prompts tend to be keyword-heavy but underspecified on constraints,
  failure handling, and verification.
- Several marketplaces hide full prompt text, so they were useful mainly for
  high-level pattern spotting, not as primary evidence.

## Playwright pass notes

- Anthropic docs were the strongest browser-accessible source for concrete
  guidance. New additions from that pass: XML tags, long-context ordering,
  quote-first grounding, matching prompt style to output style, and softer
  trigger phrasing to avoid overfiring.
- LangChain Hub was useful for spotting live prompt categories such as
  self-checking, role prompting, few-shot, and assumption checking.
- OpenAI examples were blocked by a browser verification page during the
  Playwright pass.
- PromptHero was blocked by Cloudflare during the Playwright pass.
- The Wharton prompt-library URL returned a not-found page during the Playwright
  pass.

## Sites skipped or treated as low-confidence

- The Wharton prompt library path did not surface a stable, directly accessible
  library page during this pass.
- SnackPrompt and God of Prompt did not provide strong, directly citable prompt
  library material in the accessible results.
- AIPRM and some marketplace pages expose only previews unless signed in, so
  they were treated as secondary signals.
