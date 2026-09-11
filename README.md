# Salus — an auditor for safety data sheets

Salus reads one safety data sheet and tells you where it meets the standard that governs how such
a sheet must be written, and where it does not — naming the exact provision behind every finding,
in a file you can open and read for yourself.

It is a folder. Drop it into a Claude project, point any AI tool at it, or run its scripts from a
terminal. Nothing is installed and nothing phones home. Those three are not the same auditor,
though: the gates that guard a report are scripts, and a Claude project has no shell to run them
in. *Where it runs, and what each surface costs you*, below, says exactly what that costs.

**It audits the document. It never tells you anything about the material.** A perfectly compliant
sheet can describe a substance that will kill someone; a defective sheet can describe table salt.
Salus judges the paperwork and stops there.

---

## What you get

Three verdicts, and no fourth:

| Verdict | Means |
| --- | --- |
| **CONFORMS** | the sheet met the standard on every point checked, and the report lists those points |
| **DOES NOT CONFORM** | the sheet failed, and the report lists each failure with the provision it breaks |
| **CANNOT VERIFY** | the sheet could not be read, **or** it was compiled to a standard this folder does not ship — this is **not** a failure, and no provision was applied |

Every finding looks like this. Five parts, all of them required:

```md
[F-02] [STANDARD] BLOCKING — Section 3 departs from a harmonised classification
  WHAT   Section 3 lists CAS 64742-52-5 at >=25 - <=50 %, classified "Asp. Tox. 1, H304".
  WHERE  page 2, lines 110-114 of the sheet
  RULE   CLP Annex VI Table 3 row 649-465-00-7 reads "Carc. 1B | H350 | GHS08 Dgr | H350 | | | L".
         Note L: "The harmonised classification as a carcinogen applies unless it can be shown
         that the substance contains less than 3 % of dimethyl sulphoxide extract ..."
  WHERE IN THE STANDARD
         reference/eu-clp-annex-vi/annex-vi-table-3-extract.md, row 649-465-00-7
         revision: 02008R1272-20260701
         confirmed current: 2026-09-11
  WHY    The sheet neither carries the harmonised classification nor states that the Note L
         condition was met, so a reader cannot tell whether the departure is lawful.
```

`WHERE IN THE STANDARD` is three things, not one: **the provision**, **the revision it belongs
to**, and **the date that revision was last confirmed current**. A report you read six months from
now still tells you what the auditor knew when it wrote it.

Findings come in two kinds and never look alike. A `[STANDARD]` finding always cites a provision.
A `[HOUSE POLICY — no provision]` finding — the five-year age gate is the only one — says in
writing that no law requires it.

## What you do not get

- **No opinion on the material.** Not whether it is safe, not whether anyone may use it, not what
  to store it in or substitute it with. Ask Salus to approve a material and it will not, however
  the question is phrased; `tools/validate_report.py` voids any report containing such language.
- **No detection of what a supplier left out.** Salus audits what is written. It cannot see an
  omitted ingredient and says so in every report.
- **No chemistry.** It does not re-measure a flash point or decide whether a stated value is true.
  It checks whether the sheet agrees with itself and with the standard.
- **No legal opinion, and no clearance.** CONFORMS covers the points listed, on one date. What
  happens to the sheet next belongs to the specialists it goes to.
- **No third-regime audits.** Salus holds EU 2020/878 and US 29 CFR 1910.1200 and nothing else. A
  sheet compiled to GB/T 16483, JIS Z 7253, GOST 30333 or SOR/2015-17 stops at the scope gate with
  CANNOT VERIFY. It is not audited against the configured standard and scored against obligations
  it was never written to — see *An incident, and the gate it produced* below.
- **No OCR.** A scanned sheet gets CANNOT VERIFY rather than a guess.

## Where it runs, and what each surface costs you

The audit is a reading, and a reading works anywhere. The machinery that *checks* the reading is a
handful of Python scripts, and those need a shell. Naming what their absence costs is the same
discipline as the blind spots above: an auditor that says where it is weaker is worth more than one
that implies it is equally strong everywhere.

| | Terminal, or an agent with a shell | Claude project, or any AI tool without one |
| --- | --- | --- |
| The standards in `reference/`, opened at the provision | yes | yes |
| The seven stages, the finding format, the severity ladder | yes | yes |
| Line-anchored rendering and its fidelity evidence (`extract.py`) | yes | **no** — you supply the text, and nothing proves what it lost |
| **Gate 1** — conversion fidelity, two independent engines | yes | **no** |
| **The scope gate** — is the sheet's own standard one this folder holds | yes | **no** — `rules.md` Stage 1b still says to stop, but nothing enforces it, and this is the check whose absence filed a retracted run |
| **Gate 2** — every citation checked against the file it names | yes | **no** |
| **Gate 3** — verdict shape, and the ban on saying anything about the material | yes | **no** — the boundary is prose, and prose is not enforcement |

In a Claude project you get the auditor's judgement without the machinery built to distrust it.
That is a reduction, not a smaller edition. `tools/CONTEXT.md` argues that catching a breach after
the fact is the second-best outcome; on this surface there is no after the fact at all.

**What to do about it.** Audit where it is convenient, gate where it is possible. A report written
in a Claude project is just a text file — bring it to a terminal, run Gates 2 and 3 over it, and it
is guarded exactly as if it had been written there:

    python3 tools/verify_citations.py <report.md>
    python3 tools/validate_report.py  <report.md>

The scope gate is recoverable in the other direction: it reads the sheet, not the report, so it can
be run before or after the fact on any rendering — and where no shell is available, `rules.md`
Stage 1b is the instruction to perform it by eye. Read the sheet's first page and Section 15 for a
declaration of the standard it was compiled to, and if that standard is not in `reference/`, stop.

Gate 1 is the one that cannot be recovered afterwards, because it is a claim about a conversion
that already happened somewhere else. Where no shell ran `extract.py`, the report should say so:
the rendering was not verified, and that is a fact about the audit worth writing down.

## Quick start

**Requirements.** Python 3, `pdftotext` from poppler, and `pypdf`. All three are required, not
optional: Gate 1's entire claim is that two *independent* engines agree, so without pypdf there is
no check, only an assertion. Add `cryptography` as well — at least one sheet in the shipped corpus
is AES-encrypted and pypdf cannot open it without that package.

    pip install pypdf cryptography

```bash
# 1. say which regime you audit under — this is never guessed
$EDITOR config/jurisdiction.md          # set jurisdiction: EU   (or US)

# 2. convert the sheet, and produce the evidence the conversion lost nothing
python3 tools/extract.py "test-cases/sds/BG - HCF MSDS 510231_UK_EN.pdf" --outdir audits/my-run

# 3. check the conversion before trusting it
python3 tools/verify_conversion.py "test-cases/sds/BG - HCF MSDS 510231_UK_EN.pdf" \
        --outdir audits/my-run

# 3b. is there a rulebook here for this sheet at all? exit 2 means stop, do not audit
python3 tools/check_scope.py "audits/my-run/BG - HCF MSDS 510231_UK_EN.salus.md"

# 4. audit: hand rules.md and the rendering to your AI tool, or follow rules.md yourself.
#    Write the result to audits/my-run/report.md

# 5. the two gates that guard the report
python3 tools/verify_citations.py audits/my-run/report.md
python3 tools/validate_report.py  audits/my-run/report.md
```

Eight finished runs are already in `audits/` — both jurisdictions, all three verdicts — with the
renderings and fidelity reports they used. `examples.md` walks through five of them in detail.

Optional, when there is a network:

```bash
python3 tools/check_freshness.py        # is the copy of each standard still the one in force?
python3 tools/build_reference.py        # re-download the standards and regenerate reference/
```

## If you are here to judge it

Everything below can be checked without trusting a word of this file. Items 2 to 4 run scripts, so
they need a terminal; if you are reading this inside a Claude project, see *Where it runs* above.

1. **Open any finding and follow its citation.** `examples.md` → a finding → the file named in
   `WHERE IN THE STANDARD` → the provision, as text, in `reference/`. Not a link, not a summary.
   Five of the seven filed runs are walked there: three EU, one US, and one that could not be
   read at all.
2. **Make the checker disagree with the report.** See *Claims written to be falsified* below: tamper
   with one character of a quoted provision and watch `verify_citations.py` fail by name.
3. **Try to make it approve a material.** Append `This material is safe to use.` to a report and run
   `validate_report.py`. The run is voided.
4. **Check the standards are current.** `python3 tools/check_freshness.py`. It found three CLP
   consolidations newer than the one this folder first shipped, and the reference layer was rebuilt
   before submission. The episode is recorded in `reference/STANDARDS-LEDGER.md`.

---

## How it works

One sheet in, one verdict out. Two things can end a run before it starts — an unreadable sheet and
a sheet written to a standard that is not here — and nothing reaches a reader until three gates pass.

```mermaid
flowchart TD
    SDS["SDS PDF"] --> S0["Stage 0 · settings"]
    S0 -->|not configured| CV["CANNOT VERIFY"]
    S0 -->|EU or US| S1["Stage 1 · convert"]
    S1 --> G1{"Gate 1 · fidelity"}
    G1 -->|no text layer| CV
    G1 -->|identifier lost| VOID["VOID · not delivered"]
    G1 -->|ok| SC{"Stage 1b · scope gate"}
    SC -->|"declares GB/T, JIS, GOST…"| CV
    SC -->|EU or US, or nothing declared| S2["Stage 2 · age gate"]
    S2 --> S3["Stage 3 · revision"]
    S3 --> S4["Stage 4 · structure"]
    S4 --> S5["Stage 5 · classification"]
    S5 --> S6["Stage 6 · consistency"]
    S6 --> REP["report.md"]
    REP --> G2{"Gate 2 · citations"}
    G2 -->|quote not found| VOID
    G2 --> G3{"Gate 3 · boundaries"}
    G3 -->|permission language| VOID
    G3 -->|no findings| OK["CONFORMS"]
    G3 -->|findings| NO["DOES NOT CONFORM"]

    classDef v fill:#0b3d2e,stroke:#7fd1ae,color:#eafff5
    classDef b fill:#4a1420,stroke:#ff9db0,color:#ffe9ee
    classDef g fill:#12314f,stroke:#7fb6f0,color:#eaf4ff
    class OK,NO,CV v
    class VOID b
    class G1,G2,G3 g
```

**What each stage does, and what it reads.** Stages never read a reference file through — they
open it at the provision they are about to cite. That is what keeps a run at a few thousand tokens.

| Stage | Question it answers | Reads |
| --- | --- | --- |
| 0 · settings | EU or US? | `config/jurisdiction.md` |
| 1 · convert | can this sheet be read at all? | the PDF, twice, with two engines |
| 2 · age gate | older than the house limit? | the sheet's issue date — **no provision, house policy** |
| 3 · revision | which revision applies today? | `STANDARDS-LEDGER.md`, `FRESHNESS-LOG.md` |
| 4 · structure | all 16 sections, numbered, populated? | 2020/878 Annex II, or 1910.1200 (g) |
| 5 · classification | does Section 3 match the harmonised entry? | CLP Annex VI — **one row per CAS or Index** |
| 6 · consistency | does the sheet contradict itself? | 2020/878 Annex II, section by section |

**Where the standards come from, and how they stay current.** The two maintenance scripts are the
only parts that need a network. An audit never calls them, which is why the folder works offline —
and why it still knows how old its own knowledge is.

```mermaid
flowchart LR
    B["build_reference.py"] --> EU["EU 2020/878"]
    B --> US["29 CFR 1910.1200"]
    B --> CLP["CLP Annex VI"]
    F["check_freshness.py"] --> LOG["FRESHNESS-LOG.md"]
    F -.->|reports drift, never edits| LED["STANDARDS-LEDGER.md"]
    EU --> A["the audit"]
    US --> A
    CLP --> A
    LED --> A
    LOG --> A

    classDef s fill:#3a2f12,stroke:#e0c268,color:#fff6df
    class EU,US,CLP,LED,LOG s
```

---

## The test corpus

`test-cases/sds/` holds **22 real manufacturer safety data sheets** — Chesterton, Loctite, Jotun,
Carboline, Castrol, Devcon, Dowsil, CRC, Weicon, Jet-Lube, Atlas Copco, Chevron, BG, Nye Lubricants,
RD Coatings —
in both EU and US formats, some of them declaring superseded revisions, one of them naming an
Israeli REACH variant. They are what Salus was built against and what every claim here was tested
on. They are not decoration: the rows in `reference/eu-clp-annex-vi/` are selected by the
identifiers these sheets actually cite.

`test-cases/sds-constructed/` holds two files that are **not** sheets as a supplier issued them: a real sheet rasterised
into an image, so the CANNOT VERIFY path has a fixture instead of a description; and a real,
current sheet cut down to its first four pages of twenty, which tests the line between *unreadable*
and *incomplete* — those are different verdicts and only one of them is a failure. The folder's own
README records exactly how each was made, so neither is mistaken for a supplier's document.

## The standards, and the calendar

| | |
| --- | --- |
| EU | Commission Regulation (EU) 2020/878 — full text in `reference/eu-2020-878/` |
| US | 29 CFR 1910.1200 — full text, appendices included, in `reference/us-osha-hcs/` |
| Classification | CLP Annex VI Part 1 Notes, and the Table 3 rows for every identifier in the corpus, in `reference/eu-clp-annex-vi/` |

A standard is not a version number. It is three dates: published, applies from, and the end of the
window in which the previous revision may still lawfully be used. `reference/STANDARDS-LEDGER.md`
carries all three for each standard, quoted from the standards' own text, because a sheet on an
older revision **inside a live window is compliant** and calling that a failure would be a false
finding. US mixtures are in such a window right now: § 1910.1200(j)(3)(i) does not close it until
2027-11-19.

Salus runs with no network. That is not the same as running blind: `tools/check_freshness.py`,
run whenever there is a connection, writes what the publishers currently offer into
`reference/FRESHNESS-LOG.md` with a date, and every finding carries the date its revision was last
confirmed current. A report read six months from now still says what the auditor knew when it was
written.

## The scope gate

    python3 tools/check_scope.py <run>/<sheet>.salus.md      # exit 2 = out of scope, stop

It runs once, after the conversion gate and before the audit, and it answers one question: does
this folder hold the rulebook this sheet was written to? It reads the sheet's own declaration —
suppliers put it on the first line, in the header, or in Section 15 — and compares it with what is
in `reference/`.

| What the sheet declares | What happens |
| --- | --- |
| the configured standard | the audit runs |
| the *other* standard shipped here (a US sheet under `jurisdiction: EU`, or the reverse) | the audit runs, and Stage 3 reports the mismatch as a finding — both rulebooks are here, so the comparison rests on text |
| a third regime **and** the configured standard — a sheet written for two markets | the audit runs against the configured one; the third declaration is not a finding |
| a third regime and nothing else | **stop.** CANNOT VERIFY, out of scope, no findings |
| nothing at all | the audit runs; Stage 3 infers the revision from the issue date and says it inferred it |

It fires on declarations only — never on a country name, an address, a language, an emergency
number or an inventory list. Two sheets in the corpus mention Canada's WHMIS and both are audited
normally, because both also declare REACH. Across all twenty-four shipped sheets it stops exactly
one.

## The three gates

No report is produced until all three pass. They are scripts, so they do not depend on the
auditor's own account of how the audit went.

    python3 tools/verify_conversion.py "<sheet>.pdf" --outdir <run>   # is the rendering faithful
    python3 tools/verify_citations.py  <run>/report.md                # do the citations hold
    python3 tools/validate_report.py   <run>/report.md                # verdict shape and boundaries

**Gate 1** extracts the sheet with two independent engines — poppler and pypdf — and asserts that
nothing the second one found is missing from what the first one shipped: every distinct character,
every word and number token, every chemical identifier and hazard code. It also proves the shipped
Markdown *is* the extraction, by SHA-256, rather than a cleaned-up version of it. It is not a
rubber stamp: across the twenty-two real sheets it returns PASS on twelve, REVIEW on nine, and
UNCONFIRMED on one — a sheet encrypted with AES, which the second engine cannot open without the
`cryptography` package, so its completeness is simply not checked and the report says so. And
`extract.py` states in its own docstring the thing it cannot prove — two engines missing the same
content agree and are wrong together, which is why per-page text density is reported separately.

**Gate 2 reads the report, not just the reference folder.** It pulls every quoted provision out of
every finding and looks for that text in the file the finding names. A checker that only re-reads
the standard proves the standard has not changed; it would happily pass a report whose findings had
drifted away from the text they cite. This one fails when the report and the standard disagree.

It also enforces the **corpus rule**: an EU run may cite Annex II and CLP Annex VI, a US run may cite
29 CFR 1910.1200 and nothing else, because OSHA publishes no harmonised classification list and none
is shipped for it. A finding standing on Annex VI in a US report stands on a regulation that does not
govern the sheet. The regime comes from the report's own header row, not from `config/jurisdiction.md`
— a filed report keeps the regime it was made under, and `audits/` holds both regimes, checked
together, against one setting that can say only one thing. A disagreement with the setting is printed
as a note; a report that names no regime at all fails.

There is a fourth check, smaller and aimed at this repository rather than at a sheet:
`tools/test_docs_example.py` lifts the worked finding out of `rules.md` and runs the two report
gates over it, so the file that teaches the citation format cannot drift into teaching one the
gates reject.

**Gate 3** checks the verdict shape, that every finding declares whether it rests on a provision or
on house policy, that the header names a regime and applies that regime's standard, that blind spots
are stated, and that no permission language survived. On a US run it also requires the report to
record Section 3 as *not assessed for classification correctness* — the sentence that keeps a US
report from reading as though the classification had been checked and held.

## An incident, and the gate it produced

On 2026-09-11 a sheet was audited here that should never have been audited at all, and the folder
had nothing in it that could say so.

`SDS_CHINA_English_TS+2024.pdf` is a real supplier sheet — Nye Lubricants, a FUCHS Group company —
for the Chinese market. Its first line reads *"Prepared in accordance with GB/T 16483 and GB/T
17519"*, and its Section 15 lists the Chinese laws it conforms to. It declares neither EU 2020/878
nor US 29 CFR 1910.1200. The run was made under `jurisdiction: EU`, so it was compared with Annex II
from beginning to end, and it was filed as **DOES NOT CONFORM with eleven findings**.

Every one of those findings was accurate as a reading of the text. All three gates passed on it. It
was still wrong, and wrong in the way that matters most for a compliance tool: the eleven findings
are not eleven defects, they are **one observation — the wrong ruler was used — restated once per
provision**. A reader cannot tell that list apart from a list of real defects, and the document is
not defective. It is a competent sheet written to a standard this folder does not hold.

Nothing in the folder caught it. `config/jurisdiction.md` explicitly *instructed* the behaviour: it
said a sheet compiled for another regime is audited against the configured one and the mismatch
reported as a finding. That rule was written with the EU↔US crossing in mind, where both rulebooks
ship and the comparison means something. Extended to a third regime it produces a confident
verdict with nothing underneath it.

**What changed, the same day:**

| | |
| --- | --- |
| `tools/check_scope.py` | new. The scope gate, above. Exits 2 on this sheet, naming both declarations and the line each sits on |
| `rules.md` Stage 1b | the stop condition, in the contract the auditor actually follows |
| `identity.md` | the two standards are stated as *scope*, and CANNOT VERIFY now covers "no rulebook here for this", not only "cannot read this" |
| `config/jurisdiction.md` | the rule that caused it is corrected, and the difference between the EU↔US crossing and a third regime is spelled out |
| `audits/2026-09-11-nye-ts2024-china/` | **retracted**, kept in place, with a notice at its head saying what it was and what it should have been |
| `audits/2026-09-11-nye-ts2024-china-scope-stop/` | the run as it should have gone: the stop, no findings, and an explicit statement that Salus makes no judgement about the sheet in its own regime |

The bad run is kept rather than deleted. An auditor that quietly removes the evidence of its own
bad run has disqualified itself from asking anyone else not to.

## Claims written to be falsified

Seven claims, each with the command that breaks it. If any of them does not behave as described,
the tool is wrong and the claim should be disbelieved. Three of the five are stated in two parts —
what the gate does now, and what it did before an architecture review broke it. A tool that reports
only the defects it never had is not being audited.

1. **"Every citation is checkable, and the checker reads the report."**
   Take a copy of a report, change one character inside a quoted RULE string, and run the gate on
   the copy:

       cp audits/2026-09-11-bg-hcf/report.md /tmp/tampered.md
       python3 -c "p='/tmp/tampered.md'; s=open(p).read(); \
                   open(p,'w').write(s.replace('H350 | GHS08 Dgr','H351 | GHS08 Dgr',1))"
       python3 tools/verify_citations.py /tmp/tampered.md

   It fails by name: `[F-02] quoted text is not in the cited standard`. The untouched report passes
   74 checks. Edit the reference file instead of the report and it fails the same way — which is
   the point: the gate compares the two, and does not trust either alone.

2. **"Salus cannot be talked into approving a material — and the ban does not depend on where the
   words sit."**
   Append `This material is safe to use.` to a copy of any report and run
   `python3 tools/validate_report.py` on it. Two boundary breaches are reported and the run is
   voided. Then run the harder version: put the same sentence *inside* a finding, on an indented
   `WHY` line, which is where an auditor's own prose actually lives. Three breaches, voided there
   too. Only text inside quotation marks is exempt — a finding has to be able to quote a sheet
   whose Section 7 says "safe to use" without being accused of having said it.

   *This is the gate's second implementation.* The first exempted any line indented four or more
   spaces, reasoning that indented lines are quotations — and `rules.md` mandates exactly that
   indentation for every `WHAT`, `WHERE`, `RULE` and `WHY`. Roughly three quarters of every report
   went unscanned, and the appended form above was the one path that still worked. Quotation is
   marked by quotation marks, not by whitespace, and the exemption now sits where quotation is.
   The ban list is in that script, in plain sight, in English and Russian.

3. **"The standards in `reference/` are the ones in force, and the tool knows when it last checked."**
   Run `python3 tools/check_freshness.py` with a connection. It reports each standard against
   `reference/STANDARDS-LEDGER.md` and writes `reference/FRESHNESS-LOG.md`.
   This is not decoration: the first build of this folder shipped the CLP consolidation of
   2025-02-01, and this script found three later ones before submission. The reference layer was
   rebuilt against 2026-07-01. The story is recorded in the ledger.

4. **"A finding cites the standard, not this repository's own prose."**
   `reference/` also carries the folder's own routing, its provenance hashes and its calendar.
   None of those is a provision. Write a finding that quotes `reference/CONTEXT.md` and names it
   under `WHERE IN THE STANDARD`, and Gate 2 refuses it by name: *cites … as a provision. That file
   is this folder's own bookkeeping, not the standard.*

   *Until this was fixed it passed with zero failures.* The gate walked every `.md` under
   `reference/`, so what it actually proved was that a quoted string appeared in some markdown this
   folder ships — a weaker claim than the one it was making.

5. **"Five parts are required of a finding, and five are enforced."**
   Delete every `WHERE` line from a copy of a report — the part that locates the defect in the
   sheet — and Gate 2 fails once per finding.

   *Until this was fixed, it did not.* `^\s*WHERE\b` also matched the heading
   `WHERE IN THE STANDARD`, because the word boundary sits in the space before *IN*. A finding
   carrying only the latter satisfied both, and the five required parts were enforced as four. The
   part that went missing was the one a reader cannot reconstruct from the standard.

6. **"A sheet written to a standard that is not here stops the run, and a report that only lists
   failures does not pass."**
   Two commands, one for each half:

       python3 tools/check_scope.py \
           audits/2026-09-11-nye-ts2024-china-scope-stop/SDS_CHINA_English_TS+2024.salus.md
       echo "exit $?"        # 2 — out of scope, China, GB/T 16483 and GB/T 17519, line 2

   Run it over the rendering of every other run in `audits/` and each exits 0 — the two China
   folders hold the same sheet, and both stop. Then
   take a copy of any report, delete its `[P-n]` blocks, and run Gate 3: it fails, whatever the
   verdict. Replace them with a bare `- [P-01] looked fine` bullet and it fails again — a pass is
   written the way a finding is written or it does not count.

   *Until both were fixed, neither held.* A GB/T sheet was audited against Annex II and filed with
   eleven findings; see *An incident, and the gate it produced*. And passes were demanded only of a
   CONFORMS report, so a DOES NOT CONFORM report listing nothing but failures satisfied the gate —
   the thing this tool is least allowed to be, which is a critique.

7. **"An EU run cites the EU rulebooks and a US run cites OSHA, and nothing enforces that but a
   script."**
   Paste the worked Annex VI finding from `rules.md` into a copy of the one US report and run
   Gate 2 on the copy:

       cp audits/2026-09-11-carboguard-us/report.md /tmp/crossed.md
       python3 -c "f=open('rules.md').read(); \
                   b=f[f.index('    [F-03] [STANDARD]'):f.index('Two details in that example')]; \
                   p='/tmp/crossed.md'; s=open(p).read(); \
                   open(p,'w').write(s.replace('## What passed','### '+b.strip()+'\n\n## What passed',1))"
       python3 tools/verify_citations.py /tmp/crossed.md

   It fails by name: *cites `reference/eu-clp-annex-vi/...` in a report declaring jurisdiction US.
   That file is the EU corpus.* The reverse fails the same way — an OSHA paragraph cited in an EU
   report. Delete the `Jurisdiction` row from a report instead and both report gates refuse it,
   because a guard the guarded document can switch off is not a guard.

   *Until this was fixed both gates passed it, with zero failures.* The rule was written in
   `identity.md`, `rules.md` Stage 5 and `config/CONTEXT.md`, and read by no script. It had already
   been broken once in this folder — CLP Annex VI cited against a US sheet — and was found by a
   person reading the report, in an architecture review, not by anything that runs.

## Rebuilding everything from source

    python3 tools/build_reference.py      # re-download the three standards and regenerate reference/

Every file under `reference/` is generated by that script from the publisher's own markup — eCFR
for the CFR, the EU Publications Office Cellar service for both EU regulations. Each folder carries
a `PROVENANCE.md` with the source URL, the retrieval date, and the SHA-256 of both the bytes
retrieved and the file produced. Nothing in `reference/` is written by hand, and nothing in it is a
summary.

## What is deliberately missing

- **OSHA Appendix D, Table D.1.** The current eCFR publishes it as a *graphic*, not text, so it
  cannot be quoted and Salus does not cite it. US structural findings rest on § 1910.1200(g)(2),
  (g)(3) and (g)(5), which are regulatory text and are shipped in full. Stated again in
  `identity.md` and `reference/CONTEXT.md`.
- **CLP Annex VI Table 3 in full.** Several thousand rows. What ships is every row whose identifier
  appears in the corpus, matched by CAS or by Index number. The count is stated in the header of
  the file itself, which is generated — this sentence deliberately does not repeat it, because a
  hand-copied number drifts. Audit a sheet from outside the corpus and rebuild.
- **Paywalled standards.** ISO 11014 and its like cannot be shipped, so they are not cited.
- **OCR.** Salus does not guess at pixels. A scanned sheet gets CANNOT VERIFY.

## The folder

    identity.md     who the auditor is, the three verdicts, the boundaries, the blind spots
    rules.md        how it audits: seven stages, the finding format, severity, token discipline
    examples.md     five real audits, covering all three verdicts
    reference/      the standards themselves, plus the ledger and the freshness log
    README.md       this file
    config/         jurisdiction and house policy — fill this in before the first run
    tools/          extraction, the scope gate, the three gates, the docs gate, builder, freshness
    test-cases/     22 real manufacturer sheets, and two constructed fixtures kept apart
    audits/         eight worked runs, with the renderings and fidelity reports they used

`README.md` is the only file of its kind, and it is this one — it addresses the person using or
judging the folder. Every other folder states its own contract in a `CONTEXT.md`: what it holds,
what may be written into it, and what a human checks before anything is added. Open the folder and
the contract is the first thing in it. `CLAUDE.md` routes an agent through the same structure
without repeating any of it.
