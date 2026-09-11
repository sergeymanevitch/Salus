#!/usr/bin/env python3
"""Gate 1 — is the shipped rendering of a sheet faithful to the PDF?

    python3 tools/verify_conversion.py <sheet.pdf> [--outdir DIR] [--strict]

This does not read the fidelity report that extract.py wrote. It re-derives the answer from the
PDF and from the rendering on disk, so a stale or edited report cannot pass the gate. Exit code 0
means the rendering may be used in an audit.

It re-derives it by calling the same comparison `extract.py` used — `extract.compare()` — rather
than by carrying a second copy of it. That is deliberate and it is the fix for a real defect: the
second copy that lived here checked tokens and identifiers and had quietly lost the character
check, so a rendering that dropped `µ` from "49.9 µg/kg dw", or `≥` from "≥25 - ≤50 %", was REVIEW
in the fidelity report and PASS at the gate. Re-deriving means running the same question against
different INPUTS — the PDF and the file on disk, not the JSON — not asking a different question.

WHAT THIS GATE IS FOR. It is the enforcement of `rules.md` Stage 1a. Three of its answers end a
run there:

    NO TEXT LAYER  the PDF has no extractable text at all. Nothing was compared, because there was
                   nothing to compare, and two empty extractions are equal — which is how this
                   gate once printed PASS on a scanned sheet under --strict. Stage 1a: CANNOT
                   VERIFY, stop.
    FAIL           the rendering on disk is no longer the extraction, or an identifier the
                   independent engine found is missing from it.
    UNCONFIRMED    the independent engine could not run, so completeness was not checked. This is
                   a statement about the check, not about the sheet, and it is not a pass.

Without --strict, REVIEW is allowed through and printed loudly. With --strict, only PASS passes.

EXIT CODES. 0 — PASS, or REVIEW without --strict. 1 — every other verdict. 2 — there is no
rendering on disk to check, which is a mistake in the run, not an answer about the sheet.
`extract.py` deliberately exits 0 on all of these; the gate is the one place the verdict decides
anything. See `tools/CONTEXT.md` § Conventions.
"""
import argparse, os, sys

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

    try:
        primary = X.extract_poppler(a.pdf)
    except RuntimeError as e:
        # The same installation problem, told the same way. This gate is the one a judge runs
        # first, so it is the one that must not answer a missing program with a stack trace.
        sys.exit(f"FAIL  {e}")
    secondary, _ = X.extract_pypdf(a.pdf)
    shipped = open(md, encoding="utf-8").read()

    has_text = bool(primary.strip())
    roundtrip_ok = X.sha256_text(X.unrender(shipped)) == X.sha256_text(primary)
    comp = X.compare(primary, secondary) if (has_text and secondary is not None) else None
    verdict = X.fidelity_verdict(has_text, roundtrip_ok, secondary is not None, comp)

    lost_ids = comp["lost_identifiers"] if comp else []
    lost_tokens = comp["lost_tokens"] if comp else []
    lost_chars = comp["lost_characters"] if comp else []

    print(f"{verdict}  {os.path.basename(a.pdf)}")

    if not has_text:
        print("  ! this PDF has no extractable text layer — the primary engine returned nothing, "
              "so nothing was compared")
        print(f"    The rendering is {len(shipped)} character(s). A gate that compares two empty "
              "extractions and finds them equal has proved nothing; it is not a pass.")
        print("    rules.md Stage 1a: no text layer → CANNOT VERIFY, and the run stops here. "
              "The sheet is not thereby defective — it is unreadable by this auditor.")
        if secondary and secondary.strip():
            print("    ! and the independent engine DID find text here. The two engines disagree "
                  "about whether this PDF has a text layer at all, and the rendering that ships "
                  "is the empty one. That is a conversion to fix, not a sheet to re-file.")
    if not roundtrip_ok:
        print("  ! the rendering on disk no longer reproduces the extraction byte for byte — it "
              "has been edited, or the PDF has changed since it was made")
    if secondary is None and has_text:
        print("  ! the independent engine could not run — completeness was NOT independently "
              "checked. Nothing here says the rendering is incomplete, and nothing here says it "
              "is complete. Resolve it before this conversion is used in an audit.")
    if lost_ids:
        print("  ! chemical identifiers present in the independent extraction and missing from "
              "the rendering: " + ", ".join(d["value"] for d in lost_ids))
        print("    On a safety document a lost CAS number or hazard code is disqualifying.")
    if lost_chars:
        print(f"  ? {len(lost_chars)} character(s) in the independent extraction appear nowhere "
              f"in the rendering: {' '.join(lost_chars[:20])}")
        print("    A character is not a typographic detail on a safety sheet. Losing µ turns a "
              "microgram into a gram; losing ≥ or ≤ turns a concentration band into a number.")
    if lost_tokens:
        print(f"  ? {len(lost_tokens)} token(s) in the independent extraction are not adjacent "
              f"anywhere in the rendering: {', '.join(lost_tokens[:10])}")
        print("    Usually this is the two engines reading a table in a different order. "
              "A person must look before the rendering is used.")
    if verdict == "PASS":
        print("  rendering reproduces the extraction byte for byte; every distinct character, "
              "token and chemical identifier the independent engine found is present in it")
    return 0 if verdict == "PASS" or (verdict == "REVIEW" and not a.strict) else 1


if __name__ == "__main__":
    sys.exit(main())
