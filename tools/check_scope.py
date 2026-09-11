#!/usr/bin/env python3
"""The scope gate - is this sheet one Salus has a rulebook for, or does the run stop here?

    python3 tools/check_scope.py <sheet.salus.md> [--config config/jurisdiction.md]

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
  exit 0  IN SCOPE      - the configured standard is declared, or nothing is declared, or the other
                          SHIPPED regime is declared (a US-format sheet under jurisdiction: EU is a
                          finding at rules.md Stage 3, not a stop - both rulebooks are here)
  exit 2  OUT OF SCOPE  - a third regime is declared and the configured standard is not. The run
                          stops, the verdict is CANNOT VERIFY, and the report says which standard
                          the sheet names and that Salus does not ship it
  exit 1  the gate could not run at all (no such file, jurisdiction not configured)

What this gate CANNOT do, stated here rather than discovered later:

  - It reads declarations, so a third-regime sheet that declares nothing reads as "nothing
    declared" and the run continues. The stop is evidence-based; silence is not evidence.
  - Its list of third regimes is finite and hand-written. A regime not in REGIMES is invisible
    to it. Adding one is a one-line change and a deliberate act, not a guess the script makes.
  - It cannot tell a declaration from a mention. A sheet that says "this SDS does not follow
    GB/T 16483" would be stopped. A human reads the quoted line the gate prints and overrules it
    by filling in config/jurisdiction.md - never by editing this file to make a sheet pass.
"""
import argparse, os, re, sys

# Markers of the two standards this folder ships. Presence of one of these means the sheet was
# written against a rulebook that is in reference/, and the audit has something to stand on.
SHIPPED = {
    "EU": [
        (r"2020/\s?878", "Commission Regulation (EU) 2020/878"),
        (r"1907/\s?2006", "Regulation (EC) No 1907/2006 (REACH)"),
        (r"1272/\s?2008", "Regulation (EC) No 1272/2008 (CLP)"),
        (r"\bREACH\b", "REACH"),
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
    if not os.path.exists(path):
        return None, f"{path} does not exist"
    text = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r"(?m)^\s*jurisdiction:\s*([A-Za-z]+)", text)
    if not m:
        return None, f"{path} names no jurisdiction"
    value = m.group(1).upper()
    if value not in SHIPPED:
        return None, f"{path} sets jurisdiction: {value}, which is not a regime Salus ships"
    return value, None


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
    ap.add_argument("--config", default=os.path.join("config", "jurisdiction.md"))
    a = ap.parse_args()

    configured, problem = read_jurisdiction(a.config)
    if problem:
        print(f"FAIL  the scope gate cannot run: {problem}")
        print("      rules.md Stage 0: jurisdiction not configured is CANNOT VERIFY, and the run stops.")
        return 1
    if not os.path.exists(a.rendering):
        print(f"FAIL  no such rendering: {a.rendering}")
        return 1

    text = open(a.rendering, encoding="utf-8", errors="replace").read()
    other = "US" if configured == "EU" else "EU"

    mine = hits(text, SHIPPED[configured])
    theirs = hits(text, SHIPPED[other])
    foreign = hits(text, REGIMES)

    print(f"configured jurisdiction: {configured}   sheet: {os.path.basename(a.rendering)}\n")
    for (name,), ln, line in mine:
        print(f"  declares the configured standard: {name}  (line {ln})")
    for (name,), ln, line in theirs:
        print(f"  declares the other shipped standard: {name}  (line {ln})")
    for (country, name), ln, line in foreign:
        print(f"  declares a third regime: {country} - {name}  (line {ln})")
        print(f"      {line}")

    if foreign and not mine:
        countries = sorted({c for (c, _), _, _ in foreign})
        print(f"\nOUT OF SCOPE - the sheet declares {', '.join(countries)} and does not declare "
              f"{configured}.")
        print("Salus ships EU 2020/878 and US 29 CFR 1910.1200 and no other rulebook. The standard "
              "this sheet\nnames is not in reference/, so there is nothing to quote and nothing to "
              "check it against.")
        print("\nSTOP. Verdict: CANNOT VERIFY - out of scope. The report states which standard the "
              "sheet declares,\nthat Salus does not ship it, and makes no judgement about the sheet "
              "in its own regime. Run no\nfurther stages: findings from the wrong rulebook are not "
              "findings.")
        return 2

    if foreign and mine:
        print("\nIN SCOPE - the sheet declares the configured standard as well as a third regime. "
              "A sheet written\nfor two markets is audited against the configured one. The third "
              "declaration is not a finding.")
        return 0
    if theirs and not mine:
        print(f"\nIN SCOPE - the sheet is compiled to {other}, the other standard this folder "
              f"ships. rules.md Stage 3\nreports that as a finding and the audit continues: both "
              f"rulebooks are here, so the comparison is real.")
        return 0
    if not mine:
        print("\nIN SCOPE - the sheet declares no compilation standard at all. rules.md Stage 3 "
              "infers the applicable\nrevision from the issue date and says in the report that it "
              "was inferred.")
        return 0
    print(f"\nIN SCOPE - the sheet declares {configured}, the configured standard.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
