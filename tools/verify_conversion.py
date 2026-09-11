#!/usr/bin/env python3
"""Gate 1 — is the shipped rendering of a sheet faithful to the PDF?

    python3 tools/verify_conversion.py <sheet.pdf> [--outdir DIR] [--strict]

This does not read the fidelity report that extract.py wrote. It re-derives the answer from the
PDF and from the rendering on disk, so a stale or edited report cannot pass the gate. Exit code 0
means the rendering may be used in an audit.

Without --strict, REVIEW is allowed through and printed loudly. With --strict, only PASS passes.
"""
import argparse, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import extract as X  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()

    outdir = a.outdir or os.path.dirname(os.path.abspath(a.pdf))
    stem = os.path.splitext(os.path.basename(a.pdf))[0]
    md = os.path.join(outdir, stem + ".salus.md")
    if not os.path.exists(md):
        print(f"FAIL  no rendering at {md} — run tools/extract.py first")
        return 2

    primary = X.extract_poppler(a.pdf)
    secondary, _ = X.extract_pypdf(a.pdf)
    shipped = open(md, encoding="utf-8").read()

    problems = []
    if X.sha256_text(X.unrender(shipped)) != X.sha256_text(primary):
        problems.append("the rendering on disk no longer reproduces the extraction byte for byte")

    if secondary is None:
        problems.append("pypdf unavailable — completeness could not be independently checked")
        lost_ids, lost_tokens = [], []
    else:
        lost_ids = sorted(X.identifiers(secondary) - X.identifiers(primary))
        hay = X.squash(primary)
        lost_tokens = sorted(t for t in (X.split_tokens(secondary) - X.split_tokens(primary))
                             if t not in hay)
        if lost_ids:
            problems.append("chemical identifiers lost: " + ", ".join(v for _, v in lost_ids))

    verdict = "FAIL" if problems else ("REVIEW" if lost_tokens else "PASS")
    print(f"{verdict}  {os.path.basename(a.pdf)}")
    for p in problems:
        print("  ! " + p)
    if lost_tokens:
        print(f"  ? {len(lost_tokens)} token(s) in the independent extraction are not adjacent "
              f"anywhere in the rendering: {', '.join(lost_tokens[:10])}")
        print("    Usually this is the two engines reading a table in a different order. "
              "A person must look before the rendering is used.")
    if verdict == "PASS":
        print("  rendering reproduces the extraction byte for byte; nothing the independent "
              "engine found is missing from it")
    return 0 if verdict == "PASS" or (verdict == "REVIEW" and not a.strict) else 1


if __name__ == "__main__":
    sys.exit(main())
