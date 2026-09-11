#!/usr/bin/env python3
"""Gate 2 — does every citation in a report exist, and does the quoted text match the standard?

    python3 tools/verify_citations.py <report.md> [--reference <dir>] [--config <jurisdiction.md>]

Run it from anywhere. The answer does not depend on your working directory: see REPO_ROOT below.

This is the gate that reads the AUDITOR'S OWN OUTPUT. A checker that only proves the reference
folder still says what it said proves nothing about the report: it would pass a report whose
findings had drifted away from the text they cite. So this one works the other way round. It
parses each finding out of the report, pulls the quoted provision text out of it, and looks for
that text in the file the finding names. If the report and the standard disagree, the standard
wins and the gate fails.

To see it work, change one character inside a quoted RULE string in a report and re-run.

Before any finding is checked: every [F-n] and [P-n] heading in the report carries its class
marker. A heading without one is not a finding to this gate, so nothing under it would be read and
the report would leave here with the counts of a shorter report it is not.

Checks, per finding:
  1. the five required parts are present, each with something written under it - a label with an
     empty body is a missing part, not a present one
  2. every reference/ path named exists
  3. every reference/ path named belongs to the corpus the report's own regime may cite
  4. every quoted string in RULE occurs verbatim in one of those files, at any length: "Carc. 1B"
     and "H350" are checked exactly as a whole sentence is
  5. the revision named matches reference/STANDARDS-LEDGER.md
  6. a confirmation date is present and matches the ledger

Check 3 is the corpus rule, and until 2026-09-11 it was a rule nobody enforced. An EU run may
cite Annex II and CLP Annex VI; a US run may cite 29 CFR 1910.1200 and nothing else. A finding
that stands on Annex VI in a US report stands on a regulation that does not govern the sheet -
which is the false finding this whole folder is built to prevent. It was written here once, found
by hand in an architecture review and fixed by hand. A rule fixed by hand can be broken again by
hand, and a reader cannot tell "the auditor obeyed the rule" from "the rule happened to hold".

A finding marked [HOUSE POLICY - no provision] is held to a different rule, not a weaker one: it
must state in BOTH its RULE and its WHERE IN THE STANDARD that no provision exists. A policy gate
that quietly omits its citation and one that declares it has none look identical to a script that
only counts citations, and they are not the same thing at all.

Before any of that, this runs tools/verify_reference.py over the corpus it is about to quote
against. Check 3 says the quoted provision appears in the standard, and that sentence means
nothing unless the standard is the one that was downloaded: edit a date in reference/ and this
gate would confirm the edit and fail the report for disagreeing with it. Verifying the whole
corpus costs about 5 ms against this gate's own ~130 ms, and the corpus is read into memory here
anyway, so the check is unconditional — there is no flag to skip it. If it fails, this gate stops
and says so, rather than blaming a report that may be perfectly correct.
"""
import argparse, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_reference as R  # noqa: E402

REQUIRED = ["WHAT", "WHERE", "RULE", "WHERE IN THE STANDARD", "WHY"]

# The Salus folder, derived from this script's own location - tools/ sits at the root, so the root
# is one directory up from this file. A path named in a finding,
# `reference/eu-2020-878/regulation-2020-878.md`, is named relative to THAT folder. It is not
# relative to whoever ran the gate, and resolving it against the caller's working directory is how
# this gate once reported twenty-six failures in a report that has none, to anyone who ran it from
# anywhere but the root - accusing the report of a defect it did not have, which is the one thing a
# gate must never do.
#
# The other candidate anchor was the report's own directory, and it is rejected deliberately: a
# report may legitimately live outside this repository - a judge auditing their own sheet in /tmp
# and pointing the gate at it - and anchoring there would leave that run with no corpus, or with
# whatever corpus happened to sit beside the report. The standards this gate checks against are the
# ones that ship with the gate. realpath, not abspath, so the anchor survives a symlink on PATH.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def norm_ws(s):
    return re.sub(r"\s+", " ", s.replace(" ", " ")).strip()


# Files that live under reference/ but are ABOUT the corpus rather than part of it: this
# folder's own routing, its provenance hashes, its calendar. A finding cites a provision, and
# none of these is one. Loaded as if they were, the gate's claim collapses from "the quoted
# provision appears in the standard" to "the quoted string appears in some markdown we ship" -
# and a finding quoting this repository's own prose passes as a regulatory citation.
NOT_A_STANDARD = {
    "CONTEXT.md", "README.md", "PROVENANCE.md", "STANDARDS-LEDGER.md", "FRESHNESS-LOG.md",
}


# Which corpus a report of each regime is entitled to cite. identity.md, config/CONTEXT.md and
# rules.md Stage 5 all say the same thing in prose; this dict is the same thing said mechanically.
#
# ca-prop-65 is the odd one and it is deliberate. It is not a hazard-communication rulebook and it
# is not a third regime: Proposition 65 is California warning law, and 29 CFR 1910.1200(a)(2)
# preempts state rules on THIS subject while leaving a rule on another subject alone. So it is
# citable on a US run, where a sheet's Section 15 may carry a Prop 65 statement, and refused on an
# EU one, where no finding can rest on it. What it cannot do is decide whether a substance is
# listed: the OEHHA list is not in reference/, and reference/ca-prop-65/CONTEXT.md says so.
CORPUS = {
    "EU": ("reference/eu-2020-878/", "reference/eu-clp-annex-vi/"),
    "US": ("reference/us-osha-hcs/", "reference/ca-prop-65/"),
}
CORPUS_OWNER = {
    "reference/eu-2020-878/": "EU", "reference/eu-clp-annex-vi/": "EU",
    "reference/us-osha-hcs/": "US", "reference/ca-prop-65/": "US",
}
# Why each crossing is wrong, said in the terms of the regime it is wrong in. A gate that only
# reported "wrong folder" would leave the reader to work out what the violation means.
WHY_CROSS = {
    ("US", "reference/eu-clp-annex-vi/"):
        "29 CFR 1910.1200 carries no harmonised classification list and none is shipped for it, "
        "so a US run performs no classification check at all and records Section 3 as not "
        "assessed for classification correctness (rules.md Stage 5). A finding standing on "
        "Annex VI stands on a regulation that does not govern this sheet.",
    ("US", "reference/eu-2020-878/"):
        "Annex II binds a supplier placing a substance on the EU market. It obliges the preparer "
        "of a US sheet to nothing, and a defect measured against it is not a defect this report "
        "may report.",
    ("EU", "reference/us-osha-hcs/"):
        "A US-format sheet audited under jurisdiction: EU is a finding at rules.md Stage 3 - that "
        "it does not meet Annex II. The finding is written against Annex II, which is the "
        "obligation that was not met. 1910.1200 is not an obligation anyone here is owed.",
}

JURIS_ROW = re.compile(r"(?mi)^\s*\|\s*Jurisdiction\b[^|]*\|\s*([^|]*?)\s*\|")


def report_jurisdiction(text):
    """The regime this report was run under, read out of the report's own header table.

    WHY THE REPORT AND NOT config/jurisdiction.md, WHEN THE TWO DISAGREE.

    The config file is the source of truth for a RUN. rules.md Stage 0 reads it before the sheet
    is opened, and tools/check_scope.py reads it because it is deciding about a live sheet in a
    live run. This gate is not doing that. It is deciding about a FILED REPORT, and a report is a
    self-contained record: it names, in its header, on a line a reader reads, the regime it was
    audited under. That declaration is the evidence of what the run was, and it does not change
    when the setting changes afterwards.

    Trusting the config here would break the folder on a fresh clone. audits/ holds reports of
    both regimes - seven EU and one US - and they are checked together, by one command, against
    one config file that can only say one thing. A judge who clones this repository with
    `jurisdiction: EU` set and runs the gates over audits/ would watch the US report fail for
    citing OSHA, and setting the config to US would light up the other seven instead. Every filed
    report of the other regime failing on every fresh clone is a worse defect than the one this
    check closes, and it would train a reader to ignore the gate.

    The config is still read, and a disagreement is still reported - as a NOTE, naming both files.
    During a live run that note is the auditor being told the header and the setting have parted
    company. Afterwards it is the harmless fact that the installation has been reconfigured since.

    A report that declares NOTHING is a failure, not a fallback to the config. Silence here is not
    an absence of information, it is the removal of the one thing that makes the corpus rule
    enforceable: if a missing row meant "check it against the config", or "do not check it", then
    deleting one line from a header would be enough to cite any regulation in the folder against
    any sheet. A guard that can be switched off by the document it guards is not a guard.
    """
    rows = [re.sub(r"[*`_\s]", "", v).upper() for v in JURIS_ROW.findall(text)]
    if not rows:
        return None, ("this report declares no jurisdiction. Its header table must carry the row "
                      "`| Jurisdiction (from `config/jurisdiction.md`) | EU |`, or the same with "
                      "US - see audits/CONTEXT.md. Without it this gate cannot tell which corpus "
                      "the report was entitled to cite, and the rule that a US run may not cite "
                      "CLP Annex VI stops being enforceable")
    if len(set(rows)) > 1:
        return None, ("this report declares more than one jurisdiction: "
                      + ", ".join(sorted(set(rows)))
                      + ". A run is made under one regime, named once in the header")
    if rows[0] not in CORPUS:
        return None, (f"this report declares jurisdiction `{rows[0]}`, which is not a regime "
                      f"Salus ships. The two are EU and US, and there is no third value")
    return rows[0], None


def config_jurisdiction(path):
    """What the installation is set to now. Read for the cross-check only, never as authority
    over a filed report - see report_jurisdiction()."""
    if not os.path.exists(path):
        return None
    text = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r"(?m)^\s*jurisdiction:\s*([A-Za-z]+)", text)
    return m.group(1).upper() if m else None


def load_reference(refdir):
    """Key every file by its path relative to the folder that CONTAINS the corpus, so the keys read
    the way a finding writes them - `reference/eu-2020-878/regulation-2020-878.md` - from any
    working directory, and so an explicit --reference elsewhere is keyed the same way."""
    base = os.path.dirname(os.path.abspath(refdir))
    files, bookkeeping = {}, set()
    for root, _, names in os.walk(refdir):
        for n in names:
            if not n.endswith(".md"):
                continue
            full = os.path.join(root, n)
            p = os.path.relpath(full, base).replace(os.sep, "/")
            if n in NOT_A_STANDARD:
                bookkeeping.add(p)
                continue
            files[p] = norm_ws(open(full, encoding="utf-8", errors="replace").read())
    return files, bookkeeping


# One heading pattern, read two ways. The group is the tag, so a heading found by either scan
# reports the same name, and the second scan is the first one with its class marker taken off.
HEADING = r"(?m)^\s*#*\s*(\[(?:F|P)-\d+\])"
CLASSED = HEADING + r"\s+\[(?:STANDARD|HOUSE POLICY)"


def split_findings(text):
    """A finding heading is a line-leading tag followed by its class marker, as in
    '### [F-03] [STANDARD] ...'. A bare tag at the head of a list item is a cross-reference
    and must not open a new block."""
    marks = [m.start() for m in re.finditer(CLASSED, text)]
    out = []
    for i, s in enumerate(marks):
        e = marks[i + 1] if i + 1 < len(marks) else len(text)
        out.append(text[s:e])
    return out


def unclassed_tags(text):
    """Tags that open a block of their own and carry no class marker.

    split_findings() recognises a finding by tag AND class marker together, which is right - a
    bare tag at the head of a list item is a cross-reference, not a new finding. But it means a
    heading that simply omits the marker is not a finding as far as every check below is
    concerned: no RULE is read, no provision is looked for, no reference/ path, no revision, no
    date. The block is not failed, it is not seen, and the report leaves this gate with the same
    counts as if the block had never been written. One missing marker and a finding ships
    unchecked.

    So the tags are scanned a second time on their own, and any tag that opens a line without a
    marker behind it is a failure. The two classes carry different weight in a conversation with a
    supplier (rules.md, "Two classes of finding, never mixed"), so an unmarked finding is not a
    formatting slip: it is a finding a reader cannot place.
    """
    classed = {m.group(1) for m in re.finditer(CLASSED, text)}
    seen, out = set(), []
    for m in re.finditer(HEADING, text):
        tag = m.group(1)
        if tag in classed or tag in seen:
            continue
        seen.add(tag)
        line = text[text.rfind("\n", 0, m.start(1)) + 1:].split("\n")[0].strip()
        out.append((tag, line))
    return out


def field(block, name):
    r"""Pull one named part out of a finding block.

    WHERE and WHERE IN THE STANDARD are different parts and one is a prefix of the other, so
    `^\s*WHERE\b` matches the heading of BOTH - \b sits happily in the space before "IN". Left
    unguarded, a finding carrying only WHERE IN THE STANDARD satisfies the requirement for WHERE
    as well, and the five required parts are enforced as four. The part that goes missing is the
    one that locates the defect in the sheet, which is the half of a finding a reader cannot
    reconstruct from the standard.

    A part ends at the next part, at the next markdown heading, at a horizontal rule, or at the
    end of the block - the last three because the LAST part of a finding, usually WHY, is
    otherwise bounded only by the next finding, and swallows whatever prose sits between them.
    Read that way an emptied WHY at the foot of the findings list has the section break below it
    for a body, and a part that is blank on the page tests as present.
    """
    guard = r"(?! IN THE STANDARD\b)" if name == "WHERE" else ""
    stop = ("|".join(re.escape(r) for r in REQUIRED))
    m = re.search(rf"(?m)^\s*{re.escape(name)}\b{guard}[:\s]*(.*?)"
                  rf"(?=^\s*(?:{stop})\b|^\s*#{{1,6}}\s|^\s*(?:---|___|\*\*\*)\s*$|\Z)",
                  block, re.S)
    return m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report")
    ap.add_argument("--reference", default=None,
                    help="corpus to check the report against; defaults to reference/ beside this "
                         "script. An explicit path is resolved against YOUR working directory.")
    ap.add_argument("--config", default=None,
                    help="read only to cross-check the report's own declaration; defaults to "
                         "config/jurisdiction.md beside this script")
    a = ap.parse_args()

    # An explicit --reference is a path the caller typed, so it is resolved the caller's way. The
    # default is not - it is this folder's own corpus, and it is found where this folder keeps it.
    refdir = os.path.abspath(a.reference) if a.reference else os.path.join(REPO_ROOT, "reference")
    if not os.path.isdir(refdir):
        # Said once, plainly. Without this the corpus simply loads empty and every finding in a
        # correct report is accused of citing a file that does not exist - the failure mode this
        # gate was fixed for, wearing a different hat.
        print(f"FAIL  no reference corpus at {refdir} \u2014 there is nothing to check the report "
              f"against. Pass --reference if it lives elsewhere.")
        return 1

    # Gate 0 before this gate: the standards on disk must be the ones build_reference.py generated.
    # This gate's claim is "the quoted provision appears in the standard", and it is worth exactly
    # what the standard being unmodified is worth. ~4% of this run's cost; there is no skip flag,
    # because a bypass would put the corpus back into prose.
    problems, stats = R.audit(refdir)
    if problems or not stats["provenance_files"]:
        for p in problems:
            print(f"FAIL  {p}")
        if not problems:
            print(f"FAIL  nothing under {refdir}/ records how it was generated \u2014 there is no "
                  f"PROVENANCE.md to check the standards against")
        print("\nThis gate checks a report against the standard it cites. The standard is not the "
              "one that was generated, so it cannot answer. Restore reference/ with git, or "
              "rebuild it, and run again. Details: python3 tools/verify_reference.py")
        return 1
    print(f"reference corpus verified: {stats['verified']} generated file(s) across "
          f"{stats['provenance_files']} standard(s) match tools/build_reference.py's hashes.\n")

    # The report is the caller's argument, relative or absolute, and is opened as given.
    report = open(a.report, encoding="utf-8").read()

    regime, problem = report_jurisdiction(report)
    if problem:
        print(f"FAIL  {problem}.")
        print("\nThe report does not say which rulebook it was entitled to open, so this gate "
              "cannot check that\nit stayed inside it.")
        return 1
    allowed = CORPUS[regime]
    configpath = os.path.abspath(a.config) if a.config else os.path.join(REPO_ROOT, "config", "jurisdiction.md")
    configured = config_jurisdiction(configpath)
    if configured and configured != regime:
        print(f"NOTE  this report declares {regime}; {configpath} currently reads {configured}. The "
              f"report is checked\n      against {regime}, the regime it names, because a filed "
              f"report keeps the regime it was made under\n      and a setting can be changed "
              f"afterwards. If this report is being written right now, the header\n      and the "
              f"setting disagree and one of the two is wrong.\n")

    ref, bookkeeping = load_reference(refdir)
    ledger_path = os.path.join(refdir, "STANDARDS-LEDGER.md")
    ledger = norm_ws(open(ledger_path, encoding="utf-8").read()) if os.path.exists(ledger_path) else ""

    findings = split_findings(report)

    # Before anything is counted: is every finding in this report visible to the checks below?
    unclassed = unclassed_tags(report)
    if unclassed:
        for tag, line in unclassed:
            print(f"FAIL  {tag}  heads a block and names no class. A finding heading reads "
                  f"`{tag} [STANDARD] ...`\n      or `{tag} [HOUSE POLICY \u2014 no provision] "
                  f"...`, and the marker is what this gate reads a\n      finding by. Without it "
                  f"the block below is not checked at all \u2014 not its RULE, not the\n      "
                  f"provision it stands on, not the revision or the date \u2014 and this gate "
                  f"reports the same\n      counts as if it had never been written.")
            print(f"      the heading as written: {line}")
        print("\nA reader has to be able to tell at a glance which findings the law requires and "
              "which this\ninstallation requires: the two carry different weight in a "
              "conversation with a supplier\n(rules.md, \u201cTwo classes of finding, never "
              "mixed\u201d). Mark every finding, then run this again.")
        return 1

    if not findings:
        # A CANNOT VERIFY report has no findings by design: the audit stopped before any
        # provision was applied, so there is nothing to cite and citing anything would be
        # the error. Any other verdict with no findings is a broken report.
        if re.search(r"(?m)^\s*#*\s*(?:VERDICT\s*[:\-]\s*)?CANNOT VERIFY\b", report):
            # The header table legitimately points at the ledger and the freshness log.
            # What must not appear is a provision cited in the body as a basis for a finding.
            body = "\n".join(l for l in report.split("\n") if not l.lstrip().startswith("|"))
            if re.search(r"reference/(?:eu-|us-)[\w./-]+\.md", body):
                print("FAIL  a CANNOT VERIFY report cites a provision. The audit stopped before "
                      "any provision was applied; nothing in reference/ should be cited.")
                return 1
            print(f"CANNOT VERIFY report, declared jurisdiction {regime}: no findings and no "
                  f"provisions cited, which is correct. Nothing to check here — gate 3 checks "
                  f"the rest.")
            return 0
        print("FAIL  no findings found in the report — expected blocks headed [F-01], [P-01], ...")
        return 1

    checks = failures = crossings = 0
    for block in findings:
        tag = re.search(r"\[(?:F|P)-\d+\]", block).group()
        house = "[HOUSE POLICY" in block

        for part in REQUIRED:
            checks += 1
            body = field(block, part)
            # A label with nothing under it is a missing part, and field() never returns None for
            # one - it returns the empty string, or whitespace, or the next label. Tested against
            # None this loop asked "are the five WORDS present", passed a finding whose WHY had
            # been emptied out, and reported it as five parts present. rules.md: "Every finding
            # carries five things. A finding missing any of them is not shippable."
            if not (body or "").strip():
                failures += 1
                if body is None:
                    print(f"FAIL  {tag}  missing required part: {part}")
                else:
                    print(f"FAIL  {tag}  {part} is a heading with nothing under it. The five parts "
                          f"are what make a\n      finding answerable - what was found, where in "
                          f"the sheet, which provision, where in the\n      standard, and why it "
                          f"matters. A label carries none of that")

        where = field(block, "WHERE IN THE STANDARD") or ""
        named = re.findall(r"reference/[\w./-]+\.md", where)
        checks += 1
        if house:
            # A policy gate has no provision. What it must do instead is say so, in both
            # places a reader looks, so it can never be mistaken for a regulatory breach.
            if "no provision" not in where.lower():
                failures += 1
                print(f"FAIL  {tag}  marked [HOUSE POLICY] but WHERE IN THE STANDARD does not "
                      f"say 'no provision'")
        elif not named:
            failures += 1
            print(f"FAIL  {tag}  names no file under reference/")
        for path in named:
            checks += 1
            if path in bookkeeping:
                failures += 1
                print(f"FAIL  {tag}  cites {path} as a provision. That file is this folder's own "
                      f"bookkeeping, not the standard — a finding must cite regulatory text")
            elif path not in ref:
                failures += 1
                print(f"FAIL  {tag}  cites a file that does not exist: {path}")
            elif not path.startswith(allowed):
                failures += 1
                crossings += 1
                root = next((r for r in CORPUS_OWNER if path.startswith(r)), None)
                owner = CORPUS_OWNER.get(root, "another regime")
                why = WHY_CROSS.get((regime, root), "")
                print(f"FAIL  {tag}  cites {path} in a report declaring jurisdiction {regime}. "
                      f"That file is the {owner} corpus. Under jurisdiction {regime} a run may "
                      f"cite {' and '.join(allowed)} and nothing else.")
                if why:
                    print(f"      {why}")

        rule = field(block, "RULE") or ""
        # Every quoted string, of any length. There was a 12-character floor here, defended on the
        # ground that two short quotes on one line are read as one quote spanning the gap between
        # them - which is not true of this regex: the character class cannot cross a quote mark,
        # so `"Carc. 1B", column "L"` yields two needles, not one. What the floor did was leave
        # `"Carc. 1B"`, `"H350"`, `"Note L"` unverified, and those are the atoms of a
        # classification finding: the shortest strings in a report are the ones a reader is least
        # able to check by eye and the ones a wrong character changes most.
        quotes = re.findall(r'"([^"]+)"', rule)
        checks += 1
        if house:
            if "none" not in rule.lower()[:80]:
                failures += 1
                print(f"FAIL  {tag}  marked [HOUSE POLICY] but RULE does not open by stating "
                      f"that there is none")
            quotes = []
        elif not quotes:
            failures += 1
            print(f"FAIL  {tag}  RULE quotes nothing from the standard. A finding stands on the "
                  f"words of a provision,\n      quoted verbatim between double quote marks, so "
                  f"that a reader can put the report and the\n      standard side by side. A rule "
                  f"described in the auditor's own words cannot be checked by anyone")
        for q in quotes:
            checks += 1
            needle = norm_ws(q).rstrip(" .[")
            hay = " ".join(ref[p] for p in named if p in ref) or " ".join(ref.values())
            if needle not in hay:
                failures += 1
                print(f"FAIL  {tag}  quoted text is not in the cited standard: \"{needle[:90]}\"")

        checks += 1
        rev = re.search(r"(?:revision|version)\s*:\s*([^\n]+)", where, re.I)
        if not rev:
            failures += 1
            print(f"FAIL  {tag}  names no revision of the standard")
        else:
            checks += 1
            key = norm_ws(rev.group(1)).split(",")[0].strip()
            if key and key not in ledger:
                failures += 1
                print(f"FAIL  {tag}  revision \"{key}\" is not in STANDARDS-LEDGER.md")

        checks += 1
        conf = re.search(r"confirmed(?:\s+current)?\s*:?\s*(\d{4}-\d{2}-\d{2})", where, re.I)
        if not conf:
            failures += 1
            print(f"FAIL  {tag}  gives no date on which that revision was confirmed current")
        elif conf.group(1) not in ledger:
            failures += 1
            print(f"FAIL  {tag}  confirmation date {conf.group(1)} does not appear in the ledger")

    print(f"\n{len(findings)} finding(s), {checks} check(s), {failures} failure(s)")
    if failures:
        if crossings:
            print(f"{crossings} citation(s) reach outside the {regime} corpus. A finding under a "
                  f"regulation that does not\ngovern the sheet is not a finding, however accurately "
                  f"it quotes. Withdraw it, or change the\nregime this run was made under and audit "
                  f"the sheet again from Stage 0.")
        print("The report does not agree with the standard it cites. The standard wins.")
        return 1
    print(f"Every citation exists and lies inside the {regime} corpus "
          f"({', '.join(allowed)}), every quoted provision is present verbatim in the file named, "
          f"and every revision and confirmation date matches the ledger.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
