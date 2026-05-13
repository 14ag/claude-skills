# Linguistic Fingerprints: Deep AI Detection Signals

Modern supervised classifiers (RoBERTa-based, Turnitin, GPTZero) go beyond surface vocabulary and detect structural patterns in the text's part-of-speech distribution, cohesion strategy, and information density. These are the signals that survive basic synonym swapping. Fix them in Stage 1 diagnosis and Stage 3 structural transfer.

## 20. Nominal Loading

**Problem:** AI-generated text has a significantly higher density of nouns and adjectives relative to total word count compared to human text. This is called nominal loading. LLMs default to expository, information-dense sentences that pack in noun phrases ("the implementation of a scalable microservices architecture") instead of using pronouns and auxiliary verbs to maintain flow.

**Detection signal:** Supervised classifiers measure noun-to-pronoun ratio and auxiliary verb frequency. High noun density with low pronoun usage is a strong AI indicator.

**Humanization strategy:**
- Replace noun clusters with a pronoun where the referent is clear ("it," "they," "this").
- Break a long noun phrase into a clause: "the implementation of a scalable microservices architecture" -> "a microservices setup that scales."
- Add auxiliary verbs to shade meaning: "The system handles requests" -> "The system can handle requests even when load spikes."
- Use perspective shift (second or first person plural) to naturally reduce noun density.

**Watch for:** Sentences where every phrase is a compound noun. Strings of three or more nouns in a row ("user engagement optimization strategy") are a reliable tell.

## 21. Overt Conjunctive Framing

**Problem:** AI models maintain coherence by using explicit transition words at the start of sentences: "Furthermore," "Moreover," "In addition," "It is important to note that," "In conclusion," "As previously mentioned." Human writing achieves the same logical flow through sentence structure, not labeling.

**Detection signal:** Transition phrase frequency is one of the most reliably flagged features by SHAP analysis on RoBERTa classifiers. "In conclusion" and "It is important to note" are near-certain AI signals.

**Humanization strategy:**
- Delete the transition phrase entirely and let the sentence stand. Most sentences work without them.
- Replace "Furthermore, X" with "And X" or reorder the paragraph so X follows naturally from the previous sentence without any connector.
- Replace "In conclusion, X" with a short declarative that is the conclusion, without announcing it.
- Replace "It is important to note that X" with just "X."
- Replace "As previously mentioned" with a pronoun reference to the earlier point.

**Phrases to eliminate:** Furthermore, Moreover, Additionally, In addition, In conclusion, To summarize, It is important to note, It is worth noting, As previously mentioned, As noted above, Needless to say, Last but not least.

## 22. Uniform Lexical Density

**Problem:** AI models, especially those fine-tuned for professional contexts, maintain a consistently high level of vocabulary complexity throughout a document regardless of the topic or reader. Humans naturally modulate their language -- using simpler words in transitions, more precise terms in technical passages.

**Detection signal:** Token entropy and lexical density (ratio of unique content words to total words) measured across paragraph windows. AI text has a narrow, stable range. Human text has a wider variance.

**Humanization strategy:**
- After a technically dense paragraph, write the connecting sentence in plain everyday language ("So what does this mean in practice?").
- Avoid using the most technical synonym available when a common word works just as well. "Utilize" is never better than "use" for density purposes.
- Vary register within the document. A paragraph of technical specifics can be followed by a direct, simple statement of consequence.

## 23. Referential Gaps

**Problem:** AI models often lose track of pronoun reference chains over long passages. They will refer to an entity by its full name four times in a paragraph instead of using "it" or "they" after the first mention. Paradoxically, they can also break referential continuity by switching between synonyms for the same referent (elegant variation, pattern #11), which makes tracking the subject harder for both readers and detectors.

**Detection signal:** Discourse analysis tools measure referential chain density and consistency. Repeated full noun repetition without pronoun substitution is an AI tell.

**Humanization strategy:**
- After the first full mention of a noun in a paragraph, use a pronoun for subsequent references where the referent is unambiguous.
- Do not substitute synonyms to avoid repetition -- just repeat the noun or use a pronoun. Synonym cycling is itself a detection signal.
- If a long paragraph refers to a complex subject repeatedly, establish a short informal label on first mention ("the pipeline," "the module," "the tool") and use that label consistently.

## 24. Formulaic Structural Flow

**Problem:** AI documents follow predictable templates: Introduction (background + importance statement), Body (three equal-weight sections), Conclusion (summary + future outlook). Detectors trained on academic and blog corpora recognize this template at the document level.

**Detection signal:** Section header pattern matching, structural symmetry between sections, and the presence of formulaic closing sections ("Future Directions," "Conclusion," "Summary").

**Humanization strategy:**
- Move the most interesting or specific finding to the opening paragraph instead of building to it.
- Merge or cut the "Conclusion" section. End the last substantive section on a direct statement of consequence or an open question.
- Make sections unequal in length. One section being twice as long as another is normal in human writing; perfect symmetry is not.
- Cut or integrate "Challenges" and "Future Outlook" sections into the body rather than isolating them as closing appendices.
