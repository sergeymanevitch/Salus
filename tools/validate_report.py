#!/usr/bin/env python3
"""Gate 3 — is the report shaped like an audit, and did it stay inside the hard boundaries?

    python3 tools/validate_report.py <report.md>

Gate 2 checks that the report agrees with the standard. This one checks that the report is an
AUDIT at all: one of exactly three verdicts, findings that carry a provision or admit they carry
none, the regime named in the header, blind spots declared — and, above everything else, not one
word of advice about the material.

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

REGIMES = ("EU", "US")

# The header row every report carries, and the row this gate reads the regime out of. It is the
# same row tools/verify_citations.py reads, and it is read from the REPORT rather than from
# config/jurisdiction.md for the reason set out at length in that file's report_jurisdiction():
# a filed report keeps the regime it was made under, and audits/ holds reports of both regimes
# that are checked together against a config file that can only say one thing.
JURIS_ROW = re.compile(r"(?mi)^\s*\|\s*Jurisdiction\b[^|]*\|\s*([^|]*?)\s*\|")
STANDARD_ROW = re.compile(r"(?mi)^\s*\|\s*Standard applied\b[^|]*\|\s*([^|]*?)\s*\|")

# What the "Standard applied" row may not name, per regime. The citation-level version of this
# rule lives in Gate 2, which reads the provisions a finding stands on. This is the header-level
# version: a report may declare one regime at the top of its table and claim the other regime's
# rulebook one line below, and no finding has to be wrong for that to be a lie about the run.
FOREIGN_STANDARD = {
    "US": [(r"2020/\s?878", "Commission Regulation (EU) 2020/878"),
           (r"1907/\s?2006", "Regulation (EC) No 1907/2006 (REACH)"),
           (r"(?i)\bCLP\b|Annex\s*VI", "CLP Annex VI")],
    "EU": [(r"1910\.1200", "29 CFR 1910.1200"),
           (r"(?i)Hazard Communication", "the OSHA Hazard Communication Standard")],
}

# rules.md Stage 5 and identity.md, in the auditor's own words: under jurisdiction: US there is no
# harmonised classification list to check Section 3 against, so none is checked and the report has
# to say so. Stated in two files and enforced in none, until this line.
US_CLASSIFICATION_PHRASE = re.compile(r"(?i)not\s+assessed\s+for\s+classification\s+correctness")


def report_jurisdiction(text):
    """The regime named in the report's header table, or None and the reason it could not be read."""
    rows = [re.sub(r"[*`_\s]", "", v).upper() for v in JURIS_ROW.findall(text)]
    if not rows:
        return None, ("the header table declares no jurisdiction — audits/CONTEXT.md requires the "
                      "row `| Jurisdiction (from `config/jurisdiction.md`) | EU |`, or US. A "
                      "report that does not say which regime it was made under cannot be read "
                      "against the right rulebook by anyone, and cannot be checked against it "
                      "by Gate 2")
    if len(set(rows)) > 1:
        return None, ("the header declares more than one jurisdiction: "
                      + ", ".join(sorted(set(rows))) + " — a run is made under one regime")
    if rows[0] not in REGIMES:
        return None, (f"the header declares jurisdiction `{rows[0]}`, which is not a regime Salus "
                      f"ships. The two are EU and US")
    return rows[0], None

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

    # A pass is part of the report, and it is part of every report that performed checks - not
    # only of the ones that passed them all. Until 2026-09-11 this was asked of CONFORMS alone,
    # so a DOES NOT CONFORM report listing nothing but failures satisfied the gate. That is the
    # failure mode the brief names outright: a report that only lists problems is a critique.
    #
    # It is asked in BLOCK form - a mark at the head of a line, carrying its class - because a
    # bare "- [P-01] looked fine" bullet is invisible to split_findings() and to Gate 2, so a
    # test for the bare tag would have let the format ask less of the less rigorous author.
    #
    # CANNOT VERIFY is exempt, and must be: that verdict means no check was performed, so there
    # is nothing that held. For the same reason it may carry no failures either.
    performed_checks = [v for v in found if v in ("CONFORMS", "DOES NOT CONFORM")]
    block_passes = re.search(r"(?m)^\s*#*\s*\[P-\d+\]\s+\[(?:STANDARD|HOUSE POLICY)", text)
    if performed_checks and not block_passes:
        problems.append(f"verdict is {performed_checks[0]} but the report shows no check that "
                        "passed, in the form a pass is written — an audit reports what it "
                        "checked, not only what broke")
    if "CANNOT VERIFY" in found and re.search(r"(?m)^\s*#*\s*\[F-\d+\]", text):
        problems.append("verdict is CANNOT VERIFY but the report lists findings — that verdict "
                        "says no check was performed, and a finding is the record of one")

    if not re.search(r"(?i)^#+\s*declared blind spots", text, re.M):
        problems.append("no 'Declared blind spots' section — identity.md requires one in every report")

    # Jurisdiction. Which regime a report was run under is part of its shape, not a detail of its
    # prose: it decides which rulebook the findings may stand on, and Gate 2 cannot enforce that
    # rule on a report that does not name a regime.
    regime, juris_problem = report_jurisdiction(text)
    if juris_problem:
        problems.append(juris_problem)
    else:
        applied = STANDARD_ROW.search(text)
        for pat, name in FOREIGN_STANDARD[regime]:
            if applied and re.search(pat, applied.group(1)):
                problems.append(
                    f"the header declares jurisdiction {regime} but the 'Standard applied' row "
                    f"names {name}, which is the other regime's rulebook: "
                    f"\"{applied.group(1).strip()[:90]}\". A run applies one standard, the one "
                    f"config/jurisdiction.md selected, and the report says which")
                break
        # A US run checks no classification at all and must record that it did not. The sentence
        # is not decoration: Section 3 is where sheets fail most often on an EU run, and a US
        # report that says nothing about it reads as though Section 3 had been checked and held.
        if regime == "US" and performed_checks and not US_CLASSIFICATION_PHRASE.search(text):
            problems.append(
                "this is a US run that performed checks, and it nowhere records Section 3 as "
                "'not assessed for classification correctness' — 29 CFR 1910.1200 publishes no "
                "harmonised classification list and none is shipped for it, so no classification "
                "was checked (rules.md Stage 5, identity.md blind spots). A report that omits "
                "that reads as though Section 3 had been checked and held")

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
    print(f"Verdict shape is valid, the run declares jurisdiction {regime} and applies that "
          f"regime's standard, every finding declares its class, blind spots are stated, and no "
          f"permission language was found. The report may be delivered.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
