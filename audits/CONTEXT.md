# audits/ — one folder per run

A run is a folder named `YYYY-MM-DD-<sheet-slug>`, and it holds three things. All three ship
together, always: a finding nobody can check against the document it describes is not evidence.

| File | What it is |
| --- | --- |
| `report.md` | the verdict, the findings, what passed, the declared blind spots |
| `<sheet>.salus.md` | the rendering the auditor actually read — the extraction, with a line number on every line |
| `<sheet>.fidelity.json` | the evidence that rendering lost nothing, and the limits of that evidence |

`report.md` opens with a header table, and two rows of it are load-bearing rather than descriptive:

    | Jurisdiction (from `config/jurisdiction.md`) | EU |
    | Run date | 2026-09-11 |

The first is where Gates 2 and 3 read the regime from, and it decides which corpus the findings are
allowed to cite. A report without it fails both gates. `tools/CONTEXT.md` § *Which jurisdiction a
report gate believes* says why the row and not the config file is what a report gate trusts.

The second is the day the run speaks for. Every age in the report, and every *confirmed current*
date a finding carries, is measured from it, so a report that does not name it states nothing a
reader can re-derive a year later. ISO, `YYYY-MM-DD`, because `03/04/2026` is two dates. Gate 3
refuses a report that carries no such row, and refuses a `[HOUSE POLICY — no provision]` finding
that does not name the `policy_max_age_years` it rests on: a threshold nobody can see is one a
reader cannot tell from an invented one.

Both rows are read out of the **report** and never out of `config/jurisdiction.md`. A filed record
keeps the settings it was made under; where they differ from this installation's today, Gate 3
prints a NOTE and delivers the report.

The line numbers in the rendering are what every `WHERE` line in the report points at. That is the
whole reason the rendering ships beside the report rather than being regenerated on demand: a
reader six months from now opens the same file the auditor opened, not a new extraction from a
newer version of a tool.

## The eight runs here

| Run | Regime | Verdict | What it is for |
| --- | --- | --- | --- |
| `2026-09-11-bg-hcf` | EU | DOES NOT CONFORM | four findings and two passes; the one to read to see how a finding cites a provision. Its conversion gate returned REVIEW, not PASS, and the report says so twice |
| `2026-09-11-dowsil-ap` | EU | CONFORMS | six checks, all passed; an audit reports what held, not only what broke |
| `2026-09-11-carboguard-us` | US | DOES NOT CONFORM | the US path. A smaller audit than the EU ones, because 1910.1200 publishes less that can be cited — and the report says which claims it is not making |
| `2026-09-11-weicon-truncated` | EU | DOES NOT CONFORM | incomplete is not unreadable. Four of sixteen sections, perfectly legible; the document's own pagination is the evidence |
| `2026-09-11-scanned-fixture` | — | CANNOT VERIFY | stops at Stage 1 and cites no provision at all, because none was applied |
| `2026-09-11-jetlube-fmg-nlgi2` | EU | DOES NOT CONFORM | a sheet that is not classified and still fails three times: a forbidden reassurance in 2.1, a revision with no indication of what changed, flammability marked not applicable on a solid. Section 3 names no substance, so Stage 5 ran no lookup at all — and the report says that rather than implying a clean classification |
| `2026-09-11-nye-ts2024-china` | EU | **RETRACTED** | **the run that should never have happened.** A sheet compiled to the Chinese GB/T standards, audited against Annex II from beginning to end, filed with eleven findings that are one observation restated — the wrong ruler was used. Kept in place, retracted with a notice at its head, because deleting the evidence of a bad run is the one thing an auditor may not do. It produced the scope gate |
| `2026-09-11-nye-ts2024-china-scope-stop` | EU | CANNOT VERIFY | the same sheet, done correctly: `tools/check_scope.py` exits 2, the run stops at Stage 1b, no provision is applied and no finding is made. The shape of every out-of-scope run from now on |

`2026-09-11-weicon-truncated` and `2026-09-11-scanned-fixture` sit either side of the line that is
easiest to get wrong under pressure.

## Before a run is added here

Every check must pass on it — `tools/CONTEXT.md` names them and their order, and `README.md`
§ *How it works* numbers them one to five. A report that has not passed them has not been produced,
and must not be filed here as though it had.

The scope gate is CHECK 2, and it is not a report gate: run
`python3 tools/check_scope.py <run>/<sheet>.salus.md` **before** auditing. Exit 2 means this folder
holds no rulebook for the sheet, and the only run that may be filed is the stop itself —
`2026-09-11-nye-ts2024-china-scope-stop/` is its shape. Gates passing is not evidence that a run
should have been made: the retracted run beside it passed every gate that existed that morning.
