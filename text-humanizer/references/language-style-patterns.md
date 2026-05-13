# Language, Grammar, and Style Patterns to Humanize

These patterns encompass word choices, sentence structures, and formatting quirks typical of statistical text generation. Humanizing these requires breaking the algorithmic rhythm and formatting.

## 7. Overused "AI Vocabulary" Words
**English words to watch:** Additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract noun), pivotal, showcase, tapestry (abstract noun), testament, underscore (verb), valuable, vibrant
**Chinese words to watch:** 此外、与……保持一致、至关重要、深入探讨、强调、持久的、增强、培养、获得、突出（动词）、相互作用、复杂/复杂性、关键（形容词）、格局（抽象名词）、关键性的、展示、织锦（抽象名词）、证明、强调（动词）、宝贵的、充满活力的

**Problem:** These words appear far more frequently in post-2023 text. They often co-occur, identifying the text instantly as AI-generated.

**Humanization Strategy:** Replace them with simpler, more direct synonyms. Prefer concrete nouns over abstract ones like "landscape" or "tapestry".

## 8. Avoidance of "is"/"are" (Copula Avoidance)
**English words to watch:** serves as/stands as/marks/represents [a], boasts/features/offers [a]
**Chinese words to watch:** 作为/代表/标志着/充当 [一个]、拥有/设有/提供 [一个]

**Problem:** LLMs substitute elaborate, formal verbs for simple 'to be' and 'to have' verbs.

**Humanization Strategy:** Use "is", "are", "has", "have" (是, 有). Simple is better.

## 9. Negative Parallelisms
**Problem:** Constructions like "Not only X, but Y" or "It's not just about X, it's Y" (不仅仅是……而是……) are overused formulas.
**Humanization Strategy:** State the point directly without the negative contrast setup.

## 10. Rule of Three Overuse
**Problem:** LLMs constantly force ideas into groups of three (A, B, and C) to appear comprehensive and balanced.
**Humanization Strategy:** Use two items, or four items. Break the triad pattern.

## 11. Elegant Variation (Synonym Cycling)
**Problem:** AI language models have repetition-penalty constraints causing excessive synonym substitution (e.g., protagonist... main character... central figure... hero) rather than just repeating the noun or using a pronoun.
**Humanization Strategy:** Repeat the standard noun or use simple pronouns. 

## 12. False Ranges
**Problem:** LLMs use "from X to Y" (从……到……) constructions rhetorically, where X and Y aren't actually on a meaningful scale (e.g., "from the Big Bang to dark matter").
**Humanization Strategy:** Just list the items, or define the actual spectrum accurately.

## 13. Em Dash Overuse
**Problem:** LLMs use em dashes (—) excessively to sound punchy and dynamic.
**Humanization Strategy:** Replace most em dashes with commas or periods.

## 14. Overuse of Boldface
**Problem:** AI chatbots emphasize noun phrases mechanically in boldface.
**Humanization Strategy:** Remove bold formatting unless it's a strict definition list.

## 15. Inline-Header Vertical Lists
**Problem:** AI outputs lists where items start with bolded headers followed by colons (e.g., "- **Performance:** It is faster.").
**Humanization Strategy:** Convert these lists to prose paragraphs, or remove the redundant bold headers.

## 16. Title Case in Headings (English specifically)
**Problem:** AI chatbots capitalize all main words in headings (e.g., Strategic Negotiations And Partnerships).
**Humanization Strategy:** Use sentence case for headings (e.g., Strategic negotiations and partnerships). 

## 17. Emojis
**Problem:** AI chatbots often decorate headings or bullet points with emojis to seem friendly.
**Humanization Strategy:** Remove emojis in professional or academic contexts.

## 18. Curly Quotation Marks
**Problem:** ChatGPT defaults to curly quotes (“...”) instead of standard straight quotes ("...").
**Humanization Strategy:** Standardize to straight quotes (or standard Chinese quotes 「」/“” as appropriate for the style guide).

## 19. Hyphenated Word Pair Overuse
**English words to watch:** third-party, cross-functional, client-facing, data-driven, decision-making, well-known, high-quality, real-time, long-term, end-to-end
**Chinese equivalent:** Overuse of four-character idioms (成语) or standardized compound adjectives where simpler descriptions suffice.

**Problem:** AI hyphenates common word pairs with perfect consistency, or overuses tight compound adjectives. Humans usually lack this rigid uniformity.
**Humanization Strategy:** Drop the hyphens on less formal text, or expand the adjective into a descriptive clause.

## 20. Nominal Loading (Noun/Adjective Overload)
**Problem:** AI text overloads sentences with nouns and adjectives to appear information-dense and professional. This is a measurable stylometric signal: AI-generated text has a significantly higher noun/adjective-to-total-words ratio than human text. It also under-produces pronouns and auxiliary verbs.

**Signs of nominal loading:**
- Long noun phrases stacked without pronouns: "The implementation of the configuration management system..."
- No referential chains across sentences (every sentence restates the full noun, not "it" or "they")
- Rare auxiliary verbs: "must", "might", "could", "should have been", "would have"

**Humanization Strategy:**
1. After rewriting for vocabulary, count content words in a paragraph. If nouns + adjectives exceed 60% of content words, rewrite.
2. Introduce pronoun referential chains: once a noun is introduced, refer to it as "it", "this", "they", or "that" in subsequent sentences.
3. Add auxiliary verbs to shade meaning: "The system can handle..." → "The system might handle... it could also..."
4. Vary noun phrase complexity: short ones ("the config system") mixed with full ones.

## 21. Contraction Absence
**Problem:** AI defaults to formal expanded forms ("do not", "it is", "we are", "cannot") uniformly across all registers. In informal and moderate-register writing, this reads as stiff and unnatural. Contraction frequency is a measurable POS balance signal.

**Humanization Strategy:** Where the register allows (blog posts, documentation, reports — anything not legal or medical), use contractions:
- "do not" → "don't"
- "it is" → "it's"
- "we are" → "we're"
- "cannot" → "can't"
- "they are" → "they're"
- "will not" → "won't"

Do not force contractions into formal legal, medical, or regulatory documents.

## 22. Uniform Lexical Density
**Problem:** AI maintains consistently high lexical density (content words / total words) across all sentences regardless of context. Human writing varies density — technical explanations are dense, linking sentences are light. Detectors measure this variance; flat density is an AI signal.

**Humanization Strategy:** After every 2-3 high-density technical sentences, add a low-density linking sentence. Examples:
- "That is the core constraint."
- "Here is why it matters."
- "This changes things."
- "So far, so predictable."

These sentences drop density intentionally and create the variation pattern detectors expect from human writing.

<!-- Patterns 23+ are in references/communication-patterns.md -->
