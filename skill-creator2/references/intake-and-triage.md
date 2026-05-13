# Intake and Triage

Read this file at the start of every skill-creator engagement.

## 1) Triage first

Classify the user request before writing or editing anything.

| Situation | Action |
|---|---|
| Brand new skill | Run full creation flow |
| Existing skill, clear requested changes | Run scoped edit flow |
| Existing skill, vague request (no specs) | Run QA-first intake flow |
| QA or benchmarking only | Evaluate as-is before edits |
| User asks to review outputs before more edits | Generate review viewer and gather user feedback first |
| User asks for objective A/B comparison | Run blind comparison workflow |
| User asks to optimize triggering | Run description optimization workflow |
| User asks to package/install | Run packaging workflow |

## 2) QA-first intake flow for vague improvement requests

Use this path for prompts like:

- "improve this skill"
- "refine this one"
- "make this better"
- "use skill-creator to refine this skill"

Do this sequence in order.

1. Locate target skill path and parse current frontmatter (`name`, `description`).
2. Snapshot baseline before any edits.
3. Ensure target `QA.txt` exists.
4. Merge missing baseline questions from `assets/QA.txt` into target `QA.txt` as-is.
5. Run comprehensive QA pass against target `QA.txt` to establish current-state findings.
6. Produce an improvement brief with:
   - Top issues (highest impact first)
   - Impact if fixed
   - Risk and regression surface
   - Confidence level
7. Present 2-3 concrete improvement options.
8. Recommend one option and proceed if the user gives minimal direction.

Do not block on broad requirement interviews before this QA-first pass.

## 3) Mandatory QA bootstrap for all paths

Before creating, editing, or evaluating any skill, complete this once per engagement:

1. Ensure `<skill-root>/QA.txt` exists.
2. Append missing questions from `assets/QA.txt` as-is (no rewrites).
3. Confirm this merged `QA.txt` is now the active checklist for the loop.

This bootstrap is required for new-skill creation, existing-skill edits, and
evaluation-only requests.

Use highest available reasoning effort by default for design-critical decisions
that affect long-term user effort. Only reduce reasoning depth when the user
explicitly prefers speed.

## 4) Capture intent (all paths)

Extract intent from conversation history first. Then fill gaps.

Minimum intent fields:

1. What should the target skill enable Claude to do?
2. When should the target skill trigger?
3. What output shape or artifact is expected?
4. Should testing be qualitative only, quantitative only, or both?
5. Which professional standard or workflow should the skill follow?

## 5) Interview and research

Before writing or changing logic:

- Research official docs, frameworks, or standards relevant to the domain.
- **For any skill targeting a hobbyist or practitioner community**, search the
  social platforms where that community is active to surface real pain points,
  common failure modes, and current best practices that official docs omit.
  Use the following platform search strategy:

  | Community type | Platforms to search |
  |---|---|
  | Android root / ROM modding | XDA Forums (`xdaforums.com`), r/Magisk, r/KernelSU, r/androidroot, GitHub topic search |
  | Game modding | NexusMods, r/modding, CurseForge forums, relevant subreddits |
  | Hardware / embedded / IoT | EEVblog forums, r/embedded, r/arduino, Hackaday community |
  | Homelab / self-hosted | r/selfhosted, r/homelab, Linuxserver.io forums, Proxmox forums |
  | Creative tools (audio, video, 3D) | KVR Audio forum, Reaper forums, BlenderArtists, r/gamedev |
  | Security / reverse engineering | r/netsec, Hack The Box forums, GitHub topic search, DEF CON discord |
  | General hobbyist / maker | Instructables, Hackaday, r/DIY, Reddit topic subreddits |

  When a skill does not fit a row above, identify the 2-3 most active community
  platforms for that domain before proceeding. Ask the user if unsure.

  Research goal: find the top 3-5 pain points, recurring failure modes, and
  current-ecosystem gaps that affect practitioners but are absent from official
  documentation. Record findings in `references/design-log.md` under a
  "Community research" heading before drafting skill content.

- Ask focused questions for missing high-impact constraints.
- Clarify edge cases, dependencies, I/O formats, and failure handling.
- Perform a **source asset audit** across all provided folders before drafting:
  - List all non-documentation files (code, configs, datasets, binaries).
  - For each executable or runnable file, decide whether to adapt it into `scripts/`. If skipped, record the rationale in `references/design-log.md`.
- Distinguish **declarative vs. operational knowledge**:
  - Declarative = rules, patterns, checklists, guidelines -> store in `references/`.
  - Operational = runnable scripts, APIs, pipelines, data tools -> adapt into `scripts/` with clear CLI entrypoints.
  - When the user requests "use all knowledge," treat both categories as mandatory inputs to the skill.

## 6) Prompt formulation requirement

Before writing the target `SKILL.md` body, draft 3 candidate core prompt formulations.
Each candidate must use a different structure from
`references/prompt-engineering-best-practices.md`.

Suggested set:

1. Direct role/context framing
2. Chained workflow prompt
3. Few-shot pattern

Pick the strongest candidate, explain why, and record decision in
`references/design-log.md`.

## 7) Writing constraints for target skills

When writing prompt blocks in any generated or edited skill:

- Never use emojis unless the user explicitly asks for them.
- Use `role -> context -> task -> constraints -> output format`
- Include reasoning guidance only when needed
- Include self-check patterns for evaluative outputs
- Use tags or delimiters when mixing instructions, examples, and input
- For long context, require evidence grounding before synthesis
- Surface hidden assumptions or ask for clarification instead of guessing

## 8) Deliverable from intake

Before writing edits, produce a concise intake summary:

- Selected path from triage
- Confirmed assumptions
- Improvement option selected
- What will be changed first
