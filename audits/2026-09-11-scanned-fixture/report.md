# Salus audit report

| | |
| --- | --- |
| Sheet | `CONSTRUCTED - scanned sheet, no text layer.pdf` (from `test-cases/sds-constructed/`) |
| Jurisdiction (from `config/jurisdiction.md`) | EU |
| Standard applied | none — the audit did not reach a standard |
| Run date | 2026-09-11 |
| Standards knowledge last confirmed online | 2026-09-11 — see `reference/FRESHNESS-LOG.md` |
| Conversion gate | NO TEXT LAYER |

## VERDICT: CANNOT VERIFY

The audit stopped at Stage 1 of `rules.md`. No provision was applied, no section was assessed, and
nothing below is a statement about this document's compliance.

**Reason.** The file opens and renders as one page, and it is an image. `pdftotext` returns one
character from the whole document and the independent engine returns none. There is no text layer.
Salus could not establish *what it would be checking*, so it did not check anything.

**Evidence.** `fidelity.json` for this run records `"verdict": "NO TEXT LAYER"`, `chars_primary: 0`,
and a `page_density` entry flagging its single page as carrying no extractable text.

**Corrected 2026-09-11.** The two sentences above read *two pages* and *both pages* when this report
was filed; the sheet has one page, and `pdfinfo` says so. The count came out of `fidelity.json`,
which counted a page that does not exist: `pdftotext` ends every page with a form feed including the
last, and `tools/extract.py` split on it without discarding the empty tail. The wrong count is the
instrument's and the report repeated it. `tools/extract.py` is fixed, the fidelity report for this
run is regenerated from the same PDF, and nothing else here moves — no finding on this run rested on
the page count, and the verdict does not.

**What this is not.** CANNOT VERIFY is not a failure and not a pass. A sheet that cannot be read is
not thereby a defective sheet — this one is a rasterised copy of a perfectly ordinary Devcon sheet,
and the original passes the conversion gate without complaint. The defect is in the copy that
arrived, not in the document the supplier wrote.

**What would change it.** Any of these, and the audit runs normally:

- the original PDF from the supplier rather than a scan of a print-out;
- the same file with a text layer, from OCR — with the caveat that an OCR layer is a *transcription*
  and this auditor would then be checking the transcription, not the sheet, which is a weaker claim
  and would be recorded as such on the report;
- the sheet in any other machine-readable form the supplier can issue.

## Declared blind spots

Stated whether or not they bit here. On this run the first one is the whole story.

- **Salus cannot read what is not text.** It has no OCR and does not guess at pixels. On a safety
  document, a plausible reconstruction of an unreadable value is worse than no answer, because it
  looks exactly like an answer.
- **Omissions are invisible** — not reached on this run.
- **Self-classified substances cannot be called wrong** — not reached on this run.
- **No value is re-measured** — not reached on this run.

## Why this fixture exists

The twenty-one real sheets in `test-cases/sds/` all carry a text layer, so none of them exercises
this path. A scanned sheet is one of the commonest things a reviewer is actually handed, and an
auditor that has never been shown one does not know it is supposed to stop. `test-cases/sds-constructed/CONTEXT.md`
records exactly how this file was built, from which sheet, so nobody mistakes it for a
manufacturer's document.
