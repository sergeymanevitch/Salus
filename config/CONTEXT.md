# config/ — what a run is bound to before it reads a sheet

One file, read at `rules.md` Stage 0, before the sheet is opened.

| File | What it sets |
| --- | --- |
| `jurisdiction.md` | the regime this installation audits under — `EU` or `US` — and the house age gate |

## The contract

- **Jurisdiction is never inferred.** Not from a locale, not from an IP address, not from where the
  supplier sits, and not from the sheet itself. A reviewer in one country may be auditing for a
  legal entity in another. This file is the answer.
- **Where this file cannot be edited, the person states the regime instead.** In a Claude project
  there is no editor and no shell, so the regime is given in the opening message and the report's
  header row records it as the setting that run was made under. That is still a *stated* setting:
  the rule above forbids inferring a regime, not receiving one from the person who knows it.
  `README.md` § *Quick start — in a Claude project* carries the wording.
- **Unfilled is not a default.** With no regime set the verdict is CANNOT VERIFY and the run stops
  at Stage 0. Guessing would produce findings under a regulation that may not govern the sheet.
- **What it selects.** An EU run may cite `reference/eu-2020-878/` and `reference/eu-clp-annex-vi/`.
  A US run may cite `reference/us-osha-hcs/` only, and skips Stage 5 entirely, because 29 CFR
  1910.1200 carries no harmonised classification list and none is shipped for it.
- **The age gate is house policy.** `policy_max_age_years` rests on no provision in either standard,
  and every finding it produces is marked `[HOUSE POLICY — no provision]`.

## What reads this file, and what does not

| Script | Reads it | For what |
| --- | --- | --- |
| `tools/read_config.py` | yes, and it is the only parser | every other script asks it. It resolves all four settings and fails by name on one that cannot be honoured as written — a regime not shipped, a threshold that is not a number, a `run_date` that is not ISO or lies in the future |
| `tools/check_scope.py` | yes, as the authority | it decides about a live sheet, and `rules.md` Stage 0 says the configured regime is the answer. Anything else wrong with the file it prints as a NOTE and runs anyway: it decides about the standard, not the age gate |
| `tools/verify_citations.py` | yes, as a cross-check only | it decides about a *filed report*, and takes the regime from that report's own header row. A disagreement with this file is printed as a NOTE, not a failure |
| `tools/validate_report.py` | yes, as a cross-check only | the report's own header row is what it judges: the run date it was made on, and the threshold any house-policy finding names. Where this file now says something different, that is a NOTE — a filed report keeps the settings it was made under |
| `tools/extract.py` | no | conversion is regime-blind |

The corpus rule above — EU runs cite the EU corpus, US runs cite `reference/us-osha-hcs/` only — is
now mechanical: Gate 2 fails any finding that reaches outside the regime its report declares. Until
2026-09-11 it was stated in three files and enforced in none, and it had already been broken once
here and repaired by hand.

## Known limit

**The arithmetic is mechanical; the reading is not, and it is not going to be.** As of 2026-09-11
the settings are parsed and validated (`tools/read_config.py`); `tools/check_age.py` finds the
dates a rendering states, removes the readings the document itself rules out, measures the newest
governing one against `policy_max_age_years` and the run date, and says whether a finding is owed;
and Gate 3 refuses a report with no run date, or a house-policy finding that does not name the
threshold it rests on.

`03/04/2026` is still two dates, and that part narrowed on 2026-09-11. Four signals now eliminate
readings — shape, the sheet's own convention, the order the sheet states between its own dates, and
the file's own timestamp as an upper bound (`--pdf`) — each printed with the line it rests on, each
able only to remove a reading and never to supply one. On the 22 corpus sheets that leaves two
whose date is genuinely unsettled, and no sheet where an ambiguity changes the verdict.

What remains is a judgement, and `check_age.py` is built to hand it back rather than to make it:

- **Which date governs is still a reading.** The shipped Carboguard sheet carries a print date a
  year after its revision date. The script prints the words that stood beside each date; that they
  meant what they say is a person's conclusion, not the script's.
- **An eliminated reading is not a proved one.** Where one reading survives, it survived because
  the others were ruled out by the signal named beside it. Where two survive, the script prints
  both and says the document does not settle it — and it will never remove the last one: the corpus
  holds a sheet whose stated dates are later than its own file timestamp, and a bound with no floor
  would have "resolved" it into a date the sheet does not state.
- **The file's timestamp is a bound and never a date.** It is read only to eliminate. Metadata can
  be stripped, rewritten, or simply wrong; three corpus sheets carry none this tool can read, and
  when it is absent the ambiguity comes back rather than a guess taking its place. `README.md`
  claim 10 is the command that shows it doing so.
- **A parser has blind spots, and a blind spot here is a verdict.** `rules.md` Stage 2 turns *no
  date found* into CANNOT VERIFY, so the script lists every line that claims a date it could not
  parse instead of reporting silence as absence. One sheet in this corpus was filed that way by a
  missing `Revision:` — the form Annex II 0.2.5 prescribes — until the vocabulary was widened.
- **Nothing forces the auditor to run it.** No gate fails a report for skipping Stage 2; a report
  that performed checks and says nothing about the age is caught by a reader, as before.

That last one is the honest boundary, and it is the same one every Salus report declares about the
sheet it audits: the gates check what was written, and an omission is invisible to them.
