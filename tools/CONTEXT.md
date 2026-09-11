# tools/ — what runs, and when

Twelve scripts. Nothing here decides anything about a sheet — the audit is the reading — with one
exception, and it is the exception that ends runs: the scope gate decides whether this folder holds
a rulebook for the sheet at all. Around that: one script prepares the sheet, one does arithmetic
for the auditor inside a stage, four guard the answer, two hold the documentation to what the
folder actually is, two keep the standards current, and one reads the settings the rest stand on.

## Run for every audit, in this order

| Order | Script | Job | Fails the run when |
| --- | --- | --- | --- |
| 0 | `verify_reference.py` | **Gate 0** · rehash every generated file under `reference/` against the SHA-256 recorded in its `PROVENANCE.md` | a shipped standard has changed, is missing, or an unrecorded file has appeared in a generated folder. Gate 2 runs this itself before checking a single citation, so it needs no place in the audit's own sequence — run it alone to ask about the corpus rather than about a report |
| 1 | `extract.py` | turn the PDF into the line-anchored rendering the auditor reads, and write the evidence that nothing was lost | never on what it found — it reports, it does not gate, and it exits 0 on PASS, REVIEW, UNCONFIRMED and NO TEXT LAYER alike. It exits non-zero only when it could not produce the two files at all: no such file, or the primary engine itself failed |
| 2 | `verify_conversion.py` | **Gate 1** · re-derive that evidence from the PDF and the rendering on disk, rather than trusting the JSON — by calling `extract.compare()`, so there is one comparison and not two that can drift apart | the PDF has no extractable text layer at all (`NO TEXT LAYER`); a chemical identifier is missing, or the rendering is no longer the extraction (`FAIL`); the independent engine could not run, so completeness was never checked (`UNCONFIRMED`). A distinct character or token the independent engine found and the rendering lacks is `REVIEW`: through without `--strict`, stopped with it |
| 3 | `check_scope.py` | **the scope gate** · does this folder hold the standard the sheet was compiled to? Reads the sheet's own declaration | the sheet declares a third regime — GB/T, JIS, GOST, SOR/2015-17 — and **neither** of the two standards this folder ships. Exit 2: the verdict is CANNOT VERIFY, out of scope, and **no further stage runs**. A sheet naming 29 CFR 1910.1200 *and* WHMIS has named a rulebook that is here, so it is not stopped — the EU↔US crossing is a finding at Stage 3 |
| 4 | *the audit itself* | `rules.md` Stages 2–6 — a person or a model, not a script | — |
| 5 | `verify_citations.py` | **Gate 2** · read the finished report and check every quoted provision against the file it names, **and that the provision belongs to the corpus the report's own regime may cite** | the report and the standard disagree, in a quoted string of any length; a citation reaches outside the regime's corpus — CLP Annex VI or Annex II in a US report, 1910.1200 in an EU one; the report names no regime at all; a finding heading carries no class marker; one of the five required parts is a label with nothing written under it |
| 6 | `validate_report.py` | **Gate 3** · verdict shape **against the report's own findings**, the class every finding tag declares, **the regime named in the header**, the declarations under *Declared blind spots*, the ban on permission language, and that a report which performed checks says what passed | any of those, in English or Russian; a verdict that contradicts what the report lists — CONFORMS carrying findings, CANNOT VERIFY carrying findings; a finding tag that declares neither class, which is a block nothing checks; a blind-spots heading with nothing under it; quotation marks that do not pair, because quotation is the only thing that exempts a phrase from the ban; also a header that declares one regime and applies the other regime's standard, and a US run that does not record Section 3 as *not assessed for classification correctness* |

The scope gate is third in the order and first in consequence: it is the only script here that can
end a run before it begins. It exists because on 2026-09-11 a sheet compiled to GB/T 16483 was
audited against Annex II from beginning to end and filed with eleven findings — accurate readings,
all of them, of a document that had never been written to that standard. `README.md` § *An incident,
and the gate it produced* has the whole story; `audits/2026-09-11-nye-ts2024-china/` is the retracted
run and the folder beside it is the same sheet done correctly.

Gate 2 is the one that matters most and is the easiest to get wrong. It reads the **report**. A
checker that only re-reads the standard proves the standard has not moved; it would pass a report
whose findings had drifted away from the text they cite.

It is also one of two scripts here that open a file nobody named on the command line. The path in a
finding — `reference/eu-2020-878/regulation-2020-878.md` — is relative to **this folder**, not to
whoever ran the gate, so the gate resolves it from its own location. Two things follow: the answer
does not change with your working directory, and a report kept outside the repository is checked
against the corpus that ships here. `--reference` still redirects the corpus, and being a path you
typed it is resolved against your working directory. If it names nothing, the gate says so once and
exits 1 rather than reporting every citation in the report as missing.

The scope gate is the other one, and it now uses the same idiom for the same reason:
`config/jurisdiction.md` is *this installation's* setting, so it is found from the script rather
than from the caller. Resolved the caller's way it made the gate answer "jurisdiction not
configured" — a real stop condition, in the words of one — from every directory but the root, about
a sheet it had not opened. `--config` still redirects, and being a path you typed it is resolved
against your working directory.

## What Gate 2 counts as present

Two of its checks are about a finding being *there* rather than being *right*, and both were once
enforced one step short of what they claim.

A finding is recognised by its tag **and** its class marker together — `### [F-03] [STANDARD] …` —
because a bare tag at the head of a list item is a cross-reference, not a new finding. The cost of
that is that a heading which simply omits the marker is invisible: no RULE read, no provision
looked for, no revision, no date, and the same counts out of the gate as if the block did not
exist. So the tags are scanned a second time on their own, and any tag heading a line without a
marker behind it fails before any other check runs.

"The five required parts are present" means their bodies are, not their labels. A part whose
heading is followed by nothing is a missing part and is failed as one, and a part ends at the next
part, the next heading, or a horizontal rule — otherwise the last part of a finding is bounded only
by the next finding and takes the section break below it for a body.

Which is why Gate 0 is separate from it and called by it. Reading the report is the right question,
but it is asked against a file on disk, and a file on disk is only the standard while nobody has
edited it. Gate 2 rehashes the corpus first — about 5 ms against its own 130 — and fails with the
corpus's diagnosis rather than the report's when the two claims come apart. Gate 0 is also the only
script here that can be run with no arguments at all: it is a statement about the folder, not about
a run.

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

## What exempts a phrase from Gate 3, and what does not

One thing: quotation marks. A finding has to be able to reproduce a Section 7 that reads
"safe to use" without being accused of having said it, so quoted spans are blanked before the ban
scan and everything outside them is the auditor speaking. Nothing else exempts anything — not
indentation, not a table row, not a blockquote, not the word "quote", and not a disclaimer
sentence. Each of those was tried here and each was a way of saying the banned thing and being
told the report may be delivered; the summary table, which is the first thing a reader sees, was
exempt as a table for as long as the table exemption existed.

Two consequences worth knowing before you write a report.

- **The marks have to pair.** A report with an odd number of `"` is refused without being scanned
  for anything else. Pairing runs left to right, so one unclosed mark — an inch sign, a citation
  cut in half — re-pairs every mark after it: the spans that get blanked become the auditor's own
  prose and the real quotations are handed to the scan. Measured on a shipped report with one mark
  added to its header table, half the report changed sides. Write an inch mark as `in`.
- **The scan reads the report, not its lines.** `rules.md` wraps a finding body at about 95
  columns, so a sentence about the material arrives broken across lines and re-indented. The ban
  patterns treat a space as any run of whitespace and run over the whole text; the line number in
  the failure is recovered from where the match starts.

## Run inside the audit, at Stage 2

| Script | Job |
| --- | --- |
| `check_age.py` | find every date the rendering states beside a word claiming to be an issue, revision or superseded-version date, eliminate the readings the document itself rules out, measure the newest governing one against `run_date` and `policy_max_age_years`, and say whether a house-policy finding is owed. `--pdf <sheet.pdf>` is optional and adds one elimination. **It reports; it does not gate** — exit 0 either way, non-zero only when the *rendering* cannot be read. An unreadable or absent PDF is not a failure, it is one fewer signal |

It is the only script that touches the audit's own reasoning, and the line it does not cross is the
one AD-15 draws. The subtraction is mechanical: what a date *means* is not. Two things in this
corpus say why. `03/04/2026` is two dates, and the shipped Carboguard sheet carries a print date one
year after its revision date: the gate runs on the revision, and only the words beside a date are
evidence of which is which.

**What it now does about the first of those.** A supplier writes dates one way and not both, so the
script works on *conventions* — d/m/y and m/d/y, applied to the whole sheet — and runs four signals
in order, each of which can only **remove** a convention and can never supply a date:

1. **Shape.** `30.08.2024` and `16/04/2019` have one reading each. A month written as a word or an
   ISO date has one reading too, and neither says anything about how the sheet writes its *numeric*
   dates, so neither is allowed to settle one.
2. **The sheet's own convention.** One governing date that shape reads only one way fixes the
   convention for every ambiguous date on the sheet. Only a *governing* date may do it, which is
   narrower than the premise needs — a print date is typeset by the same generator — and two corpus
   sheets turn on that width. Both stay undecided rather than be settled by a date the gate is not
   about, and the unused evidence is printed by name so the choice is visible.
3. **The order the sheet itself states.** A superseded or replaced version is older than the
   revision that superseded it, and an issue date falls on or before its revision. Annex II
   provision 0.2.5 requires a revised sheet to indicate which version it replaces and names a
   *supersedes date* as one of the three ways, so for an EU sheet this is what the required field
   means, not a guess about how suppliers write.
4. **The file's own timestamp, as an upper bound** — only with `--pdf`. A sheet cannot state a date
   later than the last time its own file was written. **Never as a value:** LOCTITE 270's `/ModDate`
   is the printing date on its own first page, four months after the revision it states. Absent,
   stripped or unreadable metadata means no constraint and never a guessed date; three corpus sheets
   are already in that position, one of them because it is encrypted.

Every elimination is printed with the signal that made it and the line it rests on, because a
resolved ambiguity that reads as certainty is the failure this whole folder is written against.
Where two readings survive, both are printed and the script says the document does not settle it.
That residue is the answer. The regime prior — EU d/m/y, US m/d/y — only orders what is printed and
never removes anything: JET-LUBE is a GB-market sheet written m/d/y, because its supplier is
American.

**What it still cannot prove.** That the words beside a date meant what they say. That a surviving
reading is the one the supplier intended — it survived because the others were ruled out, which is
a weaker claim and is the one printed. And the bound is only as good as the file: the corpus holds
a sheet, CRC ECO Leak Finder, whose stated dates are *later* than its own `/ModDate` and whose
stated issue date falls *after* its stated revision date. So no signal is allowed to remove the last
surviving reading: when one contradicts everything left, the contradiction is printed and nothing is
eliminated. On the 22 corpus sheets this leaves two sheets whose date is genuinely unsettled, and
neither changes a verdict.

It also prints what it could not read. A line that claims a date and yields none is listed as such,
because `rules.md` Stage 2 turns *no date found* into CANNOT VERIFY — a verdict, and too much
weight for a regex to carry quietly. That guard earned itself twice: the first version read only
digits and answered NO DATE FOUND on the sheet that dates itself `Issue date June-30-2025`, and the
second had `revision date` but not a bare `Revision:` — the form 0.2.5 *prescribes* — and so
answered NO DATE FOUND on LOCTITE 270, a sheet that complies with it. The sheet was right and the
reader was wrong, which is the worst direction for this kind of error to run. That list of unparsed
claims should stay printed forever: the next corpus will state a date in a form this one does not.

## The settings, and the one script that reads them

| Script | Job |
| --- | --- |
| `read_config.py` | parse `config/jurisdiction.md` — jurisdiction, organisation, `policy_max_age_years`, `run_date` — say what each resolves to, and fail by name on one that cannot be honoured as written: a regime Salus does not ship, a threshold that is not a number, a run date that is not ISO or is in the future. Run it after filling the file in |

It is the **only** place that knows how that file is read. `check_scope.py` imports it for the
regime and `validate_report.py` for the age policy, because until 2026-09-11 the scope gate carried
its own parser and two of the four settings were read by nothing at all — honoured because
`rules.md` says to honour them, which is a rule and not a guard. AD-15: where two scripts must know
the same thing, there is one implementation.

What it cannot do is tell you the setting is *right*. `jurisdiction: US` parses perfectly in an
installation that audits for a German legal entity; only the person filling the file in knows.
`config/CONTEXT.md` is the argument for why that is a person's job.

Gate 3 meets the same settings from the other end. It reads the run date and the age threshold out
of the **report**, never out of this file — a filed report keeps what it was made under — and
prints a NOTE, not a failure, when the two have parted company.

## Run after editing the documentation

| Script | Job |
| --- | --- |
| `test_docs_example.py` | lift the worked finding out of `rules.md` and put it through Gates 2 and 3. The file that teaches the citation format must not teach a format the gates reject |
| `check_docs.py` | hold the documents to this folder. The two diagrams in `README.md`: every node connected, every decision drawn with its outcomes, every script named real. The four places that state the sequence of checks — the flowchart, `README.md` § *The gates, one at a time*, `rules.md` § *Before the report leaves*, and the table above — saying the same thing. And every revision id named anywhere here against `reference/*/PROVENANCE.md`, which is generated output and hashed by Gate 0, so that fact has an owner nobody can edit quietly. It does not decide which statement is right; it refuses to let them disagree. `--render` also draws the diagrams, when mermaid-cli happens to be installed. It was `check_diagrams.py` until the revision check arrived |

## Run only when there is a network

| Script | Job |
| --- | --- |
| `check_freshness.py` | ask the publishers what exists now, write `reference/FRESHNESS-LOG.md`. Never edits the ledger — promoting a published revision to *in force* is a legal reading and belongs to a person. Exits 1 when any target could not be reached, and writes UNREACHABLE rather than a result: a probe that got no answer is not a confirmation that nothing has changed, and that line is one `rules.md` Stage 3 has a report cite |
| `build_reference.py` | re-download the standards and regenerate everything under `reference/`, with SHA-256 provenance for source and output. It writes the hashes; `verify_reference.py` is what reads them, and offline it can only read the output half — the publisher's bytes are not shipped. `--only osha` (or `eu878`, `clp`) rebuilds one standard and leaves the others' bytes and hashes untouched, so a fix to one converter does not put an unexplained diff on the other two |

An audit never calls either one. That is why the folder works with no connection, and why it still
knows how old its own knowledge is.

## Conventions

- Every script exits non-zero when it fails, so they chain in a shell without reading the prose.
  **What counts as failure depends on whether the script is a gate.** A gate fails on what it found
  in the sheet or the report — that is what it is for. A reporter fails only when it could not
  produce its output at all, and `extract.py` is the only reporter in the sequence. Reading a
  verdict off a reporter's exit code is how a shell chain built on this table came to die at step 1
  on the nine corpus sheets that return REVIEW, while Gate 1 let the same nine through: two scripts
  each deciding, and disagreeing. One decides now.
- Every script carries its method **and its limits** in its own docstring. `extract.py` states the
  thing its fidelity check cannot prove; read it before quoting the check at anyone.
- `.cache/` holds the downloaded publisher markup. It is gitignored: large, reproducible, and not
  ours. What ships is the generated text under `reference/`, with its hashes.
