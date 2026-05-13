# How to self-evaluate humanized text

Use this rubric when generating or reviewing text that has been processed by the text-humanizer skill.

## The Output Checklist

Before finalizing humanized text, run this checklist:

- [ ] **Has `scripts/detect_ai.py` been run?** The text must score < 50% AI probability output from the Open-Detector model.
- [ ] Does the text contain three sequential sentences of the same length? (If yes, break one up).
- [ ] Does a paragraph end with a tidy, single-line positive summary? (If yes, change the ending to a factual detail or an open thought).
- [ ] Are there dramatic em-dashes leading to a point? (If yes, delete them).
- [ ] Does the text explain metaphors or figures of speech? (If yes, trust the reader and delete the explanation).
- [ ] Are there conjunctive adverbs like "Additionally", "However", or "Furthermore"? (If yes, see if the sentence works without them; usually, a simple "And/But" is stronger).
- [ ] Are there lists of exactly three items ("A, B, and C")? (If yes, change to two or four items).

## Voice Quality Scoring (1-10)

Grade the text across these 5 dimensions. A score below 35/50 fails.

| Dimension | Evaluation | Score |
|---|---|---|
| **Directness** | Does it state facts directly (10) or circle around them (1)? | /10 |
| **Rhythm** | Is sentence length varied (10) or perfectly uniform (1)? | /10 |
| **Respect** | Does it trust the reader's intelligence (10) or over-explain (1)? | /10 |
| **Authenticity** | Does it sound like a specific human talking (10) or a corporate press release (1)? | /10 |
| **Economy** | Can more words be cut without losing meaning (10) or is there heavy fluff (1)? | /10 |

**Thresholds:**
- **45-50:** Excellent. No discernible AI footprint.
- **35-44:** Good, but has room for editing tightening.
- **Below 35:** Fails. Needs a fresh rewrite.

The 35/50 passing floor is calibrated so that a text scoring below it fails at least two of the five dimensions, which correlates with text that still reads as AI-generated to a careful human reviewer even when the detector score passes.
