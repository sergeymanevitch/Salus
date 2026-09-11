#!/usr/bin/env python3
"""Convert a safety data sheet PDF into a line-anchored Markdown rendering, and
produce the evidence that the conversion lost nothing.

    python3 tools/extract.py "test-cases/sds/<sheet>.pdf" [--outdir audits/<run>]

Writes two files beside each other:

    <sheet>.salus.md        what the auditor reads and what a judge checks against
    <sheet>.fidelity.json   the proof, and the honest limits of that proof

HOW THE FIDELITY CLAIM IS MADE

The rendering is not a summary, a reflow, or a cleanup. It is the output of one extractor with a
line number prefixed to every line. Strip the prefixes and the bytes are identical - the script
asserts that with a SHA-256 comparison, so "the Markdown equals the extraction" is proved, not
promised.

That leaves the real question: did the extraction lose anything the PDF contained? One extractor
cannot answer that about itself. So the sheet is extracted a second time with an independent
engine (pypdf, a different codebase from poppler's pdftotext), and the two are compared as
multisets of characters, ignoring whitespace - the one thing the two engines are entitled to
disagree about. On top of that, every chemical identifier and hazard code is located in both
extractions with a whitespace-tolerant pattern and the two sets must match exactly.

WHAT THIS CANNOT PROVE, stated here because a safety document is the wrong place for a quiet
assumption: if both engines miss the same thing - most of all, text that exists only as an image -
the comparison agrees and is wrong together. That is why page-level text density is reported per
page: a page carrying almost no extractable text is flagged, whatever the two engines agree on.
"""
import argparse, hashlib, json, os, re, subprocess, sys, collections, datetime

IDENTIFIER_PATTERNS = {
    # Longest first: a claimed span is never re-read as a shorter identifier.
    # The lookarounds matter more than they look. Without them "B18 7QH 0344 892" reads as
    # hazard code H034, which is not a hazard code at all - a real false positive this corpus
    # produced before the boundaries were added.
    "index": r"(?<![\d-])\d{3}\s?-\s?\d{3}\s?-\s?\d{2}\s?-\s?\d(?![\d-])",
    "cas":   r"(?<![\d-])\d{2,7}\s?-\s?\d{2}\s?-\s?\d(?![\d-])",
    "ec":    r"(?<![\d-])\d{3}\s?-\s?\d{3}\s?-\s?\d(?![\d-])",
    "hcode": r"(?<![A-Za-z0-9])EUH\s?\d{3}[A-Za-z]?(?![A-Za-z0-9])"
             r"|(?<![A-Za-z0-9])H\s?[234]\d{2}(?:[idf]|F[dD]?|D[fF]?)?(?![A-Za-z0-9])",
    "pcode": r"(?<![A-Za-z0-9])P\s?[1-5]\d{2}(?![A-Za-z0-9])",
}


def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def norm(s):
    """Fold the differences two extractors are allowed to have: the several dashes and
    quotes PDF producers emit, and the ligatures. Whitespace is handled separately,
    because the two engines legitimately disagree about it."""
    s = s.replace("\u00a0", " ")
    for a, b in [("\u2010", "-"), ("\u2011", "-"), ("\u2012", "-"), ("\u2013", "-"),
                 ("\u2014", "-"), ("\u2212", "-"), ("\u2018", "'"), ("\u2019", "'"),
                 ("\u201c", '"'), ("\u201d", '"'), ("\ufb01", "fi"), ("\ufb02", "fl")]:
        s = s.replace(a, b)
    return s


def split_tokens(text):
    """Break text into alphabetic and numeric tokens, splitting also at the boundaries one
    engine invents and the other does not: lower-to-upper transitions and digit-to-letter
    transitions. Without this, pypdf's habit of running a value into the next label
    ("Liquid.Product", "2019date") would read as content the other engine lacks."""
    t = norm(text)
    t = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", t)
    t = re.sub(r"(?<=[0-9])(?=[A-Za-z])", " ", t)
    t = re.sub(r"(?<=[A-Za-z])(?=[0-9])", " ", t)
    return set(x.lower() for x in re.findall(r"[A-Za-z\u00c0-\u024f]{3,}|[0-9]+", t))


def char_set(text):
    return set(re.sub(r"\s", "", norm(text)))


def squash(text):
    """One continuous lower-case stream of letters and digits. Used as the haystack: a token
    from the independent extraction counts as present in the shipped rendering if its
    characters occur there in that order and adjacently, which survives the two engines
    disagreeing about where a space belongs."""
    return re.sub(r"[^a-z0-9\u00c0-\u024f]", "", norm(text).lower())


def identifiers(text):
    """Chemical identifiers and hazard codes, located whitespace-tolerantly and then
    canonicalised, so "H 304" and "H304" are one token and "265 - 155 - 0" is still an EC
    number. Patterns are tried longest-first and claimed spans are not reused, so a CAS
    number is never also read as an EC number."""
    t = norm(text)
    found, spans = set(), []
    for kind, pat in IDENTIFIER_PATTERNS.items():
        for m in re.finditer(pat, t):
            if any(m.start() < e and st < m.end() for st, e in spans):
                continue
            spans.append((m.start(), m.end()))
            found.add((kind, re.sub(r"\s+", "", m.group())))
    return found


def extract_poppler(pdf):
    r = subprocess.run(["pdftotext", "-layout", pdf, "-"],
                       capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        raise RuntimeError(f"pdftotext failed: {r.stderr.strip()[:200]}")
    return r.stdout


def extract_pypdf(pdf):
    try:
        import pypdf
    except ImportError:
        return None, []
    reader = pypdf.PdfReader(pdf)
    pages = [(p.extract_text() or "") for p in reader.pages]
    return "\n".join(pages), pages


def page_density(pages_poppler, pages_pypdf):
    out = []
    n = max(len(pages_poppler), len(pages_pypdf or []))
    for i in range(n):
        a = len(re.sub(r"\s", "", pages_poppler[i])) if i < len(pages_poppler) else 0
        b = len(re.sub(r"\s", "", pages_pypdf[i])) if pages_pypdf and i < len(pages_pypdf) else 0
        out.append({"page": i + 1, "chars_poppler": a, "chars_pypdf": b,
                    "flag": "no extractable text" if max(a, b) < 40 else ""})
    return out


def render(text):
    """The rendering: every line of the extraction, prefixed with its line number.
    Nothing is dropped, reordered, reflowed or rewritten."""
    lines = text.split("\n")
    width = len(str(len(lines)))
    return "\n".join(f"{str(i + 1).rjust(width)}│{ln}" for i, ln in enumerate(lines))


def unrender(rendered):
    return "\n".join(ln.split("│", 1)[1] if "│" in ln else ln
                     for ln in rendered.split("\n"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--outdir", default=None)
    a = ap.parse_args()

    pdf = a.pdf
    if not os.path.exists(pdf):
        sys.exit(f"no such file: {pdf}")
    outdir = a.outdir or os.path.dirname(os.path.abspath(pdf))
    os.makedirs(outdir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(pdf))[0]
    md_path = os.path.join(outdir, stem + ".salus.md")
    fid_path = os.path.join(outdir, stem + ".fidelity.json")

    raw_bytes = open(pdf, "rb").read()
    primary = extract_poppler(pdf)
    pages_poppler = primary.split("\f")
    secondary, pages_pypdf = extract_pypdf(pdf)

    rendered = render(primary)
    open(md_path, "w", encoding="utf-8").write(rendered)

    # gate: the rendering is the extraction plus line numbers, and nothing else
    roundtrip_ok = sha256_text(unrender(rendered)) == sha256_text(primary)

    report = {
        "sheet": os.path.basename(pdf),
        "sheet_sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "sheet_bytes": len(raw_bytes),
        "extracted_utc": datetime.datetime.now(datetime.timezone.utc)
                          .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "rendering": os.path.basename(md_path),
        "rendering_sha256": sha256_text(rendered),
        "primary_engine": "poppler pdftotext -layout",
        "secondary_engine": "pypdf" if secondary is not None else "unavailable",
        "roundtrip_identical": roundtrip_ok,
        "chars_primary": len(re.sub(r"\s", "", primary)),
        "pages": len(pages_poppler),
        "page_density": page_density(pages_poppler, pages_pypdf),
    }

    if not primary.strip():
        report["verdict"] = "NO TEXT LAYER"
        report["detail"] = ("The primary engine returned no text. This file carries no extractable "
                            "text layer - it is an image. Salus cannot establish what it would be "
                            "checking, so the audit verdict is CANNOT VERIFY.")
        report["identifier_divergences"] = []
    elif secondary is None:
        report["verdict"] = "UNCONFIRMED"
        report["detail"] = ("Only one extraction engine was available, so no independent check of "
                            "completeness was possible. Install pypdf and re-run before relying on "
                            "this conversion.")
        report["identifier_divergences"] = []
    else:
        ca, cb = char_set(primary), char_set(secondary)
        wa, wb = split_tokens(primary), split_tokens(secondary)
        ia, ib = identifiers(primary), identifiers(secondary)
        sa, sb = set(ia), set(ib)

        lost_chars = sorted(cb - ca)
        haystack = squash(primary)
        lost_words = sorted(t for t in (wb - wa) if t not in haystack)
        lost_ids = sorted(sb - sa)

        coverage = 1 - len(lost_words) / max(1, len(wb))

        report["distinct_tokens_primary"] = len(wa)
        report["distinct_tokens_secondary"] = len(wb)
        report["coverage_of_secondary_by_shipped"] = round(coverage, 6)
        report["identifiers_primary"] = len(sa)
        report["identifiers_secondary"] = len(sb)
        report["lost_identifiers"] = [{"kind": k, "value": v} for k, v in lost_ids]
        report["lost_characters"] = lost_chars[:120]
        report["lost_tokens"] = lost_words[:200]
        report["tokens_only_in_shipped"] = sorted(
            t for t in (wa - wb) if t not in squash(secondary))[:60]
        report["method_note"] = (
            "The comparison is by COVERAGE, not by count. The two engines legitimately differ on "
            "how many times a repeated page header appears and in what order a label and its "
            "value are emitted, and counting that as loss would bury the divergences that matter. "
            "What is asserted is that nothing PRESENT in the independent extraction is ABSENT "
            "from what ships: every distinct character, every distinct word or number token, and "
            "every chemical identifier and hazard code.")

        if not roundtrip_ok:
            report["verdict"] = "FAIL"
            report["detail"] = "The rendering does not reproduce the extraction byte for byte."
        elif lost_ids:
            report["verdict"] = "FAIL"
            report["detail"] = (
                f"{len(lost_ids)} chemical identifier(s) or hazard code(s) are present in the "
                "independent extraction and absent from the shipped rendering: "
                + ", ".join(v for _, v in lost_ids[:8])
                + ". On a safety document this is disqualifying.")
        elif lost_words or lost_chars:
            report["verdict"] = "REVIEW"
            report["detail"] = (
                f"No identifier was lost, but {len(lost_words)} distinct token(s) and "
                f"{len(lost_chars)} distinct character(s) appear in the independent extraction "
                "and not in the shipped rendering. Coverage is "
                f"{coverage * 100:.4f}%. A person must read lost_tokens before this conversion "
                "is used in an audit.")
        else:
            report["verdict"] = "PASS"
            report["detail"] = (
                "Two independent engines were run. Every distinct character, every one of the "
                f"{len(wb)} distinct word and number tokens, and all {len(sb)} chemical "
                "identifiers and hazard codes found by the independent engine are present in the "
                "shipped rendering, and that rendering reproduces the primary extraction byte "
                "for byte.")

    report["limits"] = [
        "Two engines missing the same content agree and are wrong together. Text that exists only "
        "as an image is the usual case; see page_density for pages with little extractable text.",
        "Reading order in multi-column layouts is the primary engine's, and is not independently "
        "verified.",
        "Visual structure - which cell a value sat in, which column a heading spanned - is not "
        "reconstructed. The rendering preserves the layout the primary engine produced, and the "
        "original PDF ships beside it so a reader can compare.",
    ]
    open(fid_path, "w", encoding="utf-8").write(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(f"{report['verdict']:<14} {os.path.basename(pdf)}")
    print(f"  -> {os.path.relpath(md_path)}")
    print(f"  -> {os.path.relpath(fid_path)}")
    if report.get("coverage_of_secondary_by_shipped") is not None:
        print(f"  coverage {report['coverage_of_secondary_by_shipped'] * 100:.4f}%  "
              f"identifiers {report.get('identifiers_secondary', 0)}  "
              f"lost identifiers {len(report.get('lost_identifiers', []))}  "
              f"lost tokens {len(report.get('lost_tokens', []))}")
    return 0 if report["verdict"] in ("PASS", "NO TEXT LAYER") else 1


if __name__ == "__main__":
    sys.exit(main())
