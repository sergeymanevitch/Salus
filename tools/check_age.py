#!/usr/bin/env python3
"""Stage 2, the arithmetic half: find the dates a sheet states, and say what they make it.

    python3 tools/check_age.py <sheet.salus.md> [--pdf <sheet.pdf>] [--config <jurisdiction.md>]

This REPORTS. It does not gate, and it does not decide (AD-15). It exits 0 whether a finding is
owed or not, and non-zero only when it could not read the rendering at all — the same contract as
extract.py, and for the same reason: what the age of a sheet *means* is a reading, and the reading
belongs to the auditor.

WHAT IT DOES

Finds every date the rendering states near a word that claims it is an issue, revision, or
superseded-version date, parses it, and measures the newest governing one against `run_date` and
`policy_max_age_years` from config/jurisdiction.md. Every candidate is printed with its line
number and the line it came from, so the auditor checks the script rather than trusting it.

`03/04/2026` is two dates, and a rendering does not say which convention the supplier used. So the
script works on CONVENTIONS — d/m/y and m/d/y, sheet-wide, because a supplier writes dates one way
and not both — and applies four signals in order, each of which can only REMOVE a convention and
can never supply a date:

  1.  SHAPE. A day above 12, a month written as a word, an ISO date. `30.08.2024` has one reading.
  2.  THE SHEET'S OWN CONVENTION. One date that shape reads only one way fixes the convention for
      every ambiguous date on the same sheet.
  3.  THE ORDER THE SHEET ITSELF STATES. A superseded or replaced version is older than the
      revision that superseded it, and an issue date falls on or before its revision. A reading
      that inverts a stated order is not a reading, it is an error.
  4.  THE FILE'S OWN TIMESTAMP, AS AN UPPER BOUND — only with `--pdf`. A sheet cannot state a date
      later than the last time its own file was written.

Each elimination is printed with the signal that made it and the line it rests on, because a
resolved ambiguity that reads as certainty is worse than an unresolved one. Where two conventions
still survive, both are printed and the script says the document does not settle it. That residue
is the answer, not a failure.

FOUR THINGS THIS DELIBERATELY WILL NOT DO

  1.  It never reads the PDF's metadata AS the sheet's date. The corpus proves metadata dates the
      FILE and not the document: LOCTITE 270's /ModDate is 2025-01-01, which is the printing date
      printed on its own first page, while the sheet's revision is 2024-08-30. Used as a bound it
      eliminates and never supplies; used as a value it would have been wrong by four months on
      the first sheet tried. Absent, stripped or unreadable metadata means NO constraint — never a
      guessed date. Three of the 22 corpus sheets already have none this script can read.
  2.  It never lets the bound, or any other signal, remove the last surviving convention. The
      corpus has a sheet whose own file is older than the dates it prints — CRC ECO Leak Finder
      states an issue date of 14/10/2024 in a file whose /ModDate is 2024-08-19 — and one whose
      stated issue date falls after its stated revision date, which is the same sheet. When a
      signal contradicts everything left, the contradiction is printed and nothing is eliminated.
      A tool that resolves an incoherent document has stopped reading it.
  3.  The regime prior ORDERS what is printed and never decides it. EU sheets tend to d/m/y and US
      sheets to m/d/y, and the corpus carries its own counter-example: JET-LUBE's sheet is written
      for the GB market and dates itself m/d/y, because its supplier is American. A rule would have
      been confidently wrong.
  4.  It does not know that the words beside a date meant what they say. The shipped Carboguard
      sheet carries a print date one year after its revision date; the gate runs on the revision,
      and no amount of pattern matching knows that. It knows which words sat next to the date,
      which is evidence, not a decision.

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

# The words a supplier puts next to the date that governs this gate, the words that name the
# version this one replaced, and the words that mean something else entirely. All three lists are
# evidence, not a verdict: they decide what is PRINTED and which comparison it takes part in.
#
# `Revision:` with nothing after the word is in GOVERNS because it is the form the regulation
# PRESCRIBES. reference/eu-2020-878/regulation-2020-878.md, provision 0.2.5, line 145, quoted:
#
#   "The date of compilation of the safety data sheet shall be given on the first page. When a
#    safety data sheet has been revised and the new, revised version is provided to recipients,
#    the changes shall be brought to the attention of the recipients in Section 16 of the safety
#    data sheet, unless the changes have been indicated elsewhere. For the revised safety data
#    sheets, the date of compilation, identified as “Revision: (date)”, shall appear on the first
#    page, as well as one or more indications of which version is replaced, such as version
#    number, revision number, or supersedes date."
#
# Until 2026-09-11 this script had `date of revision` and `revision date` and not a bare
# `Revision:`, so LOCTITE 270 — whose first page reads `Revision: 30.08.2024`, exactly as 0.2.5
# asks — came back NO DATE FOUND, and rules.md Stage 2 turns that into CANNOT VERIFY. The sheet
# was right and the reader was wrong, which is the worst direction for this kind of error to run.
# The colon is required, so `Revision No: 1,03` stays a version number and not a date claim.
GOVERNS = re.compile(r"(?i)(?:\b(?:date of issue|date of revision|revision date|revised|"
                     r"issue date|date of preparation|prepared on|version date|"
                     r"date of the last revision|date of compilation)\b|\brevision\s*:)")
# The same provision names a "supersedes date" as one of the three ways a sheet may indicate which
# version it replaces, so these dates are not noise: they are a required field, and what the field
# MEANS is that the date under it is older than the revision above it. That is signal 3.
PRIOR = re.compile(r"(?i)\b(?:date of previous issue|previous issue|previous revision|"
                   r"previous version|supersedes|superseded|supersedes date|replaces|replaced)"
                   r"(?:\s+(?:version|date|edition|issue))?(?:\s+(?:of|from|by))?")
# Dates that are neither the gate nor part of the sheet's own version history.
OTHER = re.compile(r"(?i)\b(?:print date|printing date|date printed|printed|date of printing|"
                   r"expiry|expiration|expiry date|valid until|use before|best before)\b")
# …and of those, the ones that are meant to lie in the future, so the file's own timestamp is not
# an upper bound on them. A shelf life is not a claim about when the document was written.
FUTURE_OK = re.compile(r"(?i)\b(?:expiry|expiration|valid until|use before|best before)\b")

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

CONVENTIONS = ("d/m/y", "m/d/y")


def textual(match, month_first):
    """A date whose month is a word. One reading, and no convention to argue about."""
    word = (match.group(1) if month_first else match.group(2)).lower()[:3]
    if word not in MONTHS:
        return {}, None
    day = int(match.group(2) if month_first else match.group(1))
    try:
        when = datetime.date(int(match.group(3)), MONTHS[word], day)
    except ValueError:
        return {}, None
    # Unambiguous, but it says NOTHING about how this sheet writes its numeric dates. "January 29,
    # 2025" is not evidence that 03/04 is March. Same for ISO. Only a numeric date can fix the
    # numeric convention, so `shape` — the convention this date proves — stays None.
    return {"d/m/y": when, "m/d/y": when}, None


def readings_for(match):
    """Every reading of one matched date that is a real date, and the convention it proves.

    Returns (readings, shape). `shape` is the convention name when the digits parse under exactly
    one of them — 16/04/2019 is not a date in m/d/y, so it is d/m/y and so is the rest of the
    sheet — and None when they parse both ways or under neither."""
    if len(match.group(1)) == 4:                      # ISO: unambiguous by shape, silent on order
        try:
            when = datetime.date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        except ValueError:
            return {}, None
        return {"d/m/y": when, "m/d/y": when}, None
    a, b, c = (int(x) for x in match.groups())
    if c < 100:
        c += 2000 if c < 70 else 1900
    out = {}
    for day, month, name in ((b, a, "m/d/y"), (a, b, "d/m/y")):
        try:
            out[name] = datetime.date(c, month, day)
        except ValueError:
            pass
    if len(out) == 1:
        proves = next(iter(out))
        only = out[proves]
        # A single reading stands for both conventions rather than dropping out of one, so the
        # date is still measured if the sheet's convention turns out to be the other one. What it
        # PROVES is recorded separately, and that is what signal 2 acts on.
        return {"d/m/y": only, "m/d/y": only}, proves
    return out, None


def candidates(text):
    """Each date in the rendering, with the words that stood closest before it.

    Per DATE, not per line. A single line of a shipped sheet reads "Date of issue/Date of revision
    : 29/01/2026   Date of previous issue : 04/11/2025", and a line-level rule classifies both
    dates the same way — which is how an earlier version of this script threw away the one date
    that governs and kept the one that does not."""
    out = []
    for n, line in enumerate(text.split("\n"), 1):
        body = re.sub(r"^\s*\d+│", "", line)          # the rendering's own line-number gutter
        labels = ([(m.start(), m.group(), "governs") for m in GOVERNS.finditer(body)]
                  + [(m.start(), m.group(), "prior") for m in PRIOR.finditer(body)]
                  + [(m.start(), m.group(), "other") for m in OTHER.finditer(body)])
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
            _, word, role = before[-1]
            # "Date of previous issue" contains "date of issue" as a substring, so the longer
            # claim has to win when both matched at once. The rightmost start does that already
            # except when they start together, which is what this line settles.
            same = [l for l in before if l[0] == before[-1][0]]
            if len(same) > 1:
                word, role = max(same, key=lambda l: len(l[1]))[1:]
            r, shape = (textual(m, month_first) if month_first is not None
                        else readings_for(m))
            if r:
                span = (before[-1][0], tuple(sorted(set(r.values()))))
                if span in placed:
                    continue                          # the same date matched by two patterns
                placed.add(span)
                out.append({"line": n, "text": body.strip(), "word": word, "role": role,
                            "governs": role == "governs", "readings": r, "shape": shape,
                            "future_ok": bool(FUTURE_OK.search(word)),
                            "revision": role == "governs" and "revis" in word.lower(),
                            "issue": role == "governs" and "revis" not in word.lower()})
    return out


def unparsed_claims(text, found):
    """Lines that claim a date and gave this script none. The point of printing them is that a
    parser's blind spot must not leave the page as "no date found": rules.md Stage 2 turns that
    answer into CANNOT VERIFY, which is a verdict, and a verdict is too much weight for a regex
    to carry silently. This list should stay printed forever — the next corpus will state a date
    in a form this one does not."""
    seen = {c["line"] for c in found}
    out = []
    for n, line in enumerate(text.split("\n"), 1):
        body = re.sub(r"^\s*\d+│", "", line)
        if n not in seen and GOVERNS.search(body) and re.search(r"\d", body):
            out.append((n, body.strip()))
    return out


def file_bound(pdf_path):
    """The last time the FILE was written, from its own metadata. Returns (date, how).

    A date here is an upper bound on what the document can claim, and nothing else — see the
    docstring. `date` is None whenever there is any doubt at all: no path given, no such file, a
    PDF this machine cannot open, no /ModDate and no /CreationDate, an unparseable value. No
    constraint is always a safe answer; a guessed one never is."""
    if not pdf_path:
        return None, ("no --pdf given, so the file's own timestamp was not read and signal 4 did "
                      "not run. Pass the PDF extract.py converted to apply it")
    if not os.path.exists(pdf_path):
        return None, f"no such PDF: {pdf_path} — no bound, and no guess in place of one"
    try:
        import pypdf
        meta = pypdf.PdfReader(pdf_path).metadata or {}
    except Exception as e:                            # encrypted, truncated, not a PDF at all
        return None, (f"the PDF's metadata could not be read ({type(e).__name__}: {e}) — no "
                      "bound, and no guess in place of one")
    stamps = {}
    for key in ("/ModDate", "/CreationDate"):
        raw = meta.get(key)
        m = re.match(r"D?:?(\d{4})(\d{2})(\d{2})", str(raw or ""))
        if m:
            try:
                stamps[key] = datetime.date(*(int(x) for x in m.groups()))
            except ValueError:
                pass
    if not stamps:
        return None, ("the PDF states no readable /ModDate or /CreationDate — no bound, and no "
                      "guess in place of one")
    bound = max(stamps.values())
    how = ", ".join(f"{k} {v.isoformat()}" for k, v in sorted(stamps.items()))
    return bound, (f"{how} — the later is the bound, and a day is added to it because a PDF "
                   "timestamp carries a time zone this comparison does not")


def readings(c, conv):
    """This candidate's date under one convention, or None if it has none."""
    return c["readings"].get(conv)


def eliminate(found, bound, regime):
    """Apply the four signals in order. Returns (surviving conventions, log lines).

    Every entry in the log names the signal and the line it rests on, including the signals that
    removed nothing — a report that only lists successful eliminations reads as a report of
    certainty. Nothing here can empty the set: a signal that contradicts everything still alive
    is printed as a contradiction and applied to nothing."""
    alive = set(CONVENTIONS)
    log = []

    def drop(conv, signal, why):
        if conv not in alive:
            log.append(f"  {signal}: agrees — {why}, and {conv} was already ruled out")
        elif alive - {conv}:
            alive.discard(conv)
            log.append(f"  {signal}: RULES OUT {conv} — {why}")
        else:
            log.append(f"  {signal}: CONTRADICTION — {why}, but {conv} is the only reading left. "
                       f"Nothing is eliminated. The sheet and this signal disagree; read the "
                       f"lines above before believing either")

    # 1 — SHAPE. Per date, and it eliminates nothing by itself: it is what signal 2 acts on.
    shaped = [c for c in found if c["shape"]]
    if shaped:
        log.append("  1 shape: " + "; ".join(
            f"line {c['line']} parses only as {c['shape']}" for c in shaped[:4])
            + (f" (and {len(shaped) - 4} more)" if len(shaped) > 4 else ""))
    else:
        log.append("  1 shape: no date on this sheet has a single reading by its digits, so shape "
                   "settles nothing here")

    # 2 — THE SHEET'S OWN CONVENTION. A supplier writes dates one way, not two.
    #
    # Only a GOVERNING date is allowed to fix it, which is narrower than the premise strictly
    # needs: a print date is typeset by the same generator and is evidence of the same convention.
    # Two corpus sheets turn on that width — CHESTERTON BX5 Part B, whose only unambiguous date is
    # its print date, and DEVCON, whose only unambiguous date is its supersedes date — and both
    # stay undecided here rather than be settled by a date this gate is not about. The unused
    # evidence is printed below by name so the choice is visible instead of silent; widening it is
    # one changed list in the line under this comment, and a deliberate act.
    voters = [c for c in shaped if c["governs"]]
    votes = sorted({c["shape"] for c in voters})
    spare = [c for c in shaped if not c["governs"]]
    if len(votes) == 1:
        proved = votes[0]
        ex = next(c for c in voters if c["shape"] == proved)
        drop("m/d/y" if proved == "d/m/y" else "d/m/y", "2 the sheet's own convention",
             f"line {ex['line']} can only be read {proved}, and a supplier writes dates one way")
    elif len(votes) > 1:
        log.append("  2 the sheet's own convention: CONTRADICTION — this sheet states a governing "
                   "date that can only be d/m/y and one that can only be m/d/y. Nothing is "
                   "eliminated; the sheet does not have one convention")
    elif spare:
        log.append(f"  2 the sheet's own convention: no unambiguous GOVERNING date to fix it "
                   f"from. Line {spare[0]['line']} is unambiguous — it can only be read "
                   f"{spare[0]['shape']} — but it is labelled \"{spare[0]['word']}\", which is "
                   f"not this gate's date, and this script will not let it settle one. Read that "
                   f"line: it is evidence a person may use and this script does not")
    else:
        log.append("  2 the sheet's own convention: no unambiguous date to fix it from")

    # 3 — THE ORDER THE SHEET ITSELF STATES. 0.2.5 requires an indication of which version is
    # replaced, and a supersedes date is one of the three forms it names; so "the superseded
    # version is older" is what the required field MEANS, not a guess about how suppliers write.
    order_said = False
    for conv in CONVENTIONS:
        gov = [c for c in found if c["governs"] and readings(c, conv)]
        prior = [c for c in found if c["role"] == "prior" and readings(c, conv)]
        rev = [c for c in gov if c["revision"]]
        iss = [c for c in gov if c["issue"]]
        for older, newer, what in ((prior, gov, "the version it replaced"),
                                   (iss, rev, "its issue date")):
            if not older or not newer:
                continue
            o = max(older, key=lambda c: readings(c, conv))
            n = max(newer, key=lambda c: readings(c, conv))
            if readings(o, conv) > readings(n, conv):
                order_said = True
                drop(conv, "3 the order the sheet states",
                     f"read {conv}, line {o['line']} dates {what} "
                     f"{readings(o, conv).isoformat()}, after the revision on line {n['line']} "
                     f"({readings(n, conv).isoformat()}) that it comes before")
    if not order_said:
        log.append("  3 the order the sheet states: every reading left keeps the superseded "
                   "version older than the revision, and the issue date no later than it")

    # 4 — THE FILE'S OWN TIMESTAMP, AS A BOUND. Never as a value. See the docstring.
    if bound is None:
        log.append("  4 the file's own timestamp: not applied — there is no bound. The line at "
                   "the top of this report says why")
    else:
        # One day of slack: a PDF timestamp carries a time zone offset this comparison throws
        # away, so a same-day date must not be eliminated by an hour of arithmetic. Every
        # elimination this signal makes on the corpus clears the bound by months.
        ceiling = bound + datetime.timedelta(days=1)
        hits = {}
        for c in found:
            if c["future_ok"]:
                continue                              # a shelf life is meant to be in the future
            for conv in CONVENTIONS:
                when = readings(c, conv)
                if when and when > ceiling and conv not in hits:
                    hits[conv] = (c, when)
        for conv in CONVENTIONS:
            if conv in hits:
                c, when = hits[conv]
                drop(conv, "4 the file's own timestamp",
                     f"read {conv}, line {c['line']} dates the sheet {when.isoformat()}, after "
                     f"the last time the file itself was written ({bound.isoformat()})")
        if not hits:
            log.append(f"  4 the file's own timestamp: every reading left is on or before "
                       f"{bound.isoformat()}, so the bound removes nothing")

    likelier = "m/d/y" if regime == "US" else "d/m/y"
    order = sorted(alive, key=lambda c: c != likelier)
    return order, log


VERSION = re.compile(r"(?i)\b(?:version|revision)\s*(?:no\.?|number|#)?\s*:?\s*(\d+(?:[.,]\d+)?)\b")
REVISION_WORD = re.compile(r"(?i)\brevis")


def provision_0_2_5(text, found):
    """Evidence for Annex II 0.2.5, which is a Stage 4 question this script happens to hold the
    material for. It reports what the first page carries; rules.md § Stage 4 decides what that
    means, and states the trap: the provision illustrates the identification with the string
    "Revision: (date)" and does not mandate that spelling. Absence is the finding, not wording."""
    page_one = text.split("\f")[0] if "\f" in text else text
    first_page_lines = set(range(1, page_one.count("\n") + 2))

    dated_first_page = [c for c in found if c["line"] in first_page_lines]
    revision_first_page = [c for c in dated_first_page if REVISION_WORD.search(c["word"])]
    replaced = [c for c in found if not c["governs"] and PRIOR.search(c["word"])]
    versions = [v for v in VERSION.findall(text)]
    # What counts as evidence that the sheet HAS been revised, and what does not. The word
    # "revision" on the first page is not evidence: every EU sheet labels its date "Date of
    # issue/Date of revision" whether or not it has ever been revised, and the Chesterton Part B
    # sheet in this corpus states the same day for both. Reading that as a revision would raise a
    # 0.2.5 finding against a first edition — the wrong-ruler mistake, one restated per sheet.
    issued = {d for c in found if c["governs"] and not REVISION_WORD.search(c["word"])
              for d in c["readings"].values()}
    revised_dates = {d for c in found if c["governs"] and REVISION_WORD.search(c["word"])
                     for d in c["readings"].values()}
    moved_on = bool(issued and revised_dates and (revised_dates - issued))
    revised = bool(replaced or [v for v in versions if _above_one(v)] or moved_on)
    return {"page_one_dates": dated_first_page, "page_one_revision": revision_first_page,
            "replaced": replaced, "versions": versions, "revised": revised}


def _above_one(v):
    try:
        return float(v.replace(",", ".")) > 1
    except ValueError:
        return False


def print_0_2_5(ev, regime):
    print("\nProvision 0.2.5 — the first page and the revision trail (EU only; rules.md Stage 4 "
          "decides, this is the evidence)")
    if regime != "EU":
        print("  not applicable: this run is US, and 0.2.5 is the other regime's rulebook. "
              "§ 1910.1200(g)(2)(xvi) puts the date in Section 16 instead.")
        return
    def mark(ok):
        return "present" if ok else "NOT FOUND"
    print(f"  a date of compilation on the first page: {mark(ev['page_one_dates'])}"
          + (f" — line {ev['page_one_dates'][0]['line']}" if ev["page_one_dates"] else ""))
    if not ev["revised"]:
        print("  the sheet carries no sign of ever having been revised — no version above 1, no "
              "superseded version, no revision wording. The two obligations below do not apply.")
        return
    print(f"  that date identified as a revision: {mark(ev['page_one_revision'])}"
          + (f" — \"{ev['page_one_revision'][0]['word']}\"" if ev["page_one_revision"] else ""))
    named = ev["replaced"] or ev["versions"]
    print(f"  an indication of which version is replaced: {mark(named)}"
          + (f" — {ev['replaced'][0]['word'] if ev['replaced'] else 'version ' + ev['versions'][0]}"
             if named else ""))
    if not ev["page_one_revision"] and not named:
        print("  Neither is on this sheet. rules.md Stage 4 — read it before making the finding.")
    elif not named:
        print("  The revision trail is what is missing: nothing names the version replaced. "
              "rules.md Stage 4 decides; this script does not.")
    elif not ev["page_one_revision"]:
        print("  The sheet says it has been revised and its first-page date is not identified as "
              "a revision. That is the borderline case rules.md Stage 4 names — read it, take a "
              "reading, and write down which one you took. This script will not take it for you.")
    else:
        print("  Both are present. No 0.2.5 finding on this evidence.")


def age_in_years(when, on):
    years = on.year - when.year - ((on.month, on.day) < (when.month, when.day))
    months = (on.month - when.month - (on.day < when.day)) % 12
    return years, months


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rendering", help="the .salus.md produced by extract.py")
    ap.add_argument("--pdf", default=None,
                    help="the PDF the rendering was made from. Its /ModDate and /CreationDate are "
                         "used as an UPPER BOUND on the dates the sheet may state, and never as a "
                         "date. Absent or unreadable metadata means no bound, never a guess")
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
    found = candidates(text)
    likelier = "m/d/y" if regime == "US" else "d/m/y"
    # The prior orders what is printed. It never removes a reading — JET-LUBE is a GB-market sheet
    # written m/d/y, and a rule from the market would have been confidently wrong about it.
    print(f"run date: {today.isoformat()}   policy_max_age_years: {limit}   regime: {regime} "
          f"(so {likelier} is printed first as the likelier convention — a prior orders the "
          f"readings and never removes one)")
    bound, how = file_bound(a.pdf)
    print(f"file timestamp: {how}\n")

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
        mark = "" if c["governs"] else f"   ({c['role']}, not the gate: \"{c['word']}\")"
        print(f"line {c['line']}: {c['text'][:96]}{mark}")
        for conv in sorted(set(c["readings"].values())):
            names = sorted(k for k, v in c["readings"].items() if v == conv)
            y, mo = age_in_years(conv, today)
            print(f"    {conv.isoformat()}  ({' and '.join(names) if len(names) < 2 else 'either convention'})"
                  f"  {y} years {mo} months old")
        print()

    alive, log = eliminate(found, bound, regime)
    print("Eliminating readings — each signal removes, none invents:")
    for line in log:
        print(line)
    if len(alive) == 1:
        print(f"  → one reading survives: this sheet's dates are read {alive[0]}.\n")
    else:
        print("  → both readings survive. The document does not settle which convention it "
              "uses.\n")

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
    for conv in alive:
        dates = [readings(c, conv) for c in governing if readings(c, conv)]
        if not dates:
            continue
        newest = max(dates)
        y, mo = age_in_years(newest, today)
        verdicts[conv] = (newest, y, mo, y >= limit)

    if not verdicts:
        print("No governing date has a reading under the convention that survived. That is a "
              "contradiction between the sheet and the signals above, not a result. Read the "
              "sheet.")
        return 0

    for conv in alive:
        if conv not in verdicts:
            continue
        newest, y, mo, over = verdicts[conv]
        print(f"newest governing date, reading every date as {conv}: {newest.isoformat()} — "
              f"{y} years {mo} months old on the run date"
              f"{'  → AT OR PAST the house limit' if over else '  → inside the house limit'}")
    print()

    outcomes = {v[3] for v in verdicts.values()}
    if len(outcomes) > 1:
        print(f"THE TWO CONVENTIONS DISAGREE, AND THE DOCUMENT DOES NOT SETTLE IT. Every signal "
              f"above has been applied and both readings survive. Read as {likelier} — the "
              f"likelier one for a {regime} run — this sheet is "
              f"{'over' if verdicts[likelier][3] else 'inside'} the limit; read the other way it "
              "is not. A person decides which convention the supplier used, from the sheet's own "
              "language and origin. This script will not choose for you.")
    elif True in outcomes:
        print(f"A HOUSE-POLICY FINDING IS OWED: the sheet is at or past {limit} years on every "
              "reading that survived. rules.md Stage 2 — the finding is marked [HOUSE POLICY — "
              "no provision], names policy_max_age_years, and is not a breach of either standard, "
              "because neither sets an expiry.")
    else:
        print(f"NO FINDING IS OWED: on every reading that survived the sheet is inside the "
              f"{limit}-year house limit. Record the age and continue (rules.md Stage 2) — a "
              "report that performed the check and says nothing about it reads as one that "
              "skipped it.")

    if len(outcomes) == 1 and len({v[0] for v in verdicts.values()}) > 1:
        dates = " and ".join(sorted(v[0].isoformat() for v in verdicts.values()))
        print(f"\nBut the DATE is still not settled: the surviving readings make it {dates}, and "
              "the answer above holds for both. Record whichever the sheet's own language makes "
              "right, and say in the report that the sheet writes it ambiguously. The verdict "
              "does not turn on it here; the date you quote does.")

    print_0_2_5(provision_0_2_5(text, found), regime)

    print("\nWhat this cannot tell you: whether the words beside a date meant what they say, and "
          "whether a date it never found is printed somewhere it could not parse. If one reading "
          "survived, it survived because the other was ruled out by the signal named above — not "
          "because this script knows what the supplier meant. The evidence is above with line "
          "numbers; the reading is yours.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
