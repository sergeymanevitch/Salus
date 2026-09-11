# config/ — what a run is bound to before it reads a sheet

One file, read at `rules.md` Stage 0, before the sheet is opened.

| File | What it sets |
| --- | --- |
| `jurisdiction.md` | the regime this installation audits under — `EU` or `US` — and the house age gate |

## The contract

- **Jurisdiction is never inferred.** Not from a locale, not from an IP address, not from where the
  supplier sits, and not from the sheet itself. A reviewer in one country may be auditing for a
  legal entity in another. This file is the answer.
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
| `tools/check_scope.py` | yes, as the authority | it decides about a live sheet, and `rules.md` Stage 0 says the configured regime is the answer |
| `tools/verify_citations.py` | yes, as a cross-check only | it decides about a *filed report*, and takes the regime from that report's own header row. A disagreement with this file is printed as a NOTE, not a failure |
| `tools/validate_report.py` | no | same reason: the report's header row is what it reads |
| `tools/extract.py` | no | conversion is regime-blind |

The corpus rule above — EU runs cite the EU corpus, US runs cite `reference/us-osha-hcs/` only — is
now mechanical: Gate 2 fails any finding that reaches outside the regime its report declares. Until
2026-09-11 it was stated in three files and enforced in none, and it had already been broken once
here and repaired by hand.

## Known limit

**`policy_max_age_years` is still read by no script.** A run that ignores it is caught by a reader
rather than by a gate — which is the second-best outcome, and is recorded here rather than left to
be discovered. The gates check that an age finding which *is* made is marked `[HOUSE POLICY — no
provision]`; nothing checks that one which should have been made was.
