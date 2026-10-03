---
name: humanize-writing
description: Write or rewrite English so it reads like a real person wrote it, not an AI. Removes AI tells (delve, tapestry, "it's not X, it's Y", rule-of-three lists, em-dash overuse, tidy summary endings, uniform sentence rhythm) and adds real voice, varied rhythm, and concrete detail. Use whenever the user wants to humanize text, remove ChatGPT-sounding phrasing, sound less robotic, avoid AI-detector flags (GPTZero, Turnitin), or write a resume, CV, cover letter, report, essay, blog post, LinkedIn post, or email that should not sound like AI. Also use for English speaking practice such as interview answers, IELTS or TOEFL speaking responses, self-introductions, and presentation scripts that should sound natural when spoken. Trigger even if the user only says "make this sound more like me", "this reads too generic", or "polish my English".
---

# Humanize Writing

The goal is prose a sharp human editor would accept as written by a person with opinions and a particular way of talking. Detectors and readers pick up on the same underlying things:

- **Predictability**: every word is the most likely next word. This is what perplexity-based detectors measure.
- **Evenness**: similar sentence lengths, similar openers, similar paragraph shapes. This is "burstiness".
- **Generic content**: no specific people, numbers, places, or moments.
- **Stock moves**: the vocabulary and sentence patterns models overuse.

Removing the obvious words isn't enough. Text that's clean of "delve" but still smooth, balanced, and generic gets flagged anyway. The fixes that really work are the ones that make the text *less predictable in the way a specific person is less predictable*: their own details, their own phrasing habits, their own rhythm.

## Workflow

### 1. Get context and pick a mode (briefly)

Figure out:
- **Genre and reader**: resume, report, spoken script, email, blog, etc. Each one has its own register and its own tells, so read the matching section of `references/genres.md` before writing. For IELTS or other speaking-exam answers, also read `references/ielts-speaking.md`, which has the user's preferred model answer and template.
- **Voice sample**: Has the user given you something they wrote themselves, or is there a filled-in `references/voice-profile.md`? A sample is the single most useful input. Use it in step 3.
- **Raw material**: real anecdotes, numbers, names, and opinions.

Then pick the mode. **More of the user's own words in = more human out.**

| Mode | When | What you do |
|---|---|---|
| **Light-touch edit** | The user wrote the draft themselves | Keep their wording, order, and quirks. Fix grammar errors, unclear sentences, and the worst tells only. Don't "upgrade" their vocabulary. |
| **Build from notes** | The user gives rough notes, bullet thoughts, or a messy draft (in any language) | Write the piece around their points and phrases, reusing their exact wording wherever it works in English. |
| **Full rewrite** | Input is AI-generated or very generic | Rewrite fully using the moves in step 4. |
| **From scratch** | Only a topic | Write it, but ask for (or leave placeholders for) the real details. |

Light-touch edit matters more than it seems. Human text that's been heavily polished (by Grammarly, ChatGPT, or you) is one of the most common reasons real writing gets flagged. When the user brings their own draft, resist the urge to make it smooth.

If the request already makes most of this clear, don't interrogate the user. Ask one short question at most, or proceed and state your assumptions. If you're writing from scratch and have no real details, say once that pasting their own rough notes or a sample will make the result noticeably more human.

### 2. Draft or take the input

When writing from scratch, start from what you actually want to say, not from an outline of "key points".

### 3. Diagnose

Save the draft to a file and run the checker:

```bash
python3 <skill-dir>/scripts/check_tells.py draft.txt
python3 <skill-dir>/scripts/check_tells.py draft.txt --compare sample.txt   # when you have a writing sample
```

It reports:
- AI-tell words, phrases, and structures, with line numbers
- **bland/predictable wording**: "safe" words like *various, ensure, significant, in terms of*. They're harmless alone, but they make text predictable when they pile up.
- rhythm and style stats: sentence-length variation, short/long sentence share, sentence-opener repetition, contractions, word length
- **"Rewrite these sentences first"**: the sentences carrying the most tells
- with `--compare`, a **voice match** table showing where the draft drifts from the sample (for example "avg word length too high" or "The/This/It openers too high")

Treat it as a smoke alarm rather than a grade. A clean report doesn't mean the text is good. For the full catalog of tells, see `references/ai-tells.md`.

### 4. Rewrite

Read `references/techniques.md` for worked before/after examples. Start with the sentences the checker ranked first. The main moves:

- **Say the thing.** Cut throat-clearing openers ("In today's fast-paced world…", "When it comes to…") and the closing recap ("In conclusion…", "Ultimately, …").
- **Vary rhythm on purpose.** Mix short sentences with long ones that wander a bit before they land. Sometimes a one-line paragraph. Uniform 18–22-word sentences are the strongest statistical tell.
- **Vary how sentences start.** If half of them open with "The", "This", or "It", rework some to open with a clause, a name, a time ("Last March,"), "And", "But", or "So".
- **Break the symmetry.** Not everything comes in threes. Paragraphs should differ in length. Not every paragraph needs a topic sentence and a wrap-up line.
- **Be specific.** Replace abstractions with concrete nouns, numbers, names, places, and moments.
- **Have a point of view.** Commit to claims. Cut reflexive hedges and false balance.
- **Plain, short words.** "use" not "leverage", "help" not "facilitate", "make sure" not "ensure". A high average word length is a quiet tell.
- **De-predict the phrasing.** For each sentence the checker ranked, ask yourself whether this is exactly how anyone would phrase it. If so, say it the way *this* person would: their idiom, a more concrete verb, an aside in parentheses, a slightly unexpected but accurate word. Don't make it random or obscure, just less generic.
- **Repeat words instead of cycling synonyms.** Humans say "the city" three times. Models say "the city… the metropolis… the urban center".
- **Leave some natural roughness.** Use a sentence fragment, a parenthetical aside, a mild colloquialism, or a sentence that starts with "And". Don't sand every edge. (This doesn't mean typos. See below.)
- **Punctuation.** Keep em dashes rare (about one per 300 words at most). Avoid colon reveals. Use straight quotes.
- **Formatting.** Prose stays prose unless the genre calls for structure (resumes, long reports).
- **Match the voice sample** if you have one. Close the gaps the `--compare` table shows.

### 5. Re-check, then read it as a skeptic

Run the checker again. Reasonable targets (use judgment, these aren't rules):
- 0 flagged phrases or structures, and at most ~2 flagged words per 1,000 words
- bland wording under ~15 per 1,000 words
- sentence-length CV of at least ~0.45, with some short sentences
- with a sample: no more than 2–3 voice metrics off

If it's well off, do one more targeted pass on the worst sentences. Then read the piece as a skeptical editor and ask: Would a person actually say this? Does it sound like *one* person throughout?

## Don't use detector tricks

Some "AI humanizer" tools insert invisible characters, swap in look-alike Unicode letters, add deliberate typos, or run text through a synonym spinner. Don't do any of these:
- Detectors and plagiarism checkers flag them specifically. Turnitin, for example, reports "AI-paraphrased" text and hidden characters.
- They damage the text for the human reader, which is who actually matters.
- Hidden characters can break copy-paste, ATS resume parsers, and screen readers.

The only durable approach is writing that is actually specific, uneven, and in someone's real voice.

## Honesty guardrails

- **Don't invent experiences, quotes, statistics, or credentials** to make the piece feel human. If it needs a personal anecdote or a number you don't have, leave a clear placeholder like `[your example: the time a deploy broke on Friday]` and tell the user.
- Keep the meaning of the user's text intact when rewriting. Change the voice, not the facts or the claims.
- No tool can guarantee a "human" score on a detector, and detectors also flag plenty of real human writing. Don't promise a pass.
- If someone is clearly trying to submit AI-written work where that's prohibited, it's fine to mention that once, briefly. The writing help itself is still legitimate.

## Output

Unless the user asks for something else:
1. The final text, clean and ready to paste (or read aloud).
2. A short note (3–6 bullets) on the main changes, plus any placeholders the user needs to fill in.
3. For speaking practice only: a few reusable phrases from the script (see `references/genres.md`).
4. When it would really help, one line on the highest-leverage thing the user can do next, such as filling in the placeholders with real details, giving a writing sample, or doing a quick pass in their own words. Text the user has touched themselves reads more human than anything generated end to end.

Many users of this skill are non-native English writers. If the user writes to you in another language, write your notes in that language, but keep the deliverable itself in English.

Don't pad the response with a before/after table or a long explanation unless the user asks for one.
