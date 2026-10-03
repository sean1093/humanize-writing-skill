# humanize-writing-skill

A Claude skill that writes or rewrites English so it reads like a person wrote it. It removes "AI tells" (delve, tapestry, "it's not X, it's Y", three-item lists, em-dash overuse, summary endings, uniform sentence rhythm) and adds real voice, varied rhythm, and concrete detail.

這是一個 Claude skill，用來寫出或改寫成「像人寫的」英文。主要用在履歷、報告和英文口說練習，從零寫和改寫既有文字都可以。

## What it covers

- **Resumes / CVs**: plain verbs, varied bullets, no invented metrics
- **Reports**: lead with the finding, precise hedging, no fake citations
- **Speaking practice**: interview answers, IELTS/TOEFL, self-introductions, written to be *spoken*, plus reusable phrases
- **Also**: emails, cover letters, LinkedIn, and blog posts

## Structure

```
humanize-writing/
├── SKILL.md                  # workflow + guardrails
├── references/
│   ├── ai-tells.md           # catalog of AI tells and replacements
│   ├── techniques.md         # before/after rewrite examples
│   └── genres.md             # resume / report / speaking playbooks
├── scripts/
│   └── check_tells.py        # flags tells + rhythm stats (stdlib only)
└── evals/
    └── evals.json            # test prompts
```

## Install

**Claude Code** (personal, all projects):
```bash
cp -r humanize-writing ~/.claude/skills/
```

**Claude Code** (one project): copy the folder to `<project>/.claude/skills/humanize-writing`.

**Claude.ai**: zip the `humanize-writing` folder and upload it under Settings → Capabilities → Skills.

## Checker script

```bash
python3 humanize-writing/scripts/check_tells.py draft.txt
cat draft.txt | python3 humanize-writing/scripts/check_tells.py -
python3 humanize-writing/scripts/check_tells.py draft.txt --json
```

The script reports flagged words and phrases with line numbers, structural patterns, sentence-length variation, and em-dash density. Its output is a heuristic, not a detector score.

## Notes

- The skill never invents experiences, metrics, quotes, or citations. Where a real detail is needed, it leaves a `[placeholder]` for you to fill in.
- It can't guarantee a pass on any particular AI detector. Detectors change and have high false-positive rates. The goal is writing that reads well to people.
