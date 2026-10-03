#!/usr/bin/env python3
"""Scan English prose for common "AI tells" and rhythm stats.

Usage:
    python3 check_tells.py FILE
    cat FILE | python3 check_tells.py -
    python3 check_tells.py FILE --json
    python3 check_tells.py DRAFT --compare SAMPLE   # match a human writing sample

A heuristic smoke alarm, not a detector. Stdlib only.
"""
import argparse
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

# Second tier: not alarming alone, but models lean on these "safe", high-probability
# words and frames. High density makes text feel predictable.
BLAND_WORDS = [
    "various", "overall", "significant", "significantly", "effective",
    "effectively", "efficient", "efficiently", "ensure", "ensures", "ensuring",
    "valuable", "approach", "aspects", "potential", "particularly",
    "essentially", "numerous", "facilitate", "facilitates", "optimal",
    "optimize", "optimizing", "individuals", "thus", "therefore",
    "consequently", "key", "impactful", "strategic", "solutions",
]

BLAND_PHRASES = [
    r"in terms of", r"a variety of", r"in order to", r"it is essential",
    r"due to the fact", r"on the other hand", r"has the potential to",
    r"is designed to", r"allows? (you|us|users) to", r"is able to",
    r"a (key|major|significant) (factor|role|part)", r"(can|will) help (you|to)?",
    r"(positive|significant) impact", r"take it to the next level",
    r"stay ahead of the curve",
]

CONTRACTION = re.compile(
    r"\b\w+(n't|'re|'ll|'ve|'m|'d)\b|\b(it|that|there|what|here|he|she|who|let|where)'s\b",
    re.I,
)

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
    parts = re.split(r"(?<=[.!?])\s+(?=[\"'A-Z0-9\[(])", text)
    return [p for p in parts if p.strip()]


def line_of(text, idx):
    return text.count("\n", 0, idx) + 1


def mattr(tokens, window=50):
    """Moving-average type-token ratio: lexical variety, robust to length."""
    if not tokens:
        return 0.0
    if len(tokens) <= window:
        return len(set(tokens)) / len(tokens)
    ratios = [len(set(tokens[i:i + window])) / window for i in range(len(tokens) - window + 1)]
    return sum(ratios) / len(ratios)


def find_all(patterns, lower, text, as_words=False):
    hits = {}
    for p in patterns:
        rx = r"\b" + re.escape(p) + r"[a-z]*\b" if as_words else p
        for m in re.finditer(rx, lower):
            hits.setdefault(m.group(0), []).append(line_of(text, m.start()))
    return hits


def style_metrics(text, sents, words):
    n = max(len(words), 1)
    lens = [len(s.split()) for s in sents]
    mean = statistics.mean(lens) if lens else 0
    sd = statistics.pstdev(lens) if len(lens) > 1 else 0
    openers = [re.sub(r"[^a-z']", "", s.split()[0].lower()) for s in sents if s.split()]
    top_share = (max(openers.count(o) for o in set(openers)) / len(openers)) if openers else 0
    det_share = (sum(o in {"the", "this", "it", "these", "that", "they"} for o in openers) / len(openers)) if openers else 0
    lower_tokens = [w.lower() for w in words]
    return {
        "sentence_len_mean": round(mean, 1),
        "sentence_len_stdev": round(sd, 1),
        "sentence_len_cv": round(sd / mean, 2) if mean else 0,
        "short_sentences_pct": round(100 * sum(l <= 8 for l in lens) / len(lens), 1) if lens else 0,
        "long_sentences_pct": round(100 * sum(l >= 30 for l in lens) / len(lens), 1) if lens else 0,
        "contractions_per_100w": round(100 * len(CONTRACTION.findall(text)) / n, 2),
        "avg_word_len": round(sum(len(w) for w in words) / n, 2),
        "lexical_variety_mattr": round(mattr(lower_tokens), 3),
        "commas_per_sentence": round(text.count(",") / max(len(sents), 1), 2),
        "top_opener_share": round(top_share, 2),
        "pronoun_det_opener_share": round(det_share, 2),
        "questions_pct": round(100 * sum(s.rstrip().endswith("?") for s in sents) / max(len(sents), 1), 1),
        "parentheses_per_100w": round(100 * text.count("(") / n, 2),
        "em_dashes_per_300w": round(300 * (text.count("—") + len(re.findall(r"\s--\s", text))) / n, 2),
    }


def analyze(text):
    lower = text.lower()
    words = re.findall(r"[A-Za-z']+(?:-[A-Za-z']+)*", text)
    n_words = max(len(words), 1)

    word_hits = find_all(WORDS, lower, text, as_words=True)
    phrase_hits = find_all(PHRASES, lower, text)
    bland_hits = find_all([r"\b" + w + r"\b" for w in BLAND_WORDS] + BLAND_PHRASES, lower, text)

    struct_hits = {}
    for name, p in STRUCTURES.items():
        flags = re.MULTILINE if name == "ordinal_transitions" else 0
        ms = list(re.finditer(p, lower, flags))
        if ms:
            struct_hits[name] = [line_of(text, m.start()) for m in ms]

    sents = split_sentences(text.strip())
    paras = [p for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    plens = [len(p.split()) for p in paras]
    pcv = (statistics.pstdev(plens) / statistics.mean(plens)) if len(plens) > 1 else None

    trans_start = sum(
        1 for s in sents
        if re.match(r"(moreover|furthermore|additionally|however|ultimately|overall|notably|importantly|consequently)\b", s.lower())
    )

    # Rank sentences by how many tells/bland items they carry: rewrite these first.
    tell_rx = [r"\b" + re.escape(w) + r"[a-z]*\b" for w in WORDS] + PHRASES + \
              [p for k, p in STRUCTURES.items() if k != "triplet_list"]
    bland_rx = [r"\b" + w + r"\b" for w in BLAND_WORDS] + BLAND_PHRASES
    ranked = []
    for s in sents:
        sl = s.lower()
        score = 2 * sum(len(re.findall(p, sl)) for p in tell_rx) + sum(len(re.findall(p, sl)) for p in bland_rx)
        if score:
            ranked.append((score, s))
    ranked.sort(key=lambda x: -x[0])

    em = text.count("—") + len(re.findall(r"\s--\s", text))
    return {
        "words": len(words),
        "sentences": len(sents),
        "paragraphs": len(paras),
        "paragraph_len_cv": round(pcv, 2) if pcv is not None else None,
        "em_dashes": em,
        "transition_sentence_starts": trans_start,
        "style": style_metrics(text, sents, words),
        "flagged_words": word_hits,
        "flagged_phrases": phrase_hits,
        "structures": struct_hits,
        "bland": bland_hits,
        "bland_per_1000w": round(1000 * sum(len(v) for v in bland_hits.values()) / n_words, 1),
        "rewrite_first": [{"score": sc, "sentence": s[:200]} for sc, s in ranked[:5]],
        "tell_count": sum(len(v) for v in word_hits.values())
        + sum(len(v) for v in phrase_hits.values())
        + sum(len(v) for k, v in struct_hits.items() if k != "triplet_list"),
    }


def report(r):
    st = r["style"]
    out = [f"Words: {r['words']}  Sentences: {r['sentences']}  Paragraphs: {r['paragraphs']}", ""]
    out.append("RHYTHM & STYLE")
    enough = r["sentences"] >= 5
    flag = "  <- low variation, reads uniform" if st["sentence_len_cv"] < 0.4 and enough else ""
    out.append(f"  sentence length mean {st['sentence_len_mean']}, stdev {st['sentence_len_stdev']}, CV {st['sentence_len_cv']}{flag}")
    sflag = "  <- no short punchy sentences" if st["short_sentences_pct"] == 0 and enough else ""
    out.append(f"  short (<=8 words) {st['short_sentences_pct']}%, long (>=30) {st['long_sentences_pct']}%{sflag}")
    if r["paragraph_len_cv"] is not None:
        pflag = "  <- paragraphs suspiciously even" if r["paragraph_len_cv"] < 0.25 and r["paragraphs"] >= 4 else ""
        out.append(f"  paragraph length CV {r['paragraph_len_cv']}{pflag}")
    eflag = "  <- too many" if st["em_dashes_per_300w"] > 1 else ""
    out.append(f"  em dashes: {r['em_dashes']} ({st['em_dashes_per_300w']} per 300 words){eflag}")
    oflag = "  <- sentence openers repetitive" if (st["top_opener_share"] > 0.3 or st["pronoun_det_opener_share"] > 0.5) and enough else ""
    out.append(f"  most common opener share {st['top_opener_share']}, The/This/It openers {st['pronoun_det_opener_share']}{oflag}")
    out.append(f"  contractions {st['contractions_per_100w']}/100w, avg word length {st['avg_word_len']}, lexical variety {st['lexical_variety_mattr']}")
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
    bflag = "  <- predictable, generic wording" if r["bland_per_1000w"] > 15 else ""
    block(f"BLAND / PREDICTABLE WORDING ({r['bland_per_1000w']} per 1000 words){bflag}", r["bland"])
    if r["rewrite_first"]:
        out.append("REWRITE THESE SENTENCES FIRST")
        for item in r["rewrite_first"]:
            out.append(f"  [{item['score']}] {item['sentence']}")
        out.append("")
    out.append(f"TOTAL TELLS (excluding triplets and bland): {r['tell_count']}  "
               f"({round(r['tell_count'] / max(r['words'], 1) * 1000, 1)} per 1000 words)")
    return "\n".join(out)


# (metric, label, relative tolerance) for --compare
COMPARE = [
    ("sentence_len_mean", "avg sentence length", 0.25),
    ("sentence_len_cv", "sentence length variation", 0.30),
    ("short_sentences_pct", "% short sentences", 0.50),
    ("contractions_per_100w", "contractions /100w", 0.40),
    ("avg_word_len", "avg word length", 0.08),
    ("lexical_variety_mattr", "lexical variety", 0.08),
    ("commas_per_sentence", "commas per sentence", 0.35),
    ("pronoun_det_opener_share", "The/This/It openers", 0.40),
    ("questions_pct", "% questions", 0.60),
    ("parentheses_per_100w", "parentheses /100w", 0.60),
    ("em_dashes_per_300w", "em dashes /300w", 0.60),
]


def compare_report(draft, sample):
    ds, ss = draft["style"], sample["style"]
    out = ["", "VOICE MATCH vs SAMPLE (adjust the draft toward the sample)",
           f"  {'metric':28} {'sample':>8} {'draft':>8}"]
    off = 0
    for key, label, tol in COMPARE:
        a, b = ss[key], ds[key]
        base = max(abs(a), 1e-9)
        bad = (abs(a - b) / base > tol) if a else (b > 0.5)
        if bad:
            off += 1
            hint = "  <- too high" if b > a else "  <- too low"
        else:
            hint = ""
        out.append(f"  {label:28} {a:>8} {b:>8}{hint}")
    out.append(f"  {off} of {len(COMPARE)} metrics outside the sample's range")
    if sample["words"] < 150:
        out.append("  (sample is short; under ~150 words these numbers are rough)")
    return "\n".join(out)


def read(path):
    if path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8") as f:
        return f.read()


def main():
    ap = argparse.ArgumentParser(description="Flag AI tells and style stats in English prose.")
    ap.add_argument("file", nargs="?", default="-", help="text file, or - for stdin")
    ap.add_argument("--compare", metavar="SAMPLE", help="human writing sample to match")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    a = ap.parse_args()
    r = analyze(read(a.file))
    if a.compare:
        r["sample"] = analyze(read(a.compare))
    if a.json:
        print(json.dumps(r, indent=2))
        return
    print(report(r))
    if a.compare:
        print(compare_report(r, r["sample"]))


if __name__ == "__main__":
    main()
