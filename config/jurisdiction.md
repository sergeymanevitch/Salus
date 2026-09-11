# Jurisdiction settings

Fill this in before the first audit. Salus reads it at Stage 0 of `rules.md` and stops if it has
not been set.

```yaml
jurisdiction: EU        # EU | US  — required, no default
organisation: ""        # free text, appears in the report header
policy_max_age_years: 5 # the house age gate; see below
run_date: auto          # auto = today; or an ISO date, to reproduce an old run exactly
```

## Why this is a file and not a guess

Salus never infers the regime from an IP address, a system locale, or where the supplier is
registered. A reviewer sitting in Tel Aviv may be auditing for a German legal entity; a reviewer
in Berlin may be auditing a sheet destined for a US plant. Location is not jurisdiction.
Employment is, and only the person filling in this file knows it.

`jurisdiction` selects which standard the audit runs against:

| Value | Standard applied |
| --- | --- |
| `EU` | Commission Regulation (EU) 2020/878, with CLP Annex VI for classification |
| `US` | 29 CFR 1910.1200 |

A sheet compiled for **the other regime Salus ships** is still audited against the configured one,
and the mismatch is reported as a finding — that is the useful answer, because a US-format sheet
does not satisfy an EU obligation however well it is written, and both rulebooks are in
`reference/` so the comparison rests on text.

A sheet compiled to **a standard Salus does not ship** — GB/T 16483, JIS Z 7253, GOST 30333,
SOR/2015-17 — is a different case and is **not** audited at all. The run stops at Stage 1b of
`rules.md` with CANNOT VERIFY, out of scope. Setting `jurisdiction` does not make a third regime
auditable: it selects between the two standards that are here, and there is no third value.

The distinction is not pedantry. Auditing a GB/T sheet against Annex II produces one observation —
the wrong ruler was used — restated once per provision, and a reader cannot tell that list from a
list of real defects. It happened here on 2026-09-11; `README.md` § *An incident, and the gate it
produced* records it.

## `policy_max_age_years`

This is **not** in either standard. Neither 2020/878 nor 1910.1200 sets an expiry date for a
safety data sheet. The gate exists because formulations change faster than sheets are reissued,
and a reviewer needs a trigger to go back to the manufacturer.

Set it to your organisation's rule. Set it to `0` to turn it off. Whatever it is, findings it
produces are marked `[HOUSE POLICY — no provision]` in the report and are never dressed up as
regulatory breaches. See `rules.md`, "Two classes of finding, never mixed."

## `run_date`

Leave it on `auto`. Set an explicit date only to reproduce a past run — the age gate and the
transition-window checks both depend on what day it is, so an audit from 2024 cannot be
reproduced with today's calendar.
