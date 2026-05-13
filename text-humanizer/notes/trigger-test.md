# Negative Trigger Smoke Tests

These prompts were tested to confirm the text-humanizer skill does NOT load on clearly unrelated requests.

## Test Method

Each prompt was submitted to the assistant with the skill active. The skill should only activate when the user explicitly asks to humanize, edit for AI patterns, or review text for AI writing tells.

## Test Cases

| Prompt | Expected | Outcome |
|---|---|---|
| "Write me a Python script to sort a list." | Skill does not trigger; assistant writes Python. | PASS |
| "Explain the differences between TCP and UDP." | Skill does not trigger; assistant explains networking. | PASS |
| "Translate this paragraph from English to Spanish." | Skill does not trigger; assistant translates. | PASS |
| "What is the capital of France?" | Skill does not trigger; assistant answers factually. | PASS |

## Conclusion

The description's negative trigger clause ("Do not use this skill for generating new text from scratch, answering factual questions, or writing code.") is sufficient to prevent loading on the four tested unrelated categories.
