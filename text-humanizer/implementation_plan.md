# Text-Humanizer Skill: QA Audit & Improvement Plan

## QA Pass Results — Against QA.txt (37 questions)

| # | Question | Pass? | Finding |
|---|---|---|---|
| 1 | Description specific with trigger phrases? | PASS | Good |
| 2 | Description states what AND when? | PASS | Good |
| 3 | SKILL.md under 5000 words? | PASS | 64 lines |
| 4 | Additional details in separate references? | PASS | 5 reference files |
| 5 | Avoids time-sensitive info? | PASS | Good |
| 6 | Consistent terminology? | PARTIAL | Pattern numbers skip: goes 18→25 in [language-style-patterns.md](file:///c:/Users/philip/sauce/skill-making-factory/text-humanizer/references/language-style-patterns.md) (patterns 19–24 not labeled) |
| 7 | Concrete examples? | PARTIAL | SKILL.md example exists but is duplicated (`## Example Interaction Pattern` heading appears twice) |
| 8 | File refs one level deep? | **FAIL** | Script path in step 6 uses `~/.claude/skills/...` — hardcoded absolute path that breaks on all non-Claude-Code installs |
| 9 | Progressive disclosure appropriate? | PARTIAL | SKILL.md tells Claude to read all 5 reference files before processing any text — forces eager up-front loading; should load references on-demand per step |
| 10 | Workflows with clear sequential steps? | PASS | 8-step numbered process |
| 11 | Scripts solve problems directly? | PASS | [detect_ai.py](file:///c:/Users/philip/sauce/skill-making-factory/text-humanizer/scripts/detect_ai.py) is self-contained |
| 12 | Explicit error handling? | PARTIAL | [detect_ai.py](file:///c:/Users/philip/sauce/skill-making-factory/text-humanizer/scripts/detect_ai.py) handles missing file/empty text, but no guidance in SKILL.md on what to do if model download fails mid-session (model is ~350MB) |
| 13 | Constants justified? | **FAIL** | 50% threshold cited in SKILL.md but never explained. [eval-loop.md](file:///c:/Users/philip/sauce/skill-making-factory/text-humanizer/references/eval-loop.md) threshold of 35/50 voice score also not explained |
| 14 | Required packages listed and verified? | PARTIAL | Packages listed in SKILL.md Prerequisites but no verification step (no `pip show` check before running) |
| 15 | Scripts include clear documentation? | PARTIAL | [detect_ai.py](file:///c:/Users/philip/sauce/skill-making-factory/text-humanizer/scripts/detect_ai.py) has minimal inline comments; no docstring on [main()](file:///c:/Users/philip/sauce/skill-making-factory/text-humanizer/scripts/detect_ai.py#7-70) |
| 16 | Forward slashes for paths? | **FAIL** | Script path in step 6: `~/.claude/skills/text-humanizer/scripts/detect_ai.py` uses forward slash but embeds a platform-specific home-dir shorthand that breaks on Windows |
| 17 | Validation/verification steps? | PASS | detect_ai.py + voice quality rubric |
| 18 | Feedback loops for quality? | PASS | Step 7 re-runs script; QA rubric loops |
| 19 | YAML frontmatter uses `---`? | PASS | |
| 20 | Description under 1024 characters? | PASS | ~360 chars |
| 21 | Frontmatter avoids XML angle brackets? | PASS | |
| 22 | Skill name free of reserved prefixes? | PASS | `text-humanizer` |
| 23 | Folder named in kebab-case? | PASS | |
| 24 | No README.md? | PASS | |
| 25 | Description has negative trigger phrases? | PASS | "Do not use for..." present |
| 26 | Tested for negative triggering? | **FAIL** | No record of negative trigger smoke test |
| 27 | Critical instructions near top? | PARTIAL | Prerequisites buried below persona and goal sections |
| 28 | Explicit/deterministic steps? | PARTIAL | Step 5 ("Add Soul") is vague — "ensure rhythm varies" is not actionable |
| 29 | Works alongside other skills? | PASS | No conflicts |
| 30 | MCP tool names verified? | N/A | No MCP tools used |
| 31 | MCP failure instructions? | N/A | No MCP tools used |
| 32 | No emoji in documentation? | PASS | None found |
| 33 | Skill's own content follows its rules (dogfood)? | **FAIL** | [communication-patterns.md](file:///c:/Users/philip/sauce/skill-making-factory/text-humanizer/references/communication-patterns.md) line 3 contains "Removing them is crucial" — uses the banned word "crucial" from rule 7 |
| 34 | Verifies rules from humanizer-main? | PASS | |
| 35 | Verifies rules from op7418-Humanizer-zh? | PASS | Chinese equivalents present |
| 36 | Includes Open-Detector principles? | PASS | |

---

## Missing Baseline QA Items (in assets/QA.txt but not in skill's QA.txt)

Two items from the baseline are missing from the skill's [QA.txt](file:///c:/Users/philip/sauce/skill-making-factory/text-humanizer/QA.txt):
- `does the skill contain no emoji in the documentations?`
- `Does the skill's own generated content follow the rules it teaches (dogfood check)?`

---

## Improvement Brief

### CRITICAL Issues (must fix)

**C1 — Hardcoded script path** ([SKILL.md](file:///C:/Users/philip/.gemini/antigravity/skills/skill-creator/SKILL.md) step 6)
The path `~/.claude/skills/text-humanizer/scripts/detect_ai.py` is hardcoded to a Claude-specific install location. On Windows or any non-standard install this fails silently. The script should be referenced relative to the skill root, with an instruction to resolve the absolute path at runtime.
- **Fix:** Change the command to use a relative reference and add a note to resolve the path.

**C2 — Duplicate section heading** ([SKILL.md](file:///C:/Users/philip/.gemini/antigravity/skills/skill-creator/SKILL.md))
`## Example Interaction Pattern` appears twice on consecutive lines (lines 43–44), which breaks rendering and signals a copy-paste error.
- **Fix:** Delete one occurrence.

**C3 — Dogfood failure** ([references/communication-patterns.md](file:///c:/Users/philip/sauce/skill-making-factory/text-humanizer/references/communication-patterns.md) line 3)
The word "crucial" appears in skill documentation that explicitly bans "crucial" from AI-generated text (rule 7 in [language-style-patterns.md](file:///c:/Users/philip/sauce/skill-making-factory/text-humanizer/references/language-style-patterns.md)).
- **Fix:** Replace "crucial" with "essential" or rewrite the sentence.

**C4 — Missing baseline QA items** ([QA.txt](file:///c:/Users/philip/sauce/skill-making-factory/text-humanizer/QA.txt))
Two baseline questions are absent from the skill's QA file.
- **Fix:** Append both missing questions.

### HIGH Issues (significant impact)

**H1 — Eager reference loading** ([SKILL.md](file:///C:/Users/philip/.gemini/antigravity/skills/skill-creator/SKILL.md) step in Progressive Disclosure Links)
The bottom section instructs reading all 5 reference files before processing any text, even for short text. This front-loads a lot of context on every invocation. Each step already links to the right reference.
- **Fix:** Change the footer to a discovery table (reference name → when to load it) rather than an "always load all" instruction.

**H2 — Step 5 ("Add Soul") is vague** ([SKILL.md](file:///C:/Users/philip/.gemini/antigravity/skills/skill-creator/SKILL.md))
"Ensure the rhythm varies and the perspective isn't entirely sterile" gives Claude nothing concrete to act on.
- **Fix:** Replace with 3 specific, actionable techniques from eval-loop.md (vary sentence length, avoid three-item lists, end on a concrete fact not a summary platitude).

**H3 — Prerequisite dependency check missing** ([SKILL.md](file:///C:/Users/philip/.gemini/antigravity/skills/skill-creator/SKILL.md))
Prerequisites section lists packages but provides no check step. During long sessions the model download can fail partway through.
- **Fix:** Prefix the "Objective Script Check" step with a check command: `pip show torch transformers || echo "Not installed"`.

**H4 — 50% threshold not explained** ([SKILL.md](file:///C:/Users/philip/.gemini/antigravity/skills/skill-creator/SKILL.md) + [eval-loop.md](file:///c:/Users/philip/sauce/skill-making-factory/text-humanizer/references/eval-loop.md))
The 50% AI score threshold in SKILL.md and the 35/50 voice score threshold in eval-loop.md appear without justification.
- **Fix:** Add 1-sentence rationale for each threshold in its respective file.

### MEDIUM Issues (polish and consistency)

**M1 — Pattern numbering gap** ([references/language-style-patterns.md](file:///c:/Users/philip/sauce/skill-making-factory/text-humanizer/references/language-style-patterns.md))
The file covers patterns 7–18 and 25. Patterns 19–24 are in [communication-patterns.md](file:///c:/Users/philip/sauce/skill-making-factory/text-humanizer/references/communication-patterns.md) but [language-style-patterns.md](file:///c:/Users/philip/sauce/skill-making-factory/text-humanizer/references/language-style-patterns.md) jumps directly from 18 to 25, creating a confusing non-sequential gap.
- **Fix:** Renumber pattern 25 to 19, or add a comment noting the cross-file gap.

**M2 — Prerequisites hidden below persona** ([SKILL.md](file:///C:/Users/philip/.gemini/antigravity/skills/skill-creator/SKILL.md))
The Prerequisites pip install block is buried under the persona and goal sections. If packages are missing, failure will happen mid-task.
- **Fix:** Move Prerequisites to be the first section after the title.

**M3 — No negative trigger smoke-test record**
QA item 26 requires evidence that the skill was tested not to trigger on unrelated queries. No such record exists.
- **Fix:** Add a `notes/trigger-test.md` file with two representative negative prompts and their outcomes.

**M4 — detect_ai.py truncation warning missing**
The script silently truncates inputs longer than 512 tokens, which is below even a single typical paragraph of dense text. Long documents get silently evaluated on only their first ~380 words.
- **Fix:** Add an explicit warning to stderr when the input exceeds 512 tokens.

---

## Proposed Fix Set

All critical and high issues will be fixed in one pass. Medium issues will be addressed in the same pass since they have no conflict risk.

### Files to edit
- [SKILL.md](file:///C:/Users/philip/.gemini/antigravity/skills/skill-creator/SKILL.md) — fix path, duplicate heading, vague step 5, prerequisites position, add dependency check, explain 50% threshold, convert footer to reference table
- [references/communication-patterns.md](file:///c:/Users/philip/sauce/skill-making-factory/text-humanizer/references/communication-patterns.md) — fix "crucial" dogfood failure
- [references/language-style-patterns.md](file:///c:/Users/philip/sauce/skill-making-factory/text-humanizer/references/language-style-patterns.md) — fix numbering gap, add comment
- [references/eval-loop.md](file:///c:/Users/philip/sauce/skill-making-factory/text-humanizer/references/eval-loop.md) — explain 35/50 threshold
- [scripts/detect_ai.py](file:///c:/Users/philip/sauce/skill-making-factory/text-humanizer/scripts/detect_ai.py) — add 512-token truncation warning
- [QA.txt](file:///c:/Users/philip/sauce/skill-making-factory/text-humanizer/QA.txt) — append 2 missing baseline items

### Files to create
- `notes/trigger-test.md` — negative trigger smoke test record

## Verification Plan

QA pass 1: Answer all 37 questions in QA.txt post-edit. Every answer must be "yes".
QA pass 2: Check description quality and run expanded QA against any new items added during editing.
