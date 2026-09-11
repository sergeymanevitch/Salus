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

## Known limit

This file is honoured because `rules.md` says to honour it. **No script reads it.** Not the gates,
not the extractor. A run that ignores `policy_max_age_years`, or that cites the EU corpus while
configured for US, is caught by a reader rather than by a gate — which is the second-best outcome,
and is recorded here rather than left to be discovered.
