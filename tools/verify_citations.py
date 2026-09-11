#!/usr/bin/env python3
"""Gate 2 — does every citation in a report exist, and does the quoted text match the standard?

    python3 tools/verify_citations.py <report.md> [--reference reference]

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
  3. every quoted string in RULE occurs verbatim in one of those files
  4. the revision named matches reference/STANDARDS-LEDGER.md
  5. a confirmation date is present and matches the ledger

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
    a = ap.parse_args()

    problems, stats = R.audit(a.reference)
    if problems or not stats["provenance_files"]:
        for p in problems:
            print(f"FAIL  {p}")
        if not problems:
            print(f"FAIL  nothing under {a.reference}/ records how it was generated — there is no "
                  f"PROVENANCE.md to check the standards against")
        print("\nThis gate checks a report against the standard it cites. The standard is not the "
              "one that was generated, so it cannot answer. Restore reference/ with git, or "
              "rebuild it, and run again. Details: python3 tools/verify_reference.py")
        return 1
    print(f"reference corpus verified: {stats['verified']} generated file(s) across "
          f"{stats['provenance_files']} standard(s) match tools/build_reference.py's hashes.\n")

    report = open(a.report, encoding="utf-8").read()
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
            print("CANNOT VERIFY report: no findings and no provisions cited, which is correct. "
                  "Nothing to check here — gate 3 checks the rest.")
            return 0
        print("FAIL  no findings found in the report — expected blocks headed [F-01], [P-01], ...")
        return 1

    checks = failures = 0
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
        print("The report does not agree with the standard it cites. The standard wins.")
        return 1
    print("Every citation exists, every quoted provision is present verbatim in the file named, "
          "and every revision and confirmation date matches the ledger.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
