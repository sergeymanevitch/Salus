# Salus audit report

| | |
| --- | --- |
| Sheet | `SDS_CHINA_English_TS+2024.pdf` — TS 2024, SDS No TS2024, Version 01, Nye Lubricants, Inc., A Member of the FUCHS Group (from `test-cases/sds/`) |
| Jurisdiction (from `config/jurisdiction.md`) | EU |
| Standard applied | none — the run stopped before a standard could apply |
| Run date | 2026-09-11 |
| Standards knowledge last confirmed online | 2026-09-11 — see `reference/FRESHNESS-LOG.md` |
| Conversion gate | PASS — coverage 100.0000 %, five pages, 10,403 characters, no chemical identifier lost |
| Scope gate | OUT OF SCOPE — `python3 tools/check_scope.py` exits 2 on this sheet |

**Corrected 2026-09-11.** The conversion-gate row above read *six pages* when this report was filed;
the sheet has five, and the findings section of the companion run counts them correctly as 1/5 to
5/5. The six came out of `fidelity.json`, which counted a page that does not exist: `pdftotext` ends
every page with a form feed including the last, and `tools/extract.py` split on it without
discarding the empty tail. The wrong count is the instrument's and the report repeated it.
`tools/extract.py` is fixed and the fidelity report for this run is regenerated from the same PDF.
Nothing else here moves: the run stopped on scope, and no part of that turned on how long the sheet
is.

## VERDICT: CANNOT VERIFY

The audit stopped at Stage 1 of `rules.md`, on scope. No provision was applied, no section was
assessed, and nothing below is a statement about this document's compliance.

**Reason.** The sheet declares the standard it was compiled to, on its first line:

> `Prepared in accordance with GB/T 16483 and GB/T 17519.`

and again in Section 15, where it lists the Chinese laws and standards it conforms to, among them
*Safety Data Sheet for Chemical Products — Content and Order of Sections (GB/T 16483-2008)*. It
declares neither Commission Regulation (EU) 2020/878 nor 29 CFR 1910.1200 anywhere. Those two are
the only rulebooks Salus ships, in `reference/`. GB/T 16483 is not among them.

So there is nothing to check this sheet against. An auditor without the standard a document was
written to cannot say whether the document meets it, and saying so plainly is the whole answer.

**Evidence.** `tools/check_scope.py` reads the rendering beside this report and exits 2, naming the
two declarations and the line each was found on. The conversion gate had already passed, so this is
not an unreadable sheet — it is a perfectly legible sheet written to a rulebook that is not here.

**What this is not.** This is not a finding against the sheet, and not a verdict of any kind about
it. Audited against its own standard by someone who holds that standard, this document may well be
exemplary; Salus makes no claim either way and has no basis for one. Nor is it a statement about the
material: that boundary holds on every run, including the ones that stop.

**What would change it.** Either of these, and the audit runs normally:

- the version of this sheet compiled to Annex II of Regulation (EC) No 1907/2006, if the supplier
  issues one for the EU market — most multinational suppliers do, and the two are different
  documents, not translations of one another;
- `config/jurisdiction.md` set to a regime whose standard this sheet declares. Salus ships EU and
  US only, so today that is not available for GB/T, and adding a third standard to `reference/` is
  a deliberate act with a provenance record, not a setting.

## Declared blind spots

Stated whether or not they bit here. On this run the scope stop is the whole story, and the rest
were never reached.

- **Salus holds two rulebooks and no others.** It cannot read a sheet against a standard it does
  not ship, and it does not approximate one standard with another. GB/T 16483 and Annex II are both
  descendants of the GHS, which is exactly what makes the approximation tempting and wrong: the
  section order, the mandatory subheadings and the disclosure thresholds differ.
- **Omissions are invisible** — not reached on this run.
- **Self-classified substances cannot be called wrong** — not reached on this run.
- **No value is re-measured** — not reached on this run.

## Why this run exists

It is the corrected form of a run that went wrong. On 2026-09-11 this same sheet was audited all the
way through against Annex II and filed as DOES NOT CONFORM with eleven findings, in
`audits/2026-09-11-nye-ts2024-china/`. That report is retracted and kept where it is, with a notice
at its head. Both runs ship, side by side: what the folder did, and what it does now.

`README.md` § *An incident, and the gate it produced* tells the story, and
`test-cases/sds/CONTEXT.md` records what this sheet is and why it is in the corpus.
