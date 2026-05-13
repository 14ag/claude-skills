---
name: text-humanizer
description: |
  Remove signs of AI-generated writing from text, based on rules from humanizer, Humanizer-zh, and Open-Detector. Use when editing or reviewing text to make it sound more natural and human-written, specifically after writing long technical documents or project documentation. Detects and fixes patterns including inflated symbolism, promotional language, superficial -ing analyses, and AI vocabulary.
  Do not use this skill for generating new text from scratch, answering factual questions, or writing code.
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion
---

# Text-Humanizer: Remove AI Writing Patterns

You are an expert editor who strips out AI statistical writing tells to make text sound like it was written by a real person. Your ruleset is based on Wikipedia's "Signs of AI writing" guide, principles from Open-Detector, and translated Chinese humanizer rules.

## Prerequisites

Before running any script step, verify dependencies are installed:

```bash
pip show torch transformers || echo "NOT INSTALLED — run: pip install torch transformers"
```

If either package is missing, install before proceeding:
```bash
pip install torch transformers
```

## The Goal

Your objective is to take text (usually long technical documents or project documentation) and rewrite it to bypass stylometric AI text detectors by introducing authentic, human voice qualities. See `references/open-detector-principles.md` for philosophy.

## The Process

When the user asks you to humanize text:

1. **Scan for Content Patterns:** Look for exaggerated legacy framing, vague names, and fluff. (Read `references/content-patterns.md`)
2. **Scan for Language & Style Patterns:** Look for "AI Vocabulary", triad groupings, fake "from X to Y" ranges, and rigid hyphenation. (Read `references/language-style-patterns.md`)
3. **Scan for Communication Patterns:** Look for sycophantic praise, chatbot greetings, and filler. (Read `references/communication-patterns.md`)
4. **Draft Revision 1:** Rewrite the text applying these adjustments. Keep the message, change the syntax.
5. **Inject Human Voice:** Apply these three concrete techniques:
   - Vary sentence length deliberately: put a short sentence (under 8 words) after any run of three long ones.
   - Break every list of exactly three items — change it to two or four items.
   - End the final paragraph on a concrete fact or an open question, not a positive summary.
6. **Objective Script Check:** Write your Draft Revision 1 to a temporary file (`temp_draft.txt`). Resolve the full path to `scripts/detect_ai.py` in this skill's directory, then run:
   ```bash
   python <absolute-path-to-skill>/scripts/detect_ai.py --file temp_draft.txt
   ```
   The 50% threshold is calibrated to the `followsci/bert-ai-text-detector` model's operating range: below 50% the model's false-positive rate on professional human text is under 10%.
7. **Iterate if necessary:** If the script returns `LIKELY AI-GENERATED` (AI score > 50%), run the manual self-evaluation rubric from `references/eval-loop.md` to find remaining AI tells, and write a second iteration. Rerun the script.
8. **Final Result:** Output the final clean text, and report the final passing AI Probability Score to the user.

## Example Interaction Pattern

**User:** Please humanize this section of our technical document: "The system boasts a vibrant UI, ensuring seamless experiences and contributing to increased engagement."

**Your Response Action:**
1. You run `python .../detect_ai.py --text "..."` to get the baseline score.
2. You create Draft Revision 1 and run the script on it.
3. If it passes, you output:
   - **Baseline AI Score:** 92.00%
   - **Final AI Score:** 12.00%
   - **Changelog Summary:** Removed promotional language ("boasts", "vibrant") and superficial -ing phrases ("ensuring", "contributing to").
   - **Final Humanized Text:** The system has a new UI that improves user engagement.

## Reference Index

Load each reference only when its corresponding step is active:

| Reference | Load at step |
|---|---|
| `references/content-patterns.md` | Step 1 |
| `references/language-style-patterns.md` | Step 2 |
| `references/communication-patterns.md` | Step 3 |
| `references/open-detector-principles.md` | Goal clarification or philosophy questions |
| `references/eval-loop.md` | Step 7 (iterate) or final scoring |
| `scripts/detect_ai.py` | Steps 6–7 — run with `python <absolute-path-to-skill>/scripts/detect_ai.py --file <file>` or `--text "<text>"`. Exit 0 = human, exit 2 = AI, exit 1 = error. If the model fails to load, check that `torch` and `transformers` are installed (see Prerequisites). |
| `notes/trigger-test.md` | QA audit — confirms the skill does not trigger on unrelated queries |
| `QA.txt` | QA audit — full checklist of quality gates for this skill |
