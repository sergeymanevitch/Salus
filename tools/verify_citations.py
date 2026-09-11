#!/usr/bin/env python3
"""Gate 2 — does every citation in a report exist, and does the quoted text match the standard?

    python3 tools/verify_citations.py <report.md> [--reference reference]
                                       [--config config/jurisdiction.md]

This is the gate that reads the AUDITOR'S OWN OUTPUT. A checker that only proves the reference
folder still says what it said proves nothing about the report: it would pass a report whose
findings had drifted away from the text they cite. So this one works the other way round. It
parses each finding out of the report, pulls the quoted provision text out of it, and looks for
that text in the file the finding names. If the report and the standard disagree, the standard
wins and the gate fails.

To see it work, change one character inside a quoted RULE string in a report and re-run.

Checks, per finding:
  1. the five required parts are present
  2. every reference/ path named exists
  3. every reference/ path named belongs to the corpus the report's own regime may cite
  4. every quoted string in RULE occurs verbatim in one of those files
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
"""
import argparse, os, re, sys

REQUIRED = ["WHAT", "WHERE", "RULE", "WHERE IN THE STANDARD", "WHY"]


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
CORPUS = {
    "EU": ("reference/eu-2020-878/", "reference/eu-clp-annex-vi/"),
    "US": ("reference/us-osha-hcs/",),
}
CORPUS_OWNER = {
    "reference/eu-2020-878/": "EU", "reference/eu-clp-annex-vi/": "EU",
    "reference/us-osha-hcs/": "US",
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
    files, bookkeeping = {}, set()
    for root, _, names in os.walk(refdir):
        for n in names:
            if not n.endswith(".md"):
                continue
            p = os.path.relpath(os.path.join(root, n)).replace(os.sep, "/")
            if n in NOT_A_STANDARD:
                bookkeeping.add(p)
                continue
            files[p] = norm_ws(open(p, encoding="utf-8", errors="replace").read())
    return files, bookkeeping


def split_findings(text):
    """A finding heading is a line-leading tag followed by its class marker, as in
    '### [F-03] [STANDARD] ...'. A bare tag at the head of a list item is a cross-reference
    and must not open a new block."""
    marks = [m.start() for m in re.finditer(
        r"(?m)^\s*#*\s*\[(?:F|P)-\d+\]\s+\[(?:STANDARD|HOUSE POLICY)", text)]
    out = []
    for i, s in enumerate(marks):
        e = marks[i + 1] if i + 1 < len(marks) else len(text)
        out.append(text[s:e])
    return out


def field(block, name):
    r"""Pull one named part out of a finding block.

    WHERE and WHERE IN THE STANDARD are different parts and one is a prefix of the other, so
    `^\s*WHERE\b` matches the heading of BOTH - \b sits happily in the space before "IN". Left
    unguarded, a finding carrying only WHERE IN THE STANDARD satisfies the requirement for WHERE
    as well, and the five required parts are enforced as four. The part that goes missing is the
    one that locates the defect in the sheet, which is the half of a finding a reader cannot
    reconstruct from the standard.
    """
    guard = r"(?! IN THE STANDARD\b)" if name == "WHERE" else ""
    m = re.search(rf"(?m)^\s*{re.escape(name)}\b{guard}[:\s]*(.*?)(?=^\s*(?:{'|'.join(re.escape(r) for r in REQUIRED)})\b|\Z)",
                  block, re.S)
    return m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report")
    ap.add_argument("--reference", default="reference")
    ap.add_argument("--config", default=os.path.join("config", "jurisdiction.md"),
                    help="read only to cross-check the report's own declaration")
    a = ap.parse_args()

    report = open(a.report, encoding="utf-8").read()

    regime, problem = report_jurisdiction(report)
    if problem:
        print(f"FAIL  {problem}.")
        print("\nThe report does not say which rulebook it was entitled to open, so this gate "
              "cannot check that\nit stayed inside it.")
        return 1
    allowed = CORPUS[regime]
    configured = config_jurisdiction(a.config)
    if configured and configured != regime:
        print(f"NOTE  this report declares {regime}; {a.config} currently reads {configured}. The "
              f"report is checked\n      against {regime}, the regime it names, because a filed "
              f"report keeps the regime it was made under\n      and a setting can be changed "
              f"afterwards. If this report is being written right now, the header\n      and the "
              f"setting disagree and one of the two is wrong.\n")

    ref, bookkeeping = load_reference(a.reference)
    ledger_path = os.path.join(a.reference, "STANDARDS-LEDGER.md")
    ledger = norm_ws(open(ledger_path, encoding="utf-8").read()) if os.path.exists(ledger_path) else ""

    findings = split_findings(report)
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
            if field(block, part) is None:
                failures += 1
                print(f"FAIL  {tag}  missing required part: {part}")

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
        quotes = [q for q in re.findall(r'"([^"]{12,})"', rule)]
        checks += 1
        if house:
            if "none" not in rule.lower()[:80]:
                failures += 1
                print(f"FAIL  {tag}  marked [HOUSE POLICY] but RULE does not open by stating "
                      f"that there is none")
            quotes = []
        elif not quotes:
            failures += 1
            print(f"FAIL  {tag}  RULE quotes nothing from the standard "
                  f"(a quoted string of 12+ characters is required)")
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
