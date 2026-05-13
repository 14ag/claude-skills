# Open-Detector Principles

This reference establishes the mindset for removing AI writing traces, drawn from the philosophy of the Open Detector project.

## The Goal
The mission of AI is to improve efficiency, not return people to an era of handwriting. AI far exceeds most human writers in vocabulary selection, syntactic variation, and logical coherence.

But **"Writing like AI" ≠ Quality.**

Commercial academic detection services use black-box stylometric detection to punish "AI style". This means students and professionals are penalized not for cheating, but for formatting facts in a way that aligns statistically with an LLM's average output.

Therefore, the goal of this humanizer skill is to:
1. Identify formatting choices made by AI statistical models.
2. Break those formatting models so the text sounds genuinely personal, specific, and human.
3. Eliminate AI writing traces to avoid misjudgment by style detection systems like Turnitin or Open Detector.

## Hallucinations vs. Authenticity
What humans should really care about is not whether AI was used, but whether the content is authentic, reliable, and free of false generation (hallucinations).

When humanizing text:
- **Prioritize factual authenticity.** Ask the user for specific facts if the text uses generic filler (e.g. replacing "Industry observers note..." with actual examples).
- **Check consistency.** If the generated text lists generic features, verify if those features specifically map to the topic originally requested.
- **Maintain the thesis, discard the fluff.** Academic and professional texts should maintain their rigorous structure and reasoning. You are breaking the *style*, not the *logic*.
