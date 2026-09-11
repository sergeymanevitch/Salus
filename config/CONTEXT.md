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

**Nothing computes a sheet's age.** Since 2026-09-11 the settings are parsed and validated
(`tools/read_config.py`), and a house-policy finding that *is* made must carry its class marker and
must name the `policy_max_age_years` it rests on — Gate 3 refuses one that does not, and refuses a
report with no run date to measure any age from. What no script does is read the issue date off the
sheet and work out whether a finding was owed. A run that should have raised the age gate and did
not is still caught by a reader rather than by a gate.

That is the second-best outcome and it is written here rather than left to be discovered. It is
also the honest boundary: the gates check what the report says, and an omission is invisible to
them — the same limit every Salus run declares about the sheet it audits.
