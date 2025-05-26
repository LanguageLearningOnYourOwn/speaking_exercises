## Taboo Reformulate

### Description

Explain a target word without using its forbidden synonyms to strengthen paraphrasing skills.

### Example

```
Target: Apple
Forbidden: fruit, red, tree, iPhone
```

### AI Interaction

Two‑chat workflow:

1. **Chat A** — Use `taboo_generate` prompt to receive a target word and its forbidden synonyms.
2. **Chat B** — Switch to `taboo_reformulate` prompt, describe the target while avoiding the forbidden words.
3. The model in Chat B guesses the word and evaluates the clarity of your clues.
4. Refine your explanation or request a new word.

Pipeline:

* Generate target + taboo list (Chat A).
* Describe in Chat B without taboo words.
* Model guesses and scores.
* Start a new round.