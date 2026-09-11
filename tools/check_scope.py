#!/usr/bin/env python3
"""The scope gate - is this sheet one Salus has a rulebook for, or does the run stop here?

    python3 tools/check_scope.py <sheet.salus.md> [--config <jurisdiction.md>]

Run it from anywhere. Which regime is configured does not depend on your working directory: the
settings file is this folder's, and it is found from this script's own location - see REPO_ROOT.

Salus ships two standards: EU 2020/878 and US 29 CFR 1910.1200. A safety data sheet compiled to a
third country's standard - China's GB/T 16483, Japan's JIS Z 7253, Russia's GOST 30333, Canada's
Hazardous Products Regulations - was written to obligations this folder does not carry and cannot
quote. Auditing it against the configured standard produces findings that are all the same finding
said many times over: the wrong ruler was used. That is not an audit, and on 2026-09-11 one was
filed here before this gate existed. See README, "An incident, and the gate it produced".

The gate runs AFTER Gate 1 and BEFORE the audit. It is the only check that can end a run before it
starts, so it is deliberately narrow about what it treats as a stop.

What it looks for is a COMPILATION standard - a rule about how a safety data sheet must be written -
declared in the sheet itself. It does not look at country names, addresses, languages, emergency
numbers or chemical inventory lists: a sheet that tells a German reader its components are listed
on China's IECSC is an EU sheet with an inventory paragraph, not a Chinese sheet.

Outcomes:
  exit 0  IN SCOPE      - the sheet declares a standard this folder SHIPS: the configured one, or
                          the other one (a US-format sheet under jurisdiction: EU is a finding at
                          rules.md Stage 3, not a stop - both rulebooks are here). A third regime
                          named alongside it does not change that; a sheet sold into two markets
                          says so. Also exit 0 when the sheet declares no compilation standard at
                          all: silence is not evidence of a foreign one
  exit 2  OUT OF SCOPE  - a third regime is declared and NEITHER shipped standard is. The run
                          stops, the verdict is CANNOT VERIFY, and the report says which standard
                          the sheet names and that Salus does not ship it
  exit 1  the gate could not run at all (no such file, jurisdiction not configured)

Read that table in one direction: only the absence of BOTH shipped standards can stop a run. The
stop belongs to a sheet written to a rulebook that is not here, and a sheet naming 1910.1200 or
2020/878 has named one that is, whatever else it also names.

What this gate CANNOT do, stated here rather than discovered later:

  - It reads declarations, so a third-regime sheet that declares nothing reads as "nothing
    declared" and the run continues. The stop is evidence-based; silence is not evidence.
  - Its list of third regimes is finite and hand-written. A regime not in REGIMES is invisible
    to it. Adding one is a one-line change and a deliberate act, not a guess the script makes.
  - It cannot tell a declaration from a mention. A sheet that says "this SDS does not follow
    GB/T 16483" would be stopped. A human reads the quoted line the gate prints and overrules it
    by filling in config/jurisdiction.md - never by editing this file to make a sheet pass.
    Every hit is printed with the line it matched on, the ones that SUPPRESS a stop as much as
    the ones that cause it: the person overruling this gate has to see what it read.
"""
import argparse, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import read_config as C  # noqa: E402  — one reader for config/jurisdiction.md, not two (AD-15)

# This folder, found from this script rather than from whoever ran it. config/jurisdiction.md is
# THIS installation's setting - the file rules.md Stage 0 names - and it does not move when the
# caller's working directory does. Resolved relative to the caller, as it was until 2026-09-11,
# the gate answered "jurisdiction not configured" from every directory but the root: an inability
# to run, worded as a real stop condition, about a sheet it had not opened. Same idiom and same
# reason as REPO_ROOT in tools/verify_citations.py. realpath, not abspath, to survive a symlink.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# Markers of the two standards this folder ships. Presence of one of these means the sheet was
# written against a rulebook that is in reference/, and the audit has something to stand on.
SHIPPED = {
    "EU": [
        (r"2020/\s?878", "Commission Regulation (EU) 2020/878"),
        (r"1907/\s?2006", "Regulation (EC) No 1907/2006 (REACH)"),
        (r"1272/\s?2008", "Regulation (EC) No 1272/2008 (CLP)"),
        # REACH is a regulation and also an ordinary English word, and the bare pattern \bREACH\b
        # read the GHS precautionary statement P102, "Keep out of reach of children", as a
        # declaration that the sheet was compiled to Annex II. P102 sits on four of the 24 sheets
        # shipped with this folder and on a large share of sheets worldwide - on a sheet compiled
        # to GB/T 16483, one line of that boilerplate was enough to suppress the stop this gate
        # exists to make. That is the 2026-09-11 incident, reopened from the other end.
        #
        # So the word only counts as a declaration when it is written as one: a conformance verb
        # reaching it inside a single sentence - "Prepared according to the UK REACH by Chevron" -
        # or Annex II named beside it, Annex II being the annex that says how a safety data sheet
        # is written. Annexes XIV and XVII are deliberately not here: those restrict a SUBSTANCE,
        # and a Section 15 line citing them says nothing about which rulebook the DOCUMENT
        # followed. Deleting the pattern outright was the other candidate, and is rejected in this
        # gate's own terms: a dual-market sheet declaring GB/T 16483 and REACH in words rather
        # than by number would then read as declaring only GB/T, and the run would be stopped for
        # a sheet this folder holds the rulebook for. A false stop is the one error a gate that
        # ends runs cannot afford.
        (r"(?:conform\w*|complian\w*|complies|compiled|prepared|drawn up|issued|written|"
         r"in accordance with|according to|pursuant to)[^.\n]{0,60}?(?<!out of )\bREACH\b"
         r"|\bREACH\b[\s,()-]{0,12}(?:Regulation\s*)?Annex\s*II\b"
         r"|Annex\s*II[\s,()-]{0,12}(?:of|to|under)\s*(?:the\s*)?\bREACH\b",
         "REACH"),
    ],
    "US": [
        (r"1910\.1200", "29 CFR 1910.1200"),
        (r"\bHazCom\b", "OSHA Hazard Communication"),
        (r"Hazard Communication Standard", "OSHA Hazard Communication Standard"),
    ],
}

# Third-regime SDS COMPILATION standards. Every entry names how a safety data sheet must be
# written in that jurisdiction. Inventory lists (IECSC, DSL, AICS, ENCS, KECI) are deliberately
# absent: being listed on an inventory says where a substance may be sold, not which rulebook
# the document was written to.
REGIMES = [
    (r"GB/?T\s?16483", "China", "GB/T 16483 - Safety data sheet for chemical products"),
    (r"GB/?T\s?17519", "China", "GB/T 17519 - Guidance on the compilation of SDS"),
    (r"JIS\s?Z\s?7253", "Japan", "JIS Z 7253"),
    (r"GOST\s?30333", "Russia / EAEU", "GOST 30333"),
    (r"GOST\s?31340", "Russia / EAEU", "GOST 31340"),
    (r"ABNT\s?NBR\s?14725", "Brazil", "ABNT NBR 14725"),
    (r"NOM-018-STPS", "Mexico", "NOM-018-STPS"),
    (r"CNS\s?15030", "Taiwan", "CNS 15030"),
    (r"KS\s?M\s?ISO\s?11014", "South Korea", "KS M ISO 11014"),
    (r"SOR/\s?2015-17", "Canada", "Hazardous Products Regulations (SOR/2015-17)"),
    (r"\bWHMIS\b", "Canada", "WHMIS"),
]


def read_jurisdiction(path):
    """Which regime this installation audits under, and every other complaint the settings file
    earns. The parsing lives in read_config.py: this gate used to carry its own copy, and a
    second copy of "what the settings say" is the drift AD-15 exists to stop.

    Only the jurisdiction stops this gate — rules.md Stage 0 names that one and no other. A
    policy_max_age_years that is not a number is a real defect and is a matter for Stage 2 and
    for the report gate, so it is returned to be printed as a NOTE rather than swallowed."""
    settings, problems = C.load(path)
    if settings["jurisdiction"] is None:
        return None, (problems[0] if problems else f"{path} names no jurisdiction"), []
    rest = [p for p in problems if "jurisdiction" not in p]
    return settings["jurisdiction"], None, rest


def hits(text, patterns):
    """Every pattern that matches, with the line it matched on - the gate shows its evidence."""
    out = []
    for entry in patterns:
        pat, rest = entry[0], entry[1:]
        m = re.search(pat, text, re.I)
        if not m:
            continue
        line_no = text.count("\n", 0, m.start()) + 1
        line = text.split("\n")[line_no - 1].strip()
        out.append((rest, line_no, line[:140]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rendering", help="the .salus.md produced by extract.py")
    ap.add_argument("--config", default=None,
                    help="the settings file to read; defaults to config/jurisdiction.md beside "
                         "this script. An explicit path is resolved against YOUR working "
                         "directory.")
    a = ap.parse_args()

    # An explicit --config is a path the caller typed, so it is resolved the caller's way. The
    # default is not: it is this installation's own setting, kept where this folder keeps it. The
    # rendering stays the caller's argument and is opened exactly as given.
    configpath = os.path.abspath(a.config) if a.config else os.path.join(
        REPO_ROOT, "config", "jurisdiction.md")
    configured, problem, other_settings = read_jurisdiction(configpath)
    if problem:
        print(f"FAIL  the scope gate cannot run: {problem}")
        print("      rules.md Stage 0: jurisdiction not configured is CANNOT VERIFY, and the run stops.")
        return 1
    for note in other_settings:
        print(f"NOTE  {note}")
        print("      The scope gate runs anyway — it decides about the standard, not the age "
              "gate — but\n      python3 tools/read_config.py says what else this file cannot "
              "honour as written.")
    if not os.path.exists(a.rendering):
        print(f"FAIL  no such rendering: {a.rendering}")
        return 1

    text = open(a.rendering, encoding="utf-8", errors="replace").read()
    other = "US" if configured == "EU" else "EU"

    mine = hits(text, SHIPPED[configured])
    theirs = hits(text, SHIPPED[other])
    foreign = hits(text, REGIMES)

    print(f"configured jurisdiction: {configured}   sheet: {os.path.basename(a.rendering)}\n")
    # Every hit prints the line it was read off, not only the ones that stop a run. A hit on a
    # shipped standard SUPPRESSES the stop, and printing it bare left the person asked to overrule
    # this gate holding a verdict and no evidence for the half of it that decided the answer.
    for (name,), ln, line in mine:
        print(f"  declares the configured standard: {name}  (line {ln})")
        print(f"      {line}")
    for (name,), ln, line in theirs:
        print(f"  declares the other shipped standard: {name}  (line {ln})")
        print(f"      {line}")
    for (country, name), ln, line in foreign:
        print(f"  declares a third regime: {country} - {name}  (line {ln})")
        print(f"      {line}")

    # The order below is the decision, and it is written shipped-first on purpose. A declaration
    # of EITHER standard this folder holds settles the question - rules.md Stage 1b stops only a
    # sheet that "declares neither 2020/878 nor 1910.1200" - so both shipped branches are tested
    # before the stop is considered at all. Tested the other way round, as they were until
    # 2026-09-11, the `theirs` branch became unreachable the moment any third regime was
    # mentioned: a US sheet carrying one line about WHMIS was stopped as out of scope by a run
    # that had just printed that the sheet declares 29 CFR 1910.1200. US/Canada bilingual sheets
    # say that routinely, and the EU<->US crossing is a finding at Stage 3, never a stop.
    if mine and foreign:
        print("\nIN SCOPE - the sheet declares the configured standard as well as a third regime. "
              "A sheet written\nfor two markets is audited against the configured one. The third "
              "declaration is not a finding.")
        return 0
    if mine:
        print(f"\nIN SCOPE - the sheet declares {configured}, the configured standard.")
        return 0
    if theirs:
        print(f"\nIN SCOPE - the sheet is compiled to {other}, the other standard this folder "
              f"ships. rules.md Stage 3\nreports that as a finding and the audit continues: both "
              f"rulebooks are here, so the comparison is real.")
        if foreign:
            countries = sorted({c for (c, _), _, _ in foreign})
            print(f"The {', '.join(countries)} declaration above is not a stop either. The stop "
                  f"belongs to a sheet written to a\nrulebook this folder does not hold, and this "
                  f"sheet names one it does.")
        return 0
    if foreign:
        countries = sorted({c for (c, _), _, _ in foreign})
        print(f"\nOUT OF SCOPE - the sheet declares {', '.join(countries)} and neither of the "
              f"two standards Salus ships.")
        print("Salus ships EU 2020/878 and US 29 CFR 1910.1200 and no other rulebook. The standard "
              "this sheet\nnames is not in reference/, so there is nothing to quote and nothing to "
              "check it against.")
        print("\nSTOP. Verdict: CANNOT VERIFY - out of scope. The report states which standard the "
              "sheet declares,\nthat Salus does not ship it, and makes no judgement about the sheet "
              "in its own regime. Run no\nfurther stages: findings from the wrong rulebook are not "
              "findings.")
        return 2

    print("\nIN SCOPE - the sheet declares no compilation standard at all. rules.md Stage 3 "
          "infers the applicable\nrevision from the issue date and says in the report that it "
          "was inferred.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
