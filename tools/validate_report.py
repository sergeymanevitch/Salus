#!/usr/bin/env python3
"""Gate 3 — is the report shaped like an audit, and did it stay inside the hard boundaries?

    python3 tools/validate_report.py <report.md>

Gate 2 checks that the report agrees with the standard. This one checks that the report is an
AUDIT at all: one of exactly three verdicts, findings that carry a provision or admit they carry
none, blind spots declared — and, above everything else, not one word of advice about the
material.

That last check is the one the whole design turns on. A user can ask Salus to approve a material.
A model under pressure can drift into answering. This gate runs afterwards, over the text, and
voids the run if the answer contains permission language. It scans English and Russian because the
conversation around this tool happens in both.

The ban list is deliberately blunt. A false positive costs a rewrite. A false negative puts the
words "safe to use" on a document that will be read by someone deciding whether to hand a drum to
a worker.
"""
import argparse, re, sys

VERDICTS = ["CONFORMS", "DOES NOT CONFORM", "CANNOT VERIFY"]

BANNED = [
    # permission and prohibition about the material itself
    (r"\bsafe to (?:use|handle|store)\b", "declares the material safe"),
    (r"\bnot safe to (?:use|handle|store)\b", "declares the material unsafe"),
    (r"\b(?:is|are) safe\b", "declares something safe"),
    (r"\b(?:is|are) (?:not safe|unsafe|dangerous|hazardous to use)\b", "declares something unsafe"),
    (r"\bdo not use (?:this|the) (?:material|product|substance|chemical)\b", "prohibits use"),
    (r"\b(?:may|can) be used (?:by|in|with|safely)\b", "permits use"),
    (r"\b(?:approved|cleared|authorised|authorized) for use\b", "grants clearance"),
    (r"\bfit for use\b", "grants clearance"),
    (r"\bwe (?:recommend|advise|suggest) (?:using|avoiding|substituting)\b", "advises on the material"),
    (r"\b(?:recommend|advise|suggest)(?:ed|s)? (?:using|avoiding|substituting|replacing) "
     r"(?:this|the|another)\b", "advises on the material"),
    (r"\bworkers? (?:may|should|must) (?:now )?(?:use|handle|not use)\b", "instructs about workers"),
    (r"\bsuitable for (?:use|workers|handling)\b", "grants clearance"),
    # Russian. These are the only non-English strings in this repository, and they are here
    # because they are the words being BANNED - the language is the point, the way a quoted
    # word is. A reviewer whose working conversation happens in Russian can still be asked,
    # in Russian, to bless a material; the boundary has to hold in the language the request
    # arrives in.
    (r"безопас(?:ен|на|но|ный|ная|ное)\b", "declares safety in Russian"),
    (r"опас(?:ен|на|но|ный|ная|ное)\s+(?:материал|продукт|веществ)", "declares danger in Russian"),
    (r"можно\s+(?:использовать|применять|работать)", "permits use in Russian"),
    (r"нельзя\s+(?:использовать|применять|работать)", "prohibits use in Russian"),
    (r"разреш(?:ено|аю|ается)\b", "grants permission in Russian"),
    (r"рекоменду(?:ю|ем|ется)\s+(?:использовать|заменить|применять)", "advises in Russian"),
]

# Places the banned words may legitimately appear: a blockquote of the sheet, a table cell
# carrying its wording, and this tool's own statements about what it will not do.
#
# NOTE ON WHAT IS *NOT* HERE. This list once carried r"^\s{4,}\S" - exempt any indented line -
# on the reasoning that indented lines are quotations. They are not. rules.md mandates that
# indentation for WHAT, WHERE, RULE and WHY, which is the whole body of every finding, so the
# exemption excused roughly three quarters of a report including the auditor's own prose in WHY.
# A report reading "This material is safe to use" inside a finding passed this gate. Quotation
# is marked by quotation marks, not by whitespace, so quoted spans are now blanked out before
# the scan (see strip_quoted) and indentation exempts nothing.
EXEMPT_CONTEXT = [
    r"^\s*>", r"^\s*\|", r"(?i)\bquote\b",
    r"(?i)salus (?:does not|never|cannot)", r"(?i)this (?:is not|does not constitute)",
    r"(?i)not a (?:release|clearance|approval)",
]


def strip_quoted(text):
    """Blank every double-quoted span, keeping line numbers and column offsets intact.

    A finding quotes the sheet and the standard verbatim, and those quotations may legitimately
    contain the very words this gate bans - a supplier's Section 7 really can say "safe to use".
    What the auditor writes AROUND the quotation may not. Blanking the quoted span rather than
    the indented block is the difference between exempting a citation and exempting the report.

    Quotes may run across lines, so the substitution is made over the whole text and newlines are
    preserved, which keeps the reported line numbers true.
    """
    out = list(text)
    for m in re.finditer(r'"[^"]*"', text, re.S):
        for i in range(m.start(), m.end()):
            if out[i] != "\n":
                out[i] = " "
    return "".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report")
    a = ap.parse_args()
    text = open(a.report, encoding="utf-8").read()
    lines = text.split("\n")
    # Scanned for banned language with every quotation blanked out. Structural checks below
    # still read `text`, because a verdict or a finding tag inside a quotation is still there.
    scan_lines = strip_quoted(text).split("\n")

    problems, notes = [], []

    found = [v for v in VERDICTS if re.search(rf"(?m)^\s*#*\s*(?:VERDICT\s*[:\-]\s*)?{v}\b", text)]
    if len(found) != 1:
        problems.append(f"expected exactly one verdict line out of {VERDICTS}; found {found or 'none'}")

    if "DOES NOT CONFORM" in found and not re.search(r"\[F-\d+\]", text):
        problems.append("verdict is DOES NOT CONFORM but the report lists no findings")
    if "CONFORMS" in found and not re.search(r"\[P-\d+\]", text):
        problems.append("verdict is CONFORMS but the report shows no checks that passed — "
                        "an audit reports what it checked, not only what broke")

    if not re.search(r"(?i)^#+\s*declared blind spots", text, re.M):
        problems.append("no 'Declared blind spots' section — identity.md requires one in every report")

    # Only a mark at the head of a line opens a finding. A tag mentioned inside a WHY
    # paragraph is a cross-reference, not a new finding.
    marks = [m.start(1) for m in re.finditer(
        r"(?m)^\s*#*\s*(\[(?:F|P)-\d+\])\s+\[(?:STANDARD|HOUSE POLICY)", text)]
    for i, start in enumerate(marks):
        tag = re.match(r"\[(?:F|P)-\d+\]", text[start:]).group()
        if tag.startswith("[P-"):
            continue
        block = text[start: marks[i + 1] if i + 1 < len(marks) else len(text)]
        has_std = "[STANDARD]" in block
        has_pol = "[HOUSE POLICY" in block
        if not (has_std or has_pol):
            problems.append(f"{tag} is marked neither [STANDARD] nor [HOUSE POLICY — no provision]")
        if has_std and has_pol:
            problems.append(f"{tag} is marked as both a standard violation and a policy gate")

    for i, (line, scanned) in enumerate(zip(lines, scan_lines), 1):
        if any(re.search(p, line) for p in EXEMPT_CONTEXT):
            continue
        for pat, why in BANNED:
            m = re.search(pat, scanned, re.I)
            if m:
                problems.append(f"line {i}: BOUNDARY BREACH — {why}: \"{m.group()}\" "
                                f"in: {line.strip()[:110]}")

    if re.search(r"(?i)\b(?:probably|likely|i think|seems|appears to be fine|looks (?:ok|fine))\b", text):
        notes.append("hedging language found — an audit states what the standard says, "
                     "or states that it could not check")

    for n in notes:
        print(f"NOTE  {n}")
    if problems:
        for p in problems:
            print(f"FAIL  {p}")
        print(f"\n{len(problems)} problem(s). This report is void and must not be delivered.")
        return 1
    print("Verdict shape is valid, every finding declares its class, blind spots are stated, "
          "and no permission language was found. The report may be delivered.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
