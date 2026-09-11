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
    # Permission and prohibition about the material itself. identity.md § Hard boundaries names
    # the words outright — "safe to use, do not use, approved, cleared, hazardous product,
    # recommend using have no place in your output IN ANY LANGUAGE" — so each of those appears
    # here in both languages this folder is worked in, and in the grammatical shapes they
    # actually arrive in: predicative ("the product is safe"), not only attributive.
    #
    # Every pattern's literal spaces are relaxed to \s+ before use (see banned_patterns), because
    # a finding is hard-wrapped at about 95 columns and a sentence about the material does not
    # stop being one when the line break lands in the middle of it.
    (r"\bsafe to (?:use|handle|store)\b", "declares the material safe"),
    (r"\bnot safe to (?:use|handle|store)\b", "declares the material unsafe"),
    # Up to two words may sit between the verb and the adjective: "is perfectly safe",
    # "is not safe". Two, not any number, so that "is the Chinese national dangerous goods
    # list" - a sentence about a document - is not read as a sentence about a material.
    (r"\b(?:is|are|was|were)(?: \w+){0,2} safe\b", "says whether something is safe"),
    (r"\b(?:is|are|was|were)(?: \w+){0,2} (?:unsafe|dangerous|harmless)\b",
     "says whether something is dangerous"),
    (r"\b(?:is|are|was|were)(?: an?)? hazardous (?:product|material|chemical|substance)\b",
     "calls the material a hazardous product"),
    (r"\bhazardous to (?:use|handle|store)\b", "declares the material unsafe"),
    (r"\bdo not (?:use|handle|store|apply)\b", "prohibits use"),
    (r"\b(?:may|can) be used (?:by|in|with|safely)\b", "permits use"),
    (r"\b(?:not )?(?:approved|cleared|authorised|authorized) for use\b",
     "rules on whether the material may be used"),
    (r"\b(?:is|are|was|were)(?: \w+){0,2} (?:approved|cleared|authorised|authorized)\b",
     "says whether something is approved or cleared"),
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
    # arrives in. Russian puts the adjective on either side of the noun and drops the verb
    # entirely - "Материал опасен" is a complete sentence - so these match the word, not a
    # word order, and the endings are listed rather than left to \w* so that опасность,
    # the ordinary noun "hazard", is not swept up with them.
    (r"безопас(?:ен|на|но|ны|ный|ная|ное|ные|ным)\b", "declares safety in Russian"),
    (r"опас(?:ен|на|но|ны|ный|ная|ное|ные|ного|ным)\b",
     "declares danger, or its absence, in Russian"),
    (r"вреден\b|вредн(?:ый|ая|ое|ые)\b", "declares harm in Russian"),
    (r"можно\s+(?:использовать|применять|работать)", "permits use in Russian"),
    (r"нельзя\s+(?:использовать|применять|работать)", "prohibits use in Russian"),
    (r"разреш(?:ен|ён|ена|ено|ены|аю|аем|ается|ить)\b", "grants permission in Russian"),
    (r"запрещ(?:ен|ён|ена|ено|ены|ается)\b", "prohibits use in Russian"),
    (r"рекоменду(?:ю|ем|ется)\s+(?:использовать|заменить|применять)", "advises in Russian"),
]


def banned_patterns():
    r"""The ban list compiled, with every literal space relaxed to \s+.

    rules.md mandates a wrapped, indented finding body, so the auditor's own sentences arrive
    broken across lines at about 95 columns and re-indented. A per-line scan of a hard-wrapped
    document reads "do not use the / material" as two lines that say nothing, which is the
    breach saying itself in the one layout this format guarantees. The scan therefore runs over
    the whole report and the patterns are told that a space may be any run of whitespace.
    """
    return [(re.compile(pat.replace(" ", r"\s+"), re.I), why) for pat, why in BANNED]


# NOTE ON WHAT IS *NOT* HERE: there is no list of exempt contexts, and there was one.
#
# It began as r"^\s{4,}\S" - exempt any indented line - on the reasoning that indented lines are
# quotations. They are not. rules.md mandates that indentation for WHAT, WHERE, RULE and WHY,
# which is the whole body of every finding, so the exemption excused roughly three quarters of a
# report including the auditor's own prose in WHY. It was replaced by a list that exempted any
# blockquote line, any table row, any line containing the word "quote", and any line carrying a
# Salus disclaimer - and every one of those was a way of saying the banned thing and being told
# the report may be delivered:
#
#     | Conclusion | the material is safe to use |          exempt: it is a table row, and the
#                                                           summary table is the first thing read
#     To quote the position plainly: the material is safe to use.    exempt: it says "quote"
#     Salus does not clear materials, but this material is safe to use.   exempt: it disclaims
#
# Exemption is marked by quotation marks and by nothing else. A supplier's Section 7 really can
# read "safe to use" and a finding has to be able to reproduce it, so quoted spans are blanked
# before the scan (see strip_quoted) and everything outside them is the auditor speaking. That
# rule is checkable by a reader, it is the same rule Gate 2 uses to find the quote it verifies,
# and it leaves an author who must name a banned phrase one honest way to do it: quote it.
#
# A blockquote is not an exemption either. A `>` line reproducing the sheet is legitimate and
# stays legitimate - with the quotation marks that say it is a reproduction. Without them a
# blockquote is indistinguishable from the auditor's own prose set one level in, and none of the
# eight shipped reports needed the exemption: measured before it was removed, not one line of
# any of them relies on it.


def strip_quoted(text):
    """Blank every double-quoted span, keeping line numbers and column offsets intact.

    A finding quotes the sheet and the standard verbatim, and those quotations may legitimately
    contain the very words this gate bans - a supplier's Section 7 really can say "safe to use".
    What the auditor writes AROUND the quotation may not. Blanking the quoted span rather than
    the indented block is the difference between exempting a citation and exempting the report.

    Quotes may run across lines, so the substitution is made over the whole text and newlines are
    preserved, which keeps the reported line numbers true.

    It blanks pairs, left to right, and that is only sound while the marks in the report pair the
    way their author meant them to. quote_integrity() below is what establishes that, and it runs
    first; this function must not be called on a report that failed it.
    """
    out = list(text)
    for m in re.finditer(r'"[^"]*"', text, re.S):
        for i in range(m.start(), m.end()):
            if out[i] != "\n":
                out[i] = " "
    return "".join(out)


def quote_integrity(text):
    """Can this report's quotation marks be paired? If not, nothing else it says is readable.

    Quotation is the only exemption from the boundary scan, so where a quotation begins and ends
    decides which sentences belong to the auditor. Pairing left to right, ONE unmatched mark -
    an inch sign, a citation cut in half, a smart quote that survived a paste - re-pairs every
    mark after it: the spans that get blanked become the auditor's own prose and the real
    quotations are handed to the scan unblanked. Measured on audits/2026-09-11-bg-hcf/report.md
    with one inch mark added to its header table, the blanked span went from 1,311 characters to
    6,291 of 9,657 - two thirds of the report, most of it the auditor's own prose - and a line
    reading "The material is safe to use in any case." went from refused to delivered.

    So an odd count is not a typo to be tolerated. It is a report this gate cannot read, and a
    gate that cannot tell quotation from assertion has no business saying a report may ship. The
    same holds for a pair that swallows a paragraph break: a verbatim quote of a sheet or a
    provision does not run across a blank line, so a span that does is a mispairing wearing the
    shape of a quotation. Both are refused, and the fix costs the author one character.
    """
    problems = []
    n = text.count('"')
    if n % 2:
        problems.append(
            f"the report carries an odd number of quotation marks ({n}) — one of them never "
            "closes, so every mark after it pairs with the wrong neighbour. Quotation is the "
            "only thing that exempts a phrase from the boundary scan, which means this gate "
            "cannot tell which sentences are the sheet's and which are Salus's, and it will not "
            "guess. Close the quotation, or write an inch mark as `in`")
        return problems          # every pair below it is suspect; one diagnosis is enough
    for m in re.finditer(r'"[^"]*"', text, re.S):
        if re.search(r"\n[ \t]*\n", m.group()):
            line = text.count("\n", 0, m.start()) + 1
            problems.append(
                f"the quotation opened at line {line} is not closed before a blank line — a "
                "verbatim quote of a sheet or of a provision does not run across a paragraph "
                "break, so these two marks are not a pair and the text between them is not a "
                "quotation. Whatever was meant to close the first one is missing")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report")
    a = ap.parse_args()
    text = open(a.report, encoding="utf-8").read()
    lines = text.split("\n")

    problems, notes = [], []

    # Can the quotation marks be paired? Everything the boundary scan decides rests on this,
    # so it is asked first and its answer changes what the scan reads. With the pairing sound,
    # quoted spans are blanked and what is left is the auditor speaking. With the pairing in
    # doubt, NOTHING is blanked: the report is already refused, and the alternative is choosing
    # which half of a report to stop reading on the strength of a mark that is in the wrong
    # place. Structural checks below read `text` either way, because a verdict or a finding tag
    # inside a quotation is still there.
    quote_problems = quote_integrity(text)
    problems.extend(quote_problems)
    scan = text if quote_problems else strip_quoted(text)

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
    # The direction that matters, and the one this gate went without: CONFORMS is what a report
    # says when nothing failed. rules.md § Severity: "severity never changes the verdict — any
    # finding of either class produces DOES NOT CONFORM." A CONFORMS report carrying four
    # BLOCKING findings is not a shape error, it is the verdict being overruled by its own
    # contents, which is the one way a report can pass this gate and still tell a reader the
    # opposite of what it found.
    if "CONFORMS" in found and re.search(r"(?m)^\s*#*\s*\[F-\d+\]", text):
        problems.append("verdict is CONFORMS but the report lists findings — "
                        "any finding of either class produces DOES NOT CONFORM")

    # Declared blind spots, and what is under the heading. identity.md does not ask for the
    # heading; it asks for the declarations - "State these in every report, under this heading,
    # whether or not they bit on this run." A heading with nothing beneath it is the opposite of
    # what it announces: it tells a reader the limits were stated where they were not.
    blind = re.search(r"(?im)^#+[ \t]*declared blind spots[^\n]*\n", text)
    if not blind:
        problems.append("no 'Declared blind spots' section — identity.md requires one in every report")
    else:
        rest = text[blind.end():]
        nxt = re.search(r"(?m)^#", rest)
        body = rest[:nxt.start()] if nxt else rest
        stated = [ln for ln in body.split("\n") if ln.strip()]
        if len(stated) < 3:
            problems.append(
                f"the 'Declared blind spots' heading carries {len(stated)} line(s) under it — "
                "identity.md lists what an auditor holding two rulebooks cannot see, and asks "
                "for those declarations in every report, whether or not they bit on this run. "
                "The heading is not the declaration; an empty one says the limits were stated "
                "when they were not")

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
        # The block opened at a mark that already carried one of the two classes, so asking
        # whether it carries either is a question with one answer. What is worth asking is
        # whether it carries BOTH: rules.md § Two classes of finding, never mixed — a reader has
        # to be able to tell at a glance which findings the law requires and which this
        # installation does, and the two carry different weight with a supplier.
        if "[STANDARD]" in block and "[HOUSE POLICY" in block:
            problems.append(f"{tag} is marked as both a standard violation and a policy gate")

    # And the findings the scan above cannot see. It only recognises a tag that is FOLLOWED by
    # its class, so a heading that drops the class marker - "### [F-05] BLOCKING — ..." - is not
    # read as a finding at all: not by this gate, and not by Gate 2, which means nothing checks
    # that it names a provision, quotes it, or cites a file. The block becomes a paragraph of
    # free text wearing a finding's number. So the tags are counted independently and any tag
    # the class scan did not also find is reported here.
    #
    # "At the head of a line" is narrowed for this scan to a heading or an unindented line, and
    # a tag followed by sentence punctuation is excluded, because the mandated 95-column wrap
    # puts ordinary cross-references at the start of a line: `  [P-04].` closing a sentence in a
    # blind-spots bullet is a real line of a shipped report, not a finding that lost its class.
    classed = set(marks)
    for m in re.finditer(r"(?m)^ {0,3}(?:#{1,6} *)?(\[(?:F|P)-\d+\])(?![.,;:)])", text):
        if m.start(1) in classed:
            continue
        line = text.count("\n", 0, m.start(1)) + 1
        problems.append(
            f"line {line}: {m.group(1)} opens a block and declares no class — rules.md allows "
            "two, [STANDARD] with the provision it fails, or [HOUSE POLICY — no provision] "
            "saying it has none. A finding that names neither is invisible to this gate and to "
            "Gate 2, so nothing checks that it cites anything at all, and a reader cannot tell "
            "whether the law requires it or this installation does")

    # The boundary scan. It runs over the whole report at once rather than line by line - see
    # banned_patterns() for why a line is the wrong unit - and the line number is recovered from
    # the offset of the match so the failure still names a place to go and fix.
    breaches = []
    for pat, why in banned_patterns():
        for m in pat.finditer(scan):
            line = scan.count("\n", 0, m.start()) + 1
            said = " ".join(m.group().split())
            breaches.append((line, m.start(), f"line {line}: BOUNDARY BREACH — {why}: "
                                              f"\"{said}\" in: {lines[line - 1].strip()[:110]}"))
    seen = set()
    for line, _, message in sorted(breaches):
        if message not in seen:
            seen.add(message)
            problems.append(message)

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
    print(f"The verdict is one of the three and agrees with what the report lists, the run "
          f"declares jurisdiction {regime} and applies that regime's standard, every finding tag "
          f"declares its class, the blind spots are declared under their heading, the quotation "
          f"marks pair — and outside them, where the auditor is the one speaking, no permission "
          f"language was found. The report may be delivered.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
