#!/usr/bin/env python3
"""Stage 2, the arithmetic half: find the dates a sheet states, and say what they make it.

    python3 tools/check_age.py <sheet.salus.md> [--config <jurisdiction.md>]

This REPORTS. It does not gate, and it does not decide (AD-15). It exits 0 whether a finding is
owed or not, and non-zero only when it could not read the rendering at all — the same contract as
extract.py, and for the same reason: what the age of a sheet *means* is a reading, and the reading
belongs to the auditor.

WHAT IT DOES

Finds every date the rendering states near a word that claims it is an issue or revision date,
parses it, and measures it against `run_date` and `policy_max_age_years` from
config/jurisdiction.md. Every candidate is printed with its line number and the line it came from,
so the auditor checks the script rather than trusting it.

WHY IT DOES NOT DECIDE

Two reasons, and both are visible in this folder's own corpus.

  1.  `03/04/2026` is two dates. The rendering does not say which convention the supplier used, so
      this prints BOTH readings and names the one the configured regime makes likelier — US
      sheets are written m/d/y, EU sheets d/m/y — without acting on it. Where the two readings
      fall on opposite sides of the threshold, it says so in those words and stops there.
  2.  A sheet can state a date that is not the one the gate is about. The shipped Carboguard sheet
      carries a print date of 03/26/2020 and a revision date of 03/25/2019, a year apart; the age
      gate runs on the revision, and no amount of pattern matching knows that. It knows which
      words sat next to the date, which is evidence, not a decision.

So: the arithmetic is mechanical now, and the judgement is not. Before this script the whole of
Stage 2 was a reading, including the subtraction — and a subtraction nobody checked is exactly the
kind of thing that is right until the day it is not.
"""
import argparse
import datetime
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import read_config as C  # noqa: E402  — one reader for config/jurisdiction.md, not two (AD-15)

# The words a supplier puts next to the date that governs this gate, and the words that mean a
# date is something else. Both lists are evidence, not a verdict: they decide what is PRINTED.
GOVERNS = re.compile(r"(?i)\b(date of issue|date of revision|revision date|revised|issue date|"
                     r"date of preparation|prepared on|version date|date of the last revision)\b")
NOT_THE_GATE = re.compile(r"(?i)\b(date of previous issue|previous revision|print date|printed|"
                          r"date printed|expiry|expiration|valid until)\b")

NUMERIC = re.compile(r"\b(\d{1,4})[./-](\d{1,2})[./-](\d{2,4})\b")
ISO = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")

# A month written in words is not ambiguous, and suppliers write them: the Chinese-standard sheet
# in this corpus dates itself "Issue date  June-30-2025". The first version of this script read
# only digits, so it answered NO DATE FOUND on a sheet that states its date plainly — and
# rules.md Stage 2 turns that answer into CANNOT VERIFY. A parser's blind spot became a verdict.
MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
MONTH_FIRST = re.compile(r"(?i)\b([a-z]{3,9})[ ,.\-/]+(\d{1,2})(?:st|nd|rd|th)?[ ,.\-/]+(\d{4})\b")
DAY_FIRST = re.compile(r"(?i)\b(\d{1,2})(?:st|nd|rd|th)?[ ,.\-/]+([a-z]{3,9})[ ,.\-/]+(\d{4})\b")


def textual(match, month_first):
    """A date whose month is a word. One reading, and no convention to argue about."""
    word = (match.group(1) if month_first else match.group(2)).lower()[:3]
    if word not in MONTHS:
        return {}
    day = int(match.group(2) if month_first else match.group(1))
    try:
        when = datetime.date(int(match.group(3)), MONTHS[word], day)
    except ValueError:
        return {}
    return {"d/m/y": when, "m/d/y": when}


def readings_for(match, regime):
    """Every reading of one matched date that is a real date, keyed by convention."""
    if len(match.group(1)) == 4:                      # ISO: unambiguous by shape
        try:
            when = datetime.date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        except ValueError:
            return {}
        return {"d/m/y": when, "m/d/y": when}
    a, b, c = (int(x) for x in match.groups())
    if c < 100:
        c += 2000 if c < 70 else 1900
    out = {}
    for day, month, name in ((b, a, "m/d/y"), (a, b, "d/m/y")):
        try:
            out[name] = datetime.date(c, month, day)
        except ValueError:
            pass
    # 16/04/2019 has no m/d/y reading, and a sheet that writes one date that way wrote them all
    # that way. A single reading stands for both conventions rather than dropping out of one.
    if len(out) == 1:
        only = next(iter(out.values()))
        out = {"d/m/y": only, "m/d/y": only}
    return out


def candidates(text, regime):
    """Each date in the rendering, with the words that stood closest before it.

    Per DATE, not per line. A single line of a shipped sheet reads "Date of issue/Date of revision
    : 29/01/2026   Date of previous issue : 04/11/2025", and a line-level rule classifies both
    dates the same way — which is how an earlier version of this script threw away the one date
    that governs and kept the one that does not."""
    out = []
    for n, line in enumerate(text.split("\n"), 1):
        body = re.sub(r"^\s*\d+│", "", line)          # the rendering's own line-number gutter
        labels = ([(m.start(), m.group(), True) for m in GOVERNS.finditer(body)]
                  + [(m.start(), m.group(), False) for m in NOT_THE_GATE.finditer(body)])
        if not labels:
            continue
        labels.sort()
        matches = ([(m, None) for m in ISO.finditer(body)]
                   + [(m, None) for m in NUMERIC.finditer(body) if not ISO.fullmatch(m.group())]
                   + [(m, True) for m in MONTH_FIRST.finditer(body)]
                   + [(m, False) for m in DAY_FIRST.finditer(body)])
        placed = set()
        for m, month_first in matches:
            before = [l for l in labels if l[0] < m.start()]
            if not before:
                # "3/5/2025 (Revision date)" — a real line of a shipped sheet, where the claim
                # stands after the date instead of before it. The nearest label on the line is
                # what names this date either way; only a date with no claim at all is dropped.
                after = [l for l in labels if l[0] >= m.end()]
                if not after:
                    continue
                before = [after[0]]
            _, word, governs = before[-1]
            # "Date of previous issue" contains "date of issue" as a substring, so the longer
            # claim has to win when both matched at once. The rightmost start does that already
            # except when they start together, which is what this line settles.
            same = [l for l in before if l[0] == before[-1][0]]
            if len(same) > 1:
                word, governs = max(same, key=lambda l: len(l[1]))[1:]
            r = textual(m, month_first) if month_first is not None else readings_for(m, regime)
            if r:
                span = (before[-1][0], tuple(sorted(r.values())))
                if span in placed:
                    continue                          # the same date matched by two patterns
                placed.add(span)
                out.append({"line": n, "text": body.strip(), "word": word,
                            "governs": governs, "readings": r})
    return out


def unparsed_claims(text, found):
    """Lines that claim a date and gave this script none. The point of printing them is that a
    parser's blind spot must not leave the page as "no date found": rules.md Stage 2 turns that
    answer into CANNOT VERIFY, which is a verdict, and a verdict is too much weight for a regex
    to carry silently."""
    seen = {c["line"] for c in found}
    out = []
    for n, line in enumerate(text.split("\n"), 1):
        body = re.sub(r"^\s*\d+│", "", line)
        if n not in seen and GOVERNS.search(body) and re.search(r"\d", body):
            out.append((n, body.strip()))
    return out


def age_in_years(when, on):
    years = on.year - when.year - ((on.month, on.day) < (when.month, when.day))
    months = (on.month - when.month - (on.day < when.day)) % 12
    return years, months


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rendering", help="the .salus.md produced by extract.py")
    ap.add_argument("--config", default=None,
                    help="the settings file to read; defaults to config/jurisdiction.md beside "
                         "this script, not beside your working directory")
    a = ap.parse_args()
    if not os.path.exists(a.rendering):
        print(f"FAIL  no such rendering: {a.rendering}")
        return 1

    settings, problems = C.load(os.path.abspath(a.config) if a.config else None)
    for p in problems:
        print(f"NOTE  {p}")
    regime = settings["jurisdiction"] or "EU"
    limit = settings["policy_max_age_years"]
    today = settings["resolved_run_date"] or datetime.date.today()
    if limit is None:
        print("FAIL  policy_max_age_years could not be read, so there is no threshold to measure "
              "against. python3 tools/read_config.py says what is wrong with the settings")
        return 1

    text = open(a.rendering, encoding="utf-8", errors="replace").read()
    found = candidates(text, regime)
    likelier = "m/d/y" if regime == "US" else "d/m/y"
    print(f"run date: {today.isoformat()}   policy_max_age_years: {limit}   regime: {regime} "
          f"(so {likelier} is the likelier convention)\n")

    stuck = unparsed_claims(text, found)

    if not found:
        print("NO DATE FOUND beside any word claiming an issue or revision date.")
        for n, line in stuck:
            print(f"    but line {n} claims one: {line[:90]}")
        print("rules.md Stage 2: no date found anywhere is CANNOT VERIFY. Do not guess from a "
              "file timestamp — and read the sheet before accepting that, because a date this "
              "script cannot see may be one a person can.")
        return 0

    for n, line in stuck:
        print(f"CLAIMS A DATE, PARSED NONE — line {n}: {line[:92]}")
    if stuck:
        print("    Read those lines before believing the conclusion below: a date this script "
              "cannot read is a date it did not measure.\n")

    governing = [c for c in found if c["governs"]]
    for c in found:
        mark = "" if c["governs"] else f"   (not the gate: \"{c['word']}\")"
        print(f"line {c['line']}: {c['text'][:96]}{mark}")
        for conv in sorted(set(c["readings"].values())):
            names = sorted(k for k, v in c["readings"].items() if v == conv)
            y, mo = age_in_years(conv, today)
            print(f"    {conv.isoformat()}  ({' and '.join(names) if len(names) < 2 else 'either convention'})"
                  f"  {y} years {mo} months old")
        print()

    if not governing:
        print("Every date found sits behind words that name another kind of date — a previous "
              "issue, a print date. That is not evidence of the revision date, and rules.md "
              "Stage 2 is not satisfied by it. Read the sheet.")
        return 0

    if limit == 0:
        print("No conclusion: the age gate is off in this installation "
              "(policy_max_age_years: 0). The dates above are printed as evidence only.")
        return 0

    # "The date of issue or last revision" — the LAST one. A sheet that states an issue date of
    # 2020 and a revision date of 2025 is five years old as a document and one year old as a
    # sheet, and the gate is about the sheet. Each convention is applied to the whole rendering
    # rather than date by date: a supplier writes dates one way, not both ways.
    verdicts = {}
    for conv in ("d/m/y", "m/d/y"):
        dates = [c["readings"][conv] for c in governing if conv in c["readings"]]
        if not dates:
            continue
        newest = max(dates)
        y, mo = age_in_years(newest, today)
        verdicts[conv] = (newest, y, mo, y >= limit)

    for conv, (newest, y, mo, over) in verdicts.items():
        print(f"newest governing date, reading every date as {conv}: {newest.isoformat()} — "
              f"{y} years {mo} months old on the run date"
              f"{'  → AT OR PAST the house limit' if over else '  → inside the house limit'}")
    print()

    outcomes = {v[3] for v in verdicts.values()}
    if len(outcomes) > 1:
        print(f"THE TWO CONVENTIONS DISAGREE. Read as {likelier} — the likelier one for a "
              f"{regime} run — this sheet is "
              f"{'over' if verdicts[likelier][3] else 'inside'} the limit; read the other way it "
              "is not. A person decides which convention the supplier used, from the sheet's own "
              "language and origin. This script will not choose for you.")
    elif True in outcomes:
        print(f"A HOUSE-POLICY FINDING IS OWED: the sheet is at or past {limit} years on every "
              "reading. rules.md Stage 2 — the finding is marked [HOUSE POLICY — no provision], "
              "names policy_max_age_years, and is not a breach of either standard, because "
              "neither sets an expiry.")
    else:
        print(f"NO FINDING IS OWED: on every reading the sheet is inside the {limit}-year house "
              "limit. Record the age and continue (rules.md Stage 2) — a report that performed "
              "the check and says nothing about it reads as one that skipped it.")

    print("\nWhat this cannot tell you: whether the words beside a date meant what they say, and "
          "whether a date it never found is printed somewhere it could not parse. The evidence is "
          "above with line numbers; the reading is yours.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
