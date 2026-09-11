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

## The three runs here

| Run | Verdict | What it is for |
| --- | --- | --- |
| `2026-09-11-bg-hcf` | DOES NOT CONFORM | four findings and two passes; the one to read if you want to see how a finding cites a provision. Its conversion gate returned REVIEW, not PASS, and the report says so twice |
| `2026-09-11-dowsil-ap` | CONFORMS | six checks, all passed; shows that an audit reports what held, not only what broke |
| `2026-09-11-scanned-fixture` | CANNOT VERIFY | stops at Stage 1 and cites no provision at all, because none was applied |

All three are EU runs. The US path is implemented and not yet exercised end to end.

## Before a run is added here

All three gates must pass on it — `tools/CONTEXT.md` names them and their order. A report that has
not passed them has not been produced, and must not be filed here as though it had.
