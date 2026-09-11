# tools/ — what runs, and when

Six scripts, three jobs. Nothing here decides anything about a sheet: the audit is the reading, and
these are the machinery around it — one that prepares the sheet, three that guard the answer, two
that keep the standards current.

## Run for every audit, in this order

| Order | Script | Job | Fails the run when |
| --- | --- | --- | --- |
| 1 | `extract.py` | turn the PDF into the line-anchored rendering the auditor reads, and write the evidence that nothing was lost | never — it reports, it does not gate |
| 2 | `verify_conversion.py` | **Gate 1** · re-derive that evidence from the PDF and the rendering on disk, rather than trusting the JSON | a chemical identifier is missing, or the rendering is no longer the extraction |
| 3 | *the audit itself* | `rules.md` Stages 2–6 — a person or a model, not a script | — |
| 4 | `verify_citations.py` | **Gate 2** · read the finished report and check every quoted provision against the file it names | the report and the standard disagree |
| 5 | `validate_report.py` | **Gate 3** · verdict shape, finding class, declared blind spots, and the ban on permission language | any of those, in English or Russian |

Gate 2 is the one that matters most and is the easiest to get wrong. It reads the **report**. A
checker that only re-reads the standard proves the standard has not moved; it would pass a report
whose findings had drifted away from the text they cite.

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
