# audits/ — one folder per run

A run is a folder named `YYYY-MM-DD-<sheet-slug>`, and it holds three things. All three ship
together, always: a finding nobody can check against the document it describes is not evidence.

| File | What it is |
| --- | --- |
| `report.md` | the verdict, the findings, what passed, the declared blind spots |
| `<sheet>.salus.md` | the rendering the auditor actually read — the extraction, with a line number on every line |
| `<sheet>.fidelity.json` | the evidence that rendering lost nothing, and the limits of that evidence |

The line numbers in the rendering are what every `WHERE` line in the report points at. That is the
whole reason the rendering ships beside the report rather than being regenerated on demand: a
reader six months from now opens the same file the auditor opened, not a new extraction from a
newer version of a tool.

## The seven runs here

| Run | Regime | Verdict | What it is for |
| --- | --- | --- | --- |
| `2026-09-11-bg-hcf` | EU | DOES NOT CONFORM | four findings and two passes; the one to read to see how a finding cites a provision. Its conversion gate returned REVIEW, not PASS, and the report says so twice |
| `2026-09-11-dowsil-ap` | EU | CONFORMS | six checks, all passed; an audit reports what held, not only what broke |
| `2026-09-11-carboguard-us` | US | DOES NOT CONFORM | the US path. A smaller audit than the EU ones, because 1910.1200 publishes less that can be cited — and the report says which claims it is not making |
| `2026-09-11-weicon-truncated` | EU | DOES NOT CONFORM | incomplete is not unreadable. Four of sixteen sections, perfectly legible; the document's own pagination is the evidence |
| `2026-09-11-scanned-fixture` | — | CANNOT VERIFY | stops at Stage 1 and cites no provision at all, because none was applied |
| `2026-09-11-jetlube-fmg-nlgi2` | EU | DOES NOT CONFORM | a sheet that is not classified and still fails three times: a forbidden reassurance in 2.1, a revision with no indication of what changed, flammability marked not applicable on a solid. Section 3 names no substance, so Stage 5 ran no lookup at all — and the report says that rather than implying a clean classification |
| `2026-09-11-nye-ts2024-china` | EU | DOES NOT CONFORM | a sheet compiled to the Chinese GB/T standards and audited against Annex II because that is what the settings file says. Eleven findings, and they are one defect seen eleven times: no Part B subsections, no chemical identity in Section 3, no PBT/vPvB determination, no Union provisions in Section 15. The report says what it is not claiming — GB/T 16483 is not shipped, so it makes no judgement about the sheet in its own regime |

`2026-09-11-weicon-truncated` and `2026-09-11-scanned-fixture` sit either side of the line that is
easiest to get wrong under pressure.

## Before a run is added here

All three gates must pass on it — `tools/CONTEXT.md` names them and their order. A report that has
not passed them has not been produced, and must not be filed here as though it had.
