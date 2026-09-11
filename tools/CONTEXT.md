# tools/ — what runs, and when

Eight scripts. Nothing here decides anything about a sheet — the audit is the reading — with one
exception, and it is the exception that ends runs: the scope gate decides whether this folder holds
a rulebook for the sheet at all. Around that: one script prepares the sheet, three guard the answer,
one holds the documentation to the format it teaches, and two keep the standards current.

## Run for every audit, in this order

| Order | Script | Job | Fails the run when |
| --- | --- | --- | --- |
| 1 | `extract.py` | turn the PDF into the line-anchored rendering the auditor reads, and write the evidence that nothing was lost | never — it reports, it does not gate |
| 2 | `verify_conversion.py` | **Gate 1** · re-derive that evidence from the PDF and the rendering on disk, rather than trusting the JSON | a chemical identifier is missing, or the rendering is no longer the extraction |
| 3 | `check_scope.py` | **the scope gate** · does this folder hold the standard the sheet was compiled to? Reads the sheet's own declaration | the sheet declares a third regime — GB/T, JIS, GOST, SOR/2015-17 — and not the configured one. Exit 2: the verdict is CANNOT VERIFY, out of scope, and **no further stage runs** |
| 4 | *the audit itself* | `rules.md` Stages 2–6 — a person or a model, not a script | — |
| 5 | `verify_citations.py` | **Gate 2** · read the finished report and check every quoted provision against the file it names, **and that the provision belongs to the corpus the report's own regime may cite** | the report and the standard disagree; a citation reaches outside the regime's corpus — CLP Annex VI or Annex II in a US report, 1910.1200 in an EU one; the report names no regime at all |
| 6 | `validate_report.py` | **Gate 3** · verdict shape, finding class, **the regime named in the header**, declared blind spots, the ban on permission language, and that a report which performed checks says what passed | any of those, in English or Russian; also a header that declares one regime and applies the other regime's standard, and a US run that does not record Section 3 as *not assessed for classification correctness* |

The scope gate is third in the order and first in consequence: it is the only script here that can
end a run before it begins. It exists because on 2026-09-11 a sheet compiled to GB/T 16483 was
audited against Annex II from beginning to end and filed with eleven findings — accurate readings,
all of them, of a document that had never been written to that standard. `README.md` § *An incident,
and the gate it produced* has the whole story; `audits/2026-09-11-nye-ts2024-china/` is the retracted
run and the folder beside it is the same sheet done correctly.

Gate 2 is the one that matters most and is the easiest to get wrong. It reads the **report**. A
checker that only re-reads the standard proves the standard has not moved; it would pass a report
whose findings had drifted away from the text they cite.

## Which jurisdiction a report gate believes

Gates 2 and 3 take the regime from the **report's own header row**, not from `config/jurisdiction.md`.
`check_scope.py` does the opposite, and the two are not inconsistent: the scope gate decides about a
live sheet in a live run, where the config is the authority (`rules.md` Stage 0), while the report
gates decide about a filed record, which carries the regime it was made under in its header. A filed
report does not change regime when the setting changes.

The consequence is the point. `audits/` holds seven EU runs and one US run, checked together, against
one config file that can say only one thing — so a gate that trusted the config would fail the US
report on any installation set to EU, and the other seven on any installation set to US. Every fresh
clone would light up. Gate 2 still reads the config and prints a **NOTE** when the two disagree, which
during a live run is the auditor being told the header and the setting have parted company.

A report that declares **no** regime fails both gates. It is not treated as "fall back to the config":
if a missing row meant that, deleting one line from a header would be enough to cite any regulation in
`reference/` against any sheet, and a guard the guarded document can switch off is not a guard.

## Run after editing the documentation

| Script | Job |
| --- | --- |
| `test_docs_example.py` | lift the worked finding out of `rules.md` and put it through Gates 2 and 3. The file that teaches the citation format must not teach a format the gates reject |

## Run only when there is a network

| Script | Job |
| --- | --- |
| `check_freshness.py` | ask the publishers what exists now, write `reference/FRESHNESS-LOG.md`. Never edits the ledger — promoting a published revision to *in force* is a legal reading and belongs to a person |
| `build_reference.py` | re-download the three standards and regenerate everything under `reference/`, with SHA-256 provenance for source and output |

An audit never calls either one. That is why the folder works with no connection, and why it still
knows how old its own knowledge is.

## Conventions

- Every script exits non-zero when it fails, so they chain in a shell without reading the prose.
- Every script carries its method **and its limits** in its own docstring. `extract.py` states the
  thing its fidelity check cannot prove; read it before quoting the check at anyone.
- `.cache/` holds the downloaded publisher markup. It is gitignored: large, reproducible, and not
  ours. What ships is the generated text under `reference/`, with its hashes.
