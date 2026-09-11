# Salus — entry file

An auditor for safety data sheets. `README.md` is written for the person using or judging it; this
file is the route for anyone — or anything — about to *do* an audit with the folder.

## Read in this order, and stop where it says

1. **`identity.md`** — who the auditor is, the three verdicts, the hard boundaries, the declared
   blind spots. Short, and the boundaries in it are not negotiable.
2. **`config/jurisdiction.md`** — EU or US, and the house age gate. If it is not filled in, the
   verdict is CANNOT VERIFY and the audit stops there. EU and US are the whole of the scope: a
   sheet compiled to a third country's standard stops at Stage 1b with CANNOT VERIFY, out of
   scope, and is never audited against the configured standard instead.
3. **`rules.md`** — the seven stages, in order, with the finding format and the token discipline.
4. **`reference/`** — only at the provision you are about to cite. `reference/CONTEXT.md` routes.

**Do not read `reference/` end to end.** It is roughly 450 KB of regulation. `rules.md` says how to
open it: one Annex VI row per CAS or Index number, one provision at a time. A whole run should cost
a few thousand tokens, and it only does if that rule is kept.

## Then

- `tools/CONTEXT.md` — which script is a gate, which is maintenance, and the order they run in.
- `audits/CONTEXT.md` — what a run folder must contain before it may be filed.
- `examples.md` — five finished runs, covering all three verdicts and both regimes, if you want to
  see the shape before working.

## The one thing that ends a run before it starts

Run `python3 tools/check_scope.py <sheet>.salus.md` after converting and before auditing. Exit 2
means the sheet declares a standard this folder does not ship — the run stops, the verdict is
CANNOT VERIFY, and no stage after 1b is performed. Auditing such a sheet anyway produces findings
that are all one finding wearing different numbers; it happened here once, and
`README.md` § *An incident, and the gate it produced* is the record of it.

## The two things that void a run

A report that cites a provision it cannot quote, and a report that says anything about the material
rather than the document. Gates 2 and 3 catch both after the fact, but they are written down here
because catching them afterwards is the second-best outcome.
