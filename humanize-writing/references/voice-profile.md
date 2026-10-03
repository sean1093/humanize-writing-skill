# Voice Profile

Paste 2–3 samples of your own English writing below: emails, reports, chat messages, anything you wrote without AI help. Aim for 300+ words in total. The skill reads this file to match your voice, and runs `check_tells.py --compare` against the samples to measure the gap.

The more samples you add, and the more they resemble the kind of writing you'll ask for, the better the match. A work email sample helps with reports. A casual message helps with speaking scripts.

Leave this file as-is if you don't want a saved profile. You can always paste a sample directly into the conversation instead.

---

## Notes about my voice (optional)

<!-- Anything you know about how you write. Examples:
- I use short sentences and lots of parentheses
- I never use exclamation marks
- I say "pretty" and "honestly" a lot
- English is my second language. Keep the vocabulary simple and don't make me sound more fluent than I am
-->

## Sample 1

<!-- paste here -->

## Sample 2

<!-- paste here -->

## Sample 3

<!-- paste here -->

---

## For the skill: how to use this file

If the samples above are filled in:
1. Extract them into a temporary `sample.txt` and run `check_tells.py draft.txt --compare sample.txt`.
2. Note fingerprints the script doesn't measure: pet words, how paragraphs open, humor, typical sign-offs, and how formal the writing is.
3. Write to those fingerprints. Matching this person's real habits matters more than any generic "human" rule. That includes their level of English: if the samples use simple vocabulary, the output should too.
