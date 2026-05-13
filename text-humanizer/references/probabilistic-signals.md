# Probabilistic Signals: What Detectors Actually Measure

Understanding what AI detectors measure explains *why* each humanization rule works.
Modern detectors use a hybrid ensemble: probabilistic models, supervised classifiers,
and stylometric analyses. This reference covers all three layers.

---

## Layer 1 — Probabilistic: Perplexity and Entropy

**What it is:** Perplexity measures how "surprised" a language model is by each token.
AI text scores low perplexity because the model selects high-probability tokens during
generation. Human writing scores higher perplexity because it is shaped by idiosyncratic
experience, not statistical likelihood.

**Detection tools that use it:** GPTZero, DetectGPT — they calculate probability curvature.
If the text sits at the peak of an LLM's distribution, it is flagged synthetic.

**Humanization implication:** Vocabulary substitution is not cosmetic. Replacing
"meticulous" → "thorough", "utilize" → "use", "ensure" → "make sure" shifts token
probability into regions the model is less certain about. Every substitution adds
perplexity.

Prefer target words:
- thorough (not meticulous)
- use, apply (not utilize, leverage)
- make sure, check (not ensure)
- important, central (not crucial, pivotal)
- look into (not delve into)
- show (not showcase, demonstrate)
- help, build (not foster, garner)

---

## Layer 2 — Probabilistic: Burstiness

**What it is:** Burstiness is the variance in sentence length and complexity across a
document. Human prose is rhythmically uneven: short punchy sentences followed by long
subordinating ones. AI defaults to a medium-length bias — helpful, clear, monotonous.

**How it is detected:** Detectors measure the standard deviation of sentence lengths
and the entropy of part-of-speech (POS) transitions. Low standard deviation = low
burstiness = AI signal.

**Humanization implication:** The sentence-length variation rule in SKILL.md is not
a stylistic preference — it directly raises the burstiness score. The target is a high
standard deviation across sentence lengths in a paragraph.

Concrete technique: after every run of three sentences averaging 20+ words, place one
sentence of 5-8 words. Fragment sentences are acceptable ("That part matters.").

---

## Layer 3 — Supervised Classifier: SHAP-Flagged Patterns

Supervised classifiers (RoBERTa, Turnitin) are trained on paired human/AI datasets.
They identify non-linear feature patterns invisible to simple rules.
SHAP analysis has identified specific token-level tells:

**Transition phrase overload (overt conjunctive framing):**
AI uses explicit transitions to maintain surface coherence. Classifiers flag these
because human writing relies on implicit discourse scaffolding instead.

Phrases with high AI-classification SHAP weight:
- "In conclusion," / "To summarize,"
- "It is important to note that"
- "It is worth noting that"
- "Furthermore," / "Moreover," (when overused)
- "This highlights the importance of"
- "It should be noted that"
- "This underscores the need for"
- "Needless to say,"

**Humanization implication:** Remove or rewrite these. Replace them with implicit
transitions: end one sentence with the premise, start the next with the consequence.
Let the logic carry the connection.

---

## Layer 4 — Stylometric: Nominal Loading and POS Balance

**What it is:** AI text over-produces nouns and adjectives (nominal loading) and
under-produces pronouns, auxiliary verbs, and functional morphology.

| POS Feature | AI Tendency | Human Tendency |
|---|---|---|
| Nouns + adjectives | Overloaded (information-dense) | Balanced with function words |
| Pronouns | Underused | Maintains referential chains (he, they, it, we) |
| Auxiliary verbs | Rare | Common (might have been, should have gone) |
| Contractions | Absent | Present in informal/moderate registers |
| Adverbial modifiers | Generic | Specific and contextually placed |

**Humanization implication:** After rewriting for vocabulary and sentence length,
check noun density. If more than 60% of content words are nouns or adjectives, rewrite
sentences to use pronouns for referential chains and auxiliary verbs for shading meaning.

Use contractions where register allows: "don't" not "do not", "it's" not "it is",
"we're" not "we are".

---

## Layer 5 — Stylometric: Lexical Density and Discourse Scaffolding

**Lexical density** is the ratio of content words to total words. AI text maintains
uniformly high density regardless of reader context. Humans vary it — casual sentences
have lower density, technical explanations spike higher.

**Humanization implication:** Introduce lower-density connector sentences between
high-density technical sentences. "That is the key problem." or "Here is why it matters."
These drop density momentarily and produce the variance detectors expect from humans.

**Discourse scaffolding** is how writing builds implicit logical structure through
shared context rather than explicit markers. AI uses overt markers. Humans leave
referential gaps that readers bridge using context.

**Humanization implication:** After removing "Furthermore," and "It is important to
note that," do not replace them with another explicit connector. Trust the paragraph
structure to carry the relationship.

---

## Summary: What to target in order

1. Vocabulary — highest perplexity gain per word changed.
2. Sentence length variance — directly raises burstiness score.
3. Transition phrase removal — high SHAP weight in supervised classifiers.
4. Pronoun and auxiliary injection — corrects nominal loading and POS balance.
5. Lexical density variation — adds structural naturalness across paragraphs.
