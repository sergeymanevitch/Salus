# tools/ — what runs, and when

Nine scripts. Nothing here decides anything about a sheet — the audit is the reading — with one
exception, and it is the exception that ends runs: the scope gate decides whether this folder holds
a rulebook for the sheet at all. Around that: one script prepares the sheet, four guard the answer,
one holds the documentation to the format it teaches, and two keep the standards current.

## Run for every audit, in this order

| Order | Script | Job | Fails the run when |
| --- | --- | --- | --- |
| 0 | `verify_reference.py` | **Gate 0** · rehash every generated file under `reference/` against the SHA-256 recorded in its `PROVENANCE.md` | a shipped standard has changed, is missing, or an unrecorded file has appeared in a generated folder. Gate 2 runs this itself before checking a single citation, so it needs no place in the audit's own sequence — run it alone to ask about the corpus rather than about a report |
| 1 | `extract.py` | turn the PDF into the line-anchored rendering the auditor reads, and write the evidence that nothing was lost | never — it reports, it does not gate |
| 2 | `verify_conversion.py` | **Gate 1** · re-derive that evidence from the PDF and the rendering on disk, rather than trusting the JSON | a chemical identifier is missing, or the rendering is no longer the extraction |
| 3 | `check_scope.py` | **the scope gate** · does this folder hold the standard the sheet was compiled to? Reads the sheet's own declaration | the sheet declares a third regime — GB/T, JIS, GOST, SOR/2015-17 — and not the configured one. Exit 2: the verdict is CANNOT VERIFY, out of scope, and **no further stage runs** |
| 4 | *the audit itself* | `rules.md` Stages 2–6 — a person or a model, not a script | — |
| 5 | `verify_citations.py` | **Gate 2** · read the finished report and check every quoted provision against the file it names | the report and the standard disagree |
| 6 | `validate_report.py` | **Gate 3** · verdict shape, finding class, declared blind spots, the ban on permission language, and that a report which performed checks says what passed | any of those, in English or Russian |

The scope gate is third in the order and first in consequence: it is the only script here that can
end a run before it begins. It exists because on 2026-09-11 a sheet compiled to GB/T 16483 was
audited against Annex II from beginning to end and filed with eleven findings — accurate readings,
all of them, of a document that had never been written to that standard. `README.md` § *An incident,
and the gate it produced* has the whole story; `audits/2026-09-11-nye-ts2024-china/` is the retracted
run and the folder beside it is the same sheet done correctly.

Gate 2 is the one that matters most and is the easiest to get wrong. It reads the **report**. A
checker that only re-reads the standard proves the standard has not moved; it would pass a report
whose findings had drifted away from the text they cite.

It is also the only script here that opens a file nobody named on the command line. The path in a
finding — `reference/eu-2020-878/regulation-2020-878.md` — is relative to **this folder**, not to
whoever ran the gate, so the gate resolves it from its own location. Two things follow: the answer
does not change with your working directory, and a report kept outside the repository is checked
against the corpus that ships here. `--reference` still redirects the corpus, and being a path you
typed it is resolved against your working directory. If it names nothing, the gate says so once and
exits 1 rather than reporting every citation in the report as missing.

Which is why Gate 0 is separate from it and called by it. Reading the report is the right question,
but it is asked against a file on disk, and a file on disk is only the standard while nobody has
edited it. Gate 2 rehashes the corpus first — about 5 ms against its own 130 — and fails with the
corpus's diagnosis rather than the report's when the two claims come apart. Gate 0 is also the only
script here that can be run with no arguments at all: it is a statement about the folder, not about
a run.

## Run after editing the documentation

| Script | Job |
| --- | --- |
| `test_docs_example.py` | lift the worked finding out of `rules.md` and put it through Gates 2 and 3. The file that teaches the citation format must not teach a format the gates reject |

## Run only when there is a network

| Script | Job |
| --- | --- |
| `check_freshness.py` | ask the publishers what exists now, write `reference/FRESHNESS-LOG.md`. Never edits the ledger — promoting a published revision to *in force* is a legal reading and belongs to a person |
| `build_reference.py` | re-download the three standards and regenerate everything under `reference/`, with SHA-256 provenance for source and output. It writes the hashes; `verify_reference.py` is what reads them, and offline it can only read the output half — the publisher's bytes are not shipped |

An audit never calls either one. That is why the folder works with no connection, and why it still
knows how old its own knowledge is.

## Conventions

- Every script exits non-zero when it fails, so they chain in a shell without reading the prose.
- Every script carries its method **and its limits** in its own docstring. `extract.py` states the
  thing its fidelity check cannot prove; read it before quoting the check at anyone.
- `.cache/` holds the downloaded publisher markup. It is gitignored: large, reproducible, and not
  ours. What ships is the generated text under `reference/`, with its hashes.
