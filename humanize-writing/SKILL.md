---
name: humanize-writing
description: Write or rewrite English prose so it reads like a specific human wrote it, not a language model, stripping out "AI tells" (delve, tapestry, "it's not X, it's Y", rule-of-three lists, em-dash overuse, tidy summary endings, uniform sentence rhythm) and adding real voice, rhythm variation, and concrete detail. Use this skill whenever the user asks to humanize text, remove "AI voice" or "ChatGPT-sounding" phrasing, make writing sound more natural or less robotic, pass or avoid flags from AI detectors (GPTZero, Originality, Turnitin, etc.), or write a resume/CV, cover letter, work or school report, essay, blog post, LinkedIn post, or email that "shouldn't sound like AI". Also use it for English speaking practice: interview answers, IELTS/TOEFL speaking responses, self-introductions, and presentation scripts that should sound natural when spoken rather than memorized. Use it even when the user only says "make this sound more like me", "this reads too generic", or "polish my English".
---

# Humanize Writing

The goal is prose a sharp human editor would accept as written by a person with opinions and a particular way of talking. Detectors and readers pick up on the same underlying things: predictable word choice, even rhythm, generic content, and a set of stock moves models overuse. Fix those at the root and the detector score usually takes care of itself. Chasing a single detector's number by inserting typos or swapping in odd synonyms makes the writing worse and stops working once the detector updates, so don't do that.

## Workflow

### 1. Get context (briefly)

Before writing, figure out:
- **Genre and reader**: resume, report, spoken script, email, blog, etc. Each one has its own register and its own tells, so read the matching section of `references/genres.md` before writing. Resumes keep their bullets, reports may stay formal, and speaking scripts must sound like speech rather than an essay.
- **Voice**: Did the user give a writing sample? If so, it's the best input you have. Study its sentence length, how it opens paragraphs, its contractions, humor, pet phrases, punctuation habits, and how formal it is, then match that. If there's no sample, pick a voice that fits the genre and commit to it.
- **Raw material**: real anecdotes, numbers, names, and opinions the user can provide.

If the request already makes most of this clear, don't interrogate the user. Ask one short question at most, or just proceed and state your assumptions.

### 2. Draft or take the input

When writing from scratch, write the way a person does: start from what you actually want to say, not from an outline of "key points".

### 3. Diagnose

Run the checker on the draft (or on the user's original, so you can show the before/after):

```bash
python3 <skill-dir>/scripts/check_tells.py draft.txt      # or: echo "$TEXT" | python3 .../check_tells.py -
```

It reports flagged words and phrases with line numbers, structural patterns, and rhythm stats (sentence-length variation, em-dash density). Treat it as a smoke alarm rather than a grade. A clean report doesn't mean the text is good, and one "crucial" in a 1,000-word piece is fine. For the full catalog of tells and the reasons they read as machine-made, see `references/ai-tells.md`.

### 4. Rewrite

Read `references/techniques.md` for worked before/after examples. The main moves:

- **Say the thing.** Cut throat-clearing openers ("In today's fast-paced world…", "When it comes to…") and the closing recap ("In conclusion…", "Ultimately, …"). Start where the interesting part starts, and stop when you're done.
- **Vary rhythm on purpose.** Mix short sentences with long ones that wander a bit before they land. Sometimes a one-line paragraph. Uniform 18–22-word sentences are the strongest statistical tell.
- **Break the symmetry.** Not everything comes in threes. Make two points, or one point developed properly. Paragraphs should differ in length. Not every paragraph needs a topic sentence and a wrap-up line.
- **Be specific.** Replace abstractions with concrete nouns, numbers, names, places, and moments. "Our onboarding was slow" becomes "New hires spent their first four days waiting on laptop permissions."
- **Have a point of view.** Commit to claims. Cut reflexive hedges and false balance. A little bluntness, an aside, or a joke that fits the voice beats a neutral survey.
- **Plain words.** Use "use" instead of "leverage", "help" instead of "empower", "show" instead of "showcase". Prefer the word you'd say out loud.
- **Natural register.** Use contractions where the genre allows. Occasional fragments. Starting a sentence with "And" or "But" is fine.
- **Punctuation.** Keep em dashes rare (about one per 300 words at most) and rework most of them into commas, periods, or parentheses. Avoid colon-reveal and semicolon-heavy sentences. Use straight quotes unless the user's text already uses curly ones.
- **Formatting.** Prose stays prose. Don't add headers, bolded lead-ins, bullet lists, or emoji unless the genre really calls for them (resumes, long reports, docs) or the user's original had them.

### 5. Re-check and read it aloud (mentally)

Run the checker again. Then read the piece as a skeptical editor would and ask: Would a person actually say this sentence? Is there anything here only a model would write? Does it sound like *one* person throughout?

## Honesty guardrails

- **Don't invent experiences, quotes, statistics, or credentials** to make the piece feel human. Fabricated specifics are worse than generic ones. If the piece needs a personal anecdote or a number you don't have, leave a clear placeholder like `[your example: the time a deploy broke on Friday]` and tell the user, or ask for one.
- Keep the meaning of the user's text intact when rewriting. Change the voice, not the facts or the claims.
- If someone is clearly trying to submit AI-written work where that's prohibited (for example, a class assignment that bans AI), it's fine to mention that once, briefly. The writing help itself is still legitimate, and plenty of people are trying to avoid false positives on their own writing.

## Output

Unless the user asks for something else:
1. The rewritten text, clean and ready to paste (or read aloud).
2. A short note (3–6 bullets) on the main changes, plus any placeholders the user needs to fill in.
3. For speaking practice only: a few reusable phrases from the script (see `references/genres.md`).

Many users of this skill are non-native English writers. If the user writes to you in another language, write your notes in that language, but keep the deliverable itself in English.

Don't pad the response with a before/after table or a long explanation unless the user asks for one.
