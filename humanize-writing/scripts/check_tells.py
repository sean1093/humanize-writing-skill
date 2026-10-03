#!/usr/bin/env python3
"""Scan English prose for common "AI tells" and rhythm stats.

Usage:
    python3 check_tells.py FILE
    cat FILE | python3 check_tells.py -
    python3 check_tells.py FILE --json

A heuristic smoke alarm, not a detector. Stdlib only.
"""
import json
import re
import statistics
import sys

# Stems: matched as whole-word prefixes (e.g. "foster" catches fosters/fostering).
WORDS = [
    "delve", "delving", "tapestr", "testament", "landscape", "realm", "navigat",
    "leverag", "harness", "utiliz", "foster", "cultivat", "empower", "unlock",
    "unleash", "elevat", "enhanc", "showcas", "underscor", "crucial", "pivotal",
    "paramount", "vital", "robust", "seamless", "comprehensive", "holistic",
    "intricate", "nuanced", "multifaceted", "vibrant", "bustling", "meticulous",
    "embark", "resonat", "boasts", "plethora", "myriad", "ever-evolving",
    "ever-changing", "fast-paced", "game-changer", "game-changing",
    "cutting-edge", "groundbreaking", "beacon", "cornerstone", "interplay",
    "synerg", "moreover", "furthermore", "additionally", "notably",
    "ultimately", "commendable", "noteworthy", "invaluable", "insights",
    "streamlin", "transformative", "dynamic",
]

PHRASES = [
    r"in today'?s(?: [\w-]+){0,3} (world|landscape|age|era|climate|market)",
    r"in the ever-\w+ (world|landscape|realm) of",
    r"when it comes to",
    r"in an era (where|of)",
    r"it'?s (important|worth) (to note|noting|mentioning)",
    r"let'?s (dive|delve) in(to)?",
    r"let'?s break (it|this) down",
    r"plays? an? (crucial|pivotal|vital|key|important|significant) role",
    r"(stands|serves) as an?",
    r"(is|stands as) a testament to",
    r"at its core",
    r"at the end of the day",
    r"in conclusion",
    r"in summary",
    r"to sum (it )?up",
    r"all in all",
    r"whether you'?re an? .{1,40}? or",
    r"the (possibilities|options) are endless",
    r"only time will tell",
    r"a (rich|vibrant) (tapestry|history|culture)",
    r"a wide (array|range|variety) of",
    r"(navigate|navigating) the (complexities|challenges)",
    r"(certainly|absolutely|great question)!",
    r"i hope this helps",
    r"feel free to",
    r"picture this",
    r"imagine a world",
    r"have you ever wondered",
    r"here'?s the thing",
    r"without further ado",
    r"experts (agree|say|suggest)",
    r"studies (show|suggest)",
]

STRUCTURES = {
    "negation_reframe": r"\b(more than (just )?an? [^.!?]{1,40}?[,;—–-]+ ?it'?s|not (just|only|merely) [^.!?]{1,80}?,? (but|it'?s)|isn'?t (just |only )?(about )?[^.!?]{1,60}?[.,;] ?(it'?s|this is))",
    "trailing_participle": r", (highlighting|underscoring|showcasing|emphasizing|ensuring|making it|reflecting|demonstrating|signaling|fostering|paving the way)\b",
    "triplet_list": r"\b\w+, \w+(?: \w+)?,? and \w+\b",
    "colon_reveal": r"(^|[.!?] )\w+(\s\w+){0,4}\?\s+\w+(\s\w+){0,3}\.",
    "hedge_stack": r"\b(may|might|could) (potentially|possibly)\b",
    "ordinal_transitions": r"(^|\n)\s*(firstly|secondly|thirdly|lastly|finally),",
}


def split_sentences(text):
    text = re.sub(r"\s+", " ", text)
    parts = re.split(r"(?<=[.!?])\s+(?=[\"'A-Z0-9])", text)
    return [p for p in parts if len(p.split()) >= 1]


def line_of(text, idx):
    return text.count("\n", 0, idx) + 1


def analyze(text):
    lower = text.lower()
    words = re.findall(r"[A-Za-z']+(?:-[A-Za-z']+)*", text)
    n_words = max(len(words), 1)

    word_hits = {}
    for w in WORDS:
        for m in re.finditer(r"\b" + re.escape(w) + r"[a-z]*\b", lower):
            word_hits.setdefault(m.group(0), []).append(line_of(text, m.start()))

    phrase_hits = {}
    for p in PHRASES:
        for m in re.finditer(p, lower):
            phrase_hits.setdefault(m.group(0), []).append(line_of(text, m.start()))

    struct_hits = {}
    for name, p in STRUCTURES.items():
        flags = re.MULTILINE if name == "ordinal_transitions" else 0
        ms = list(re.finditer(p, lower, flags))
        if ms:
            struct_hits[name] = [line_of(text, m.start()) for m in ms]

    sents = split_sentences(text.strip())
    lens = [len(s.split()) for s in sents]
    mean = statistics.mean(lens) if lens else 0
    sd = statistics.pstdev(lens) if len(lens) > 1 else 0
    cv = sd / mean if mean else 0

    paras = [p for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    plens = [len(p.split()) for p in paras]
    pcv = (statistics.pstdev(plens) / statistics.mean(plens)) if len(plens) > 1 else None

    em = text.count("—") + len(re.findall(r"\s--\s", text))
    em_per_300 = em / n_words * 300

    trans_start = sum(
        1 for s in sents
        if re.match(r"(moreover|furthermore|additionally|however|ultimately|overall|notably|importantly|consequently)\b", s.lower())
    )

    return {
        "words": len(words),
        "sentences": len(sents),
        "sentence_len_mean": round(mean, 1),
        "sentence_len_stdev": round(sd, 1),
        "sentence_len_cv": round(cv, 2),
        "paragraphs": len(paras),
        "paragraph_len_cv": round(pcv, 2) if pcv is not None else None,
        "em_dashes": em,
        "em_dashes_per_300_words": round(em_per_300, 2),
        "transition_sentence_starts": trans_start,
        "flagged_words": word_hits,
        "flagged_phrases": phrase_hits,
        "structures": struct_hits,
        "tell_count": sum(len(v) for v in word_hits.values())
        + sum(len(v) for v in phrase_hits.values())
        + sum(len(v) for k, v in struct_hits.items() if k != "triplet_list"),
    }


def report(r):
    out = []
    out.append(f"Words: {r['words']}  Sentences: {r['sentences']}  Paragraphs: {r['paragraphs']}")
    out.append("")
    out.append("RHYTHM")
    flag = "  <- low variation, reads uniform" if r["sentence_len_cv"] < 0.4 and r["sentences"] >= 5 else ""
    out.append(f"  sentence length mean {r['sentence_len_mean']}, stdev {r['sentence_len_stdev']}, CV {r['sentence_len_cv']}{flag}")
    if r["paragraph_len_cv"] is not None:
        pflag = "  <- paragraphs suspiciously even" if r["paragraph_len_cv"] < 0.25 and r["paragraphs"] >= 4 else ""
        out.append(f"  paragraph length CV {r['paragraph_len_cv']}{pflag}")
    eflag = "  <- too many" if r["em_dashes_per_300_words"] > 1 else ""
    out.append(f"  em dashes: {r['em_dashes']} ({r['em_dashes_per_300_words']} per 300 words){eflag}")
    out.append(f"  sentences opening with stock transitions: {r['transition_sentence_starts']}")
    out.append("")

    def block(title, d):
        out.append(title)
        if not d:
            out.append("  (none)")
        for k, lines in sorted(d.items(), key=lambda kv: -len(kv[1])):
            out.append(f"  {k!r} x{len(lines)}  (lines {', '.join(map(str, lines[:8]))})")
        out.append("")

    block("FLAGGED WORDS", r["flagged_words"])
    block("FLAGGED PHRASES", r["flagged_phrases"])
    block("STRUCTURAL PATTERNS (triplet_list is noisy; check by eye)", r["structures"])
    out.append(f"TOTAL TELLS (excluding triplets): {r['tell_count']}  "
               f"({round(r['tell_count'] / max(r['words'], 1) * 1000, 1)} per 1000 words)")
    return "\n".join(out)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    if not args or args[0] == "-":
        text = sys.stdin.read()
    else:
        with open(args[0], encoding="utf-8") as f:
            text = f.read()
    r = analyze(text)
    print(json.dumps(r, indent=2) if as_json else report(r))


if __name__ == "__main__":
    main()
