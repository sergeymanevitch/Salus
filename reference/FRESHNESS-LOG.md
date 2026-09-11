# Freshness log

Written by `tools/check_freshness.py`. This file is the memory an offline run reads:
it says what was true the last time this folder could reach the publishers, and when
that was. It does not change `STANDARDS-LEDGER.md` — promoting a published revision to
'in force' is a legal reading and belongs to a person.

Last run: **2026-09-11**

## EU — Commission Regulation (EU) 2020/878

- held in `reference/`: `32020R0878`
- checked: 2026-09-11
- result: reachable, HTTP 200
- action: none

## EU — CLP Annex VI (Regulation (EC) No 1272/2008, consolidated)

- held in `reference/`: `02008R1272-20260701`
- checked: 2026-09-11
- result: no newer consolidated version found (2 probe(s), all answered)
- action: none

## US — 29 CFR 1910.1200

- held in `reference/`: `eCFR point-in-time 2026-09-01`
- checked: 2026-09-11
- result: latest amendment date reported by eCFR: 2026-02-13
- action: none

---

If this log is old, an audit run today does not silently pretend otherwise. `rules.md` Stage 3 requires the report to state the date above, so a reader always knows how fresh the auditor's knowledge of the calendar was.
