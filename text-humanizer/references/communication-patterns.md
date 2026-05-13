# Communication Patterns, Filler, and Hedging to Humanize

These patterns are artifacts of chatbot alignment, designed to be helpful, harmless, and universally appeasing. Removing them is essential for giving text a distinct, human "voice."

## 19. Collaborative Communication Artifacts
**English words to watch:** I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., let me know, here is a...
**Chinese words to watch:** 希望这对您有帮助、当然！、一定！、您说得完全正确！、您想要……、请告诉我、这是一个……

**Problem:** Text meant as chatbot conversational correspondence gets pasted directly into final content.

**Humanization Strategy:** Delete these entirely. They add zero value to the content.

## 20. Knowledge-Cutoff Disclaimers
**English words to watch:** as of [date], Up to my last training update, While specific details are limited/scarce..., based on available information...
**Chinese words to watch:** 截至 [日期]、根据我最后的训练更新、虽然具体细节有限/稀缺……、基于可用信息……

**Problem:** AI disclaimers about incomplete information or training timelines are left in the text.

**Humanization Strategy:** Remove the disclaimer. Fact-check the specific detail, and state the verified fact directly.

## 21. Sycophantic/Servile Tone
**Problem:** AI possesses an overly positive, people-pleasing, and subordinate language tone ("Great question! You're absolutely right that this is a complex topic.")
**Humanization Strategy:** Delete the flattery. Address the topic directly.

## 22. Filler Phrases
**Problem:** AI relies on formal padded phrases to seem objective and analytical.
**English Before → After:**
- "In order to achieve this goal" → "To achieve this"
- "Due to the fact that it was raining" → "Because it was raining"
- "At this point in time" → "Now"
- "In the event that you need help" → "If you need help"
- "The system has the ability to process" → "The system can process"
- "It is important to note that the data shows" → "The data shows"

**Chinese Before → After:**
- "为了实现这一目标" → "为了实现这一点"
- "由于下雨的事实" → "因为下雨"
- "在这个时间点" → "现在"
- "在您需要帮助的情况下" → "如果您需要帮助"
- "系统具有处理的能力" → "系统可以处理"
- "值得注意的是数据显示" → "数据显示"

**Humanization Strategy:** Cut the filler. Use the simplest, shortest preposition or conjunction.

## 23. Excessive Hedging
**Problem:** Over-qualifying statements to avoid hallucination responsibility (e.g., "It could potentially possibly be argued that...", "可以潜在地可能被认为...").
**Humanization Strategy:** Collapse the hedging into a simple "may", "might", or state it as an opinion if it is one.

## 24. Generic Positive Conclusions
**Problem:** AI ends passages with vague, upbeat, forward-looking endings (e.g., "The future looks bright for the company. Exciting times lie ahead.").
**Humanization Strategy:** Conclude with a concrete fact, a specific plan, or simply end the thought without a forced summary paragraph.

## 25. Overt Conjunctive Framing (Supervised Classifier Targets)
**Problem:** Supervised classifiers assign high SHAP weight to explicit transition phrases that AI uses to maintain surface coherence. These phrases are among the strongest positive signals in models like RoBERTa and Turnitin's classifier. Human writing builds logical flow implicitly through sentence structure, not through explicit labeling.

**English phrases to remove:**
- "In conclusion," / "To summarize," / "To wrap up,"
- "It is important to note that"
- "It is worth noting that" / "It is worth mentioning that"
- "Furthermore," / "Moreover," (when used more than once per page)
- "This highlights the importance of"
- "It should be noted that"
- "This underscores the need for" / "This underscores the importance of"
- "Needless to say,"
- "Last but not least,"
- "This is a testament to"
- "At the end of the day,"
- "Moving forward,"

**Humanization Strategy:** Delete the phrase and restructure the sentence so the relationship is implied. End one sentence with a premise; open the next with its consequence. Do not replace a removed transition with another explicit connector. Trust the paragraph to carry the logic.

**Before:** "Furthermore, this approach reduces latency. It is important to note that this has a direct impact on user experience."
**After:** "This approach reduces latency, which cuts directly into user wait time."

## 26. Structural Formula: Intro-Body-Conclusion Template
**Problem:** AI reliably produces sections that follow an explicit formula: introduce the topic, develop three points, then restate everything in a conclusion. Detectors recognize this rigid scaffolding through template-matching analysis.

**English markers of the formula:**
- Opening: "In this section, we will explore..."
- Body: numbered points with headers that mirror the introduction sentence
- Closing: any paragraph that restates what was just said

**Humanization Strategy:** Cut the meta-announcement opening. Cut or fold the restatement conclusion into the final body point. Let the content carry its own structure without narrating it.

<!-- Patterns continue in references/probabilistic-signals.md for detector-layer theory -->
