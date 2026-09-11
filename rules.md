# How Salus audits

One pass, seven stages, in this order. Later stages depend on earlier ones: you cannot check a
provision until you know which revision of the standard applies, and you cannot know that until
you have read the sheet's own header. Do not reorder them.

Stop conditions are named at each stage. When a stage says stop, stop — do not "check the rest
anyway." A verdict reached on a document you could not read is worse than no verdict.

---

## Stage 0 — Settings

Read `config/jurisdiction.md`. It names the regime this installation audits under: `EU` or `US`.

- Not filled in → **CANNOT VERIFY**, reason: jurisdiction not configured. Stop.
- Never infer jurisdiction from an IP address, a locale, or where the supplier sits. A reviewer
  in Tel Aviv may be auditing for a German legal entity. The settings file is the answer.

## Stage 1 — Legibility, then scope

Two questions, in this order: can the sheet be read at all, and is it a sheet this folder has a
rulebook for. Either one can end the run before a single provision is opened.

### 1a — Legibility

Extract the sheet. `tools/extract.py` produces `<name>.salus.md`, a line-anchored rendering, plus
a fidelity report.

- No text layer, zero characters, or the fidelity check fails → **CANNOT VERIFY**, reason quoted
  from the fidelity report. Stop.
- Text extracted but no section headings found at all → **CANNOT VERIFY**. Stop.
- Partial: some sections legible, others empty → continue, and record each unreadable section as
  `not assessed — unreadable`, never as a failure.

### 1b — Scope

    python3 tools/check_scope.py <sheet.salus.md>     # the scope gate; exit 2 means stop

Read the sheet's own declaration of the standard it was **compiled to** — suppliers put it on the
first line, in the header, or in Section 15.

- **It declares a standard from a third regime — GB/T 16483, JIS Z 7253, GOST 30333, SOR/2015-17
  and the like — and declares neither 2020/878 nor 1910.1200** → **CANNOT VERIFY**, reason: out of
  scope. **Stop.** Name the standard the sheet declares, say that `reference/` does not ship it,
  and make no judgement about the sheet in its own regime. Run no further stages.
- It declares a third regime **and** the configured standard → continue. A sheet written for two
  markets is audited against the configured one, and the third declaration is not a finding.
- It declares the *other* standard this folder ships — a US sheet under `jurisdiction: EU`, or the
  reverse → continue. That is Stage 3's business and it is a finding there, not a stop: both
  rulebooks are here, so the comparison is real and says something useful.
- It declares nothing → continue. Stage 3 infers the revision from the issue date and says so.

Why this stops the run rather than becoming a finding: an auditor that does not hold the standard a
document was written to cannot say whether the document meets it. Measuring it against a different
standard yields one observation — the wrong ruler was used — restated once per provision, which
reads like a list of defects and is not one. This gate exists because exactly that was filed here
on 2026-09-11, before it existed. See `README.md` § *An incident, and the gate it produced*, and
the two runs in `audits/` that record it.

The stop is evidence-based, and only evidence-based: it fires on what the sheet **declares**, never
on a country name, an address, a language, an emergency telephone number or a chemical inventory
list. A sheet that tells a German reader its components appear on China's IECSC inventory is an EU
sheet with an inventory paragraph. Adding a regime to the gate's list is a deliberate edit to
`tools/check_scope.py`, and making a sheet pass by deleting one is forbidden outright.

A word is not a declaration either, and that cuts the other way — towards the stop, not away from
it. `REACH` is a regulation and an ordinary English verb, and *"Keep out of reach of children"* is
GHS precautionary statement P102, printed on sheets of every regime including the ones this folder
does not hold. The gate reads `REACH` as a declaration of Annex II only where the sheet writes it
as one: prepared, compiled, issued or conforming to it, or Annex II named beside it. Read loosely,
that one line of boilerplate was enough to suppress the stop on a sheet compiled to GB/T 16483.

## Stage 2 — Age gate *(house policy, not a provision)*

Find the date of issue or last revision. Compare with the run date.

- **≥ 5 years old → DOES NOT CONFORM.** The reason is recorded as a **policy gate**, and it is
  marked in the report as carrying no provision, because neither 2020/878 nor 1910.1200 sets an
  expiry. The rule exists because formulations change faster than sheets are reissued, and a
  sheet from 1997 read in 2026 is describing a different product. The remedy is a reissued sheet,
  or a written statement from the manufacturer that the composition has not changed.
- **No date found anywhere → CANNOT VERIFY.** Do not guess from a file timestamp.
- Under five years → record the age and continue.

The age gate never silently ends the audit. Continue through the remaining stages and report
everything you found, so the reviewer writing to the supplier has the whole list at once.

## Stage 3 — Which revision the sheet was compiled to

Look for the sheet's own declaration. Suppliers state it in the header — *"Conforms to Regulation
(EC) No. 1907/2006 (REACH), Annex II, as amended by Commission Regulation (EU) 2020/878"* — or
inside Section 15, or not at all.

Then open `reference/STANDARDS-LEDGER.md` and compare against the dates, not against your memory.

- **Declared revision superseded and its transition window closed** → finding, citing the article
  that closed it. For the EU that is 2020/878 Article 2, window closed 2022-12-31.
- **Declared revision superseded but the window is still open** → **not a finding.** Record it as
  a dated note: which revision, which deadline, how long is left. For US mixtures the window runs
  to 2027-11-19 under § 1910.1200(j)(3)(i), so most US sheets sit here today.
- **No declaration** → do not treat this as a failure by itself. Infer the applicable revision
  from the issue date against the ledger, and say in the report that you inferred it.
- **Compiled for the other regime** → a sheet built to 29 CFR 1910.1200 and audited under
  `jurisdiction: EU` has not been compiled to Annex II at all, and the reverse holds too. This is a
  finding, and it cites the article that makes the annex mandatory — for the EU, 2020/878 Article 1,
  *"Annex II to Regulation (EC) No 1907/2006 is replaced by the text in the Annex to this
  Regulation."* Report it once, at Stage 3, and continue: the remaining stages still say useful
  things about a sheet in the wrong format.

## Stage 4 — Structure: the sixteen sections

Check that all sixteen sections are present, numbered, in order, and carry content.

- EU: Annex II to 2020/878, Part A, sections 1–16, and the subheadings each section names.
- US: § 1910.1200(g)(2)(i)–(xvi) for the headings and their order; § 1910.1200(g)(3) for the rule
  that a subheading with nothing to report must be *marked* as such rather than left blank.

A blank subheading that is not marked is a finding under (g)(3) in the US and under the
corresponding Annex II requirement in the EU. An empty section is a finding. A missing section is
a finding. Quote the section number and the heading as it appears in the sheet.

## Stage 5 — Classification: Section 3 against CLP Annex VI

This is where sheets fail most often, and it is the stage that makes Salus an auditor rather than
a checklist.

**US runs stop before this stage.** 29 CFR 1910.1200 has no harmonised classification list, and
none is shipped for it. Under `jurisdiction: US`, record Section 3 as *not assessed for
classification correctness*, say so in the report's blind spots, and go to Stage 6. Citing CLP
Annex VI against a US sheet would be a finding under a regulation that does not govern it — the
exact false finding this folder is built to prevent.

**Both halves of that are now enforced, and were not until 2026-09-11.** `tools/verify_citations.py`
reads the regime out of the report's own header row and fails any finding whose `WHERE IN THE
STANDARD` names a file outside that regime's corpus: an EU run may cite `reference/eu-2020-878/`
and `reference/eu-clp-annex-vi/`, a US run may cite `reference/us-osha-hcs/` and nothing else.
`tools/validate_report.py` fails a US report that performed checks and nowhere records Section 3 as
*not assessed for classification correctness*. Until then the rule held because it was obeyed, which
is not the same thing as holding — it had already been broken once here, and was found by a person.

For each ingredient row in Section 3, on an EU run:

1. Read the identifiers: CAS number, EC number, Index number, REACH registration number.
2. Look the substance up in `reference/eu-clp-annex-vi/annex-vi-table-3-extract.md`, **by CAS or
   Index number**. Read one row. Do not read the file as prose — this is the whole reason a run
   costs a few thousand tokens instead of forty thousand.
3. **No row** → not harmonised. Record `self-classification, not checked` and move on. You have
   no provision to test it against and must not invent one.
4. **Row found** → compare the hazard class and category codes and the hazard statement codes in
   the sheet with the row.
   - Identical → passes. Say so; a pass is part of the report.
   - Sheet declares **more** than the row → not a finding. A supplier may classify more strictly
     than the harmonised minimum.
   - Sheet declares **less** than the row → check the Notes column first.
5. **Notes column.** If the row carries a note, open
   `reference/eu-clp-annex-vi/annex-vi-notes.md` and read that note before writing anything. Most
   of them are conditional releases from part of the harmonised classification, and a supplier
   relying on one is not in breach — but the sheet has to show it relied on it. Note L, for
   example, releases certain petroleum substances from the carcinogen classification only where
   the DMSO extract is below 3 % measured by IP 346. The finding in that case is not "wrong hazard
   code"; it is that the sheet departs from a harmonised classification **without recording the
   basis** the note requires. Write it that way.

## Stage 6 — Internal consistency

The standard requires a coherent document, not sixteen unrelated lists. Check that the same fact
told twice is told the same way.

| Check | What contradicts what |
| --- | --- |
| Flash point | the value in Section 9 against every other mention of it, and against the flammability class declared in Section 2 |
| Concentration | each ingredient's percentage band in Section 3 against any concentration limit the Annex VI row sets, and against the hazard statements in Section 2 |
| Hazard statements | the H-codes in Section 2 against the H-codes listed in Section 16 and against those in Section 3 |
| Physical state | Section 9 against Section 1's product type |
| Emergency contact | present in Section 1.4, and a number, not a placeholder |
| Storage and handling | Section 7 against the hazards declared in Section 2 |
| Disposal, transport, regulatory | Sections 13–15 present and populated, with the US caveat in `identity.md` |

Report a contradiction as a contradiction: quote both values, name both sections, and say that
the sheet does not let a reader determine which is correct. Do not pick a winner — you have no
basis to, and choosing one would be advising about the material.

---

## How a finding is written

Every finding carries five things. A finding missing any of them is not shippable, and a label
with nothing written under it is missing: `tools/verify_citations.py` reads the body, not the word.

    [F-03] [STANDARD] BLOCKING — Section 3 departs from Annex VI without the Note L basis
      WHAT   Section 3 lists "Distillates (petroleum), hydrotreated heavy naphthenic",
             CAS 64742-52-5, at >=25 - <=50 %, classified "Asp. Tox. 1, H304".
      WHERE  page 2, line 110 of BG - HCF MSDS 510231_UK_EN.pdf
      RULE   CLP Annex VI Table 3 row 649-465-00-7 reads, in the hazard-class, hazard-statement
             and Notes columns: "Carc. 1B | H350 | GHS08 Dgr | H350 | | | L".
             Note L reads: "The harmonised classification as a carcinogen applies unless it can
             be shown that the substance contains less than 3 % of dimethyl sulphoxide extract
             as measured by IP 346"
      WHERE IN THE STANDARD
             reference/eu-clp-annex-vi/annex-vi-table-3-extract.md, row 649-465-00-7
             reference/eu-clp-annex-vi/annex-vi-notes.md, Note L
             revision: 02008R1272-20260701
             confirmed current: 2026-09-11
      WHY    The harmonised entry classifies this substance as a category 1B carcinogen. The
             sheet does not carry that classification and does not state that the Note L
             condition was met, so a reader cannot tell whether the departure is lawful.

Two details in that example are not cosmetic, and `tools/verify_citations.py` enforces both.

**Every quoted string is checked, however short.** The gate pulls each string between double
quote marks out of the RULE and looks for it in the file the finding names — `"Carc. 1B"`, `"H350"`
and `"Note L"` exactly as readily as a whole sentence. Quote the standard's own words, at whatever
length says the thing, and quote them as they read.

There was a floor here until 2026-09-11: strings shorter than twelve characters were skipped, and
this file defended that by saying two short quotes on one line are read as one quote running from
the first closing mark to the next opening one. **That was never true of the regex that does the
reading.** Its character class cannot cross a quote mark, so `"Carc. 1B", column "L"` yields two
needles and not one. What the floor did instead was leave the hazard classes, the H-codes and the
Note letters — the atoms of a classification finding, and the strings a reader is least able to
check by eye — unverified, on a justification that a reader could have disproved in one line of
Python. It is gone.

**The example above is itself run through the gate**, by `tools/test_docs_example.py`, which lifts
it out of this file and puts it through the real citation and boundary checks. It has to be: this
is the file an auditor reads to learn how to cite, and a format taught here that the gate rejects
would be worse than no example at all. Run it after editing this section.

`WHERE IN THE STANDARD` is three parts, not one: the file and the row, the revision it belongs
to, and the date that revision was last confirmed current. A finding is checkable in time as well
as in text — a report read six months from now still says what Salus knew when it was written.

## Two classes of finding, never mixed

| Class | Marked | Has a provision | Example |
| --- | --- | --- | --- |
| **Standard violation** | `[STANDARD]` | yes, always | Section 3 classification against Annex VI |
| **Policy gate** | `[HOUSE POLICY — no provision]` | no, and it says so | the five-year age gate |

Both can produce DOES NOT CONFORM. They must never look alike on the page. A reader has to be
able to tell at a glance which findings the law requires and which this installation requires,
because those two carry different weight in a conversation with a supplier.

The marker is also how `tools/verify_citations.py` recognises a finding at all. A heading that
omits it is not a finding to the gate: nothing under it is read, no provision is looked for, and
the report leaves the gate with the same counts as if the block had never been written. So an
unmarked heading is failed on sight, by name, before any other check runs.

## Severity

Three levels, and severity never changes the verdict — any finding of either class produces DOES
NOT CONFORM. Severity orders the list so the reviewer knows what to raise first.

- **BLOCKING** — the sheet cannot serve its purpose: a missing or empty section, a superseded
  revision past its window, a classification that understates a harmonised entry, a contradiction
  in a value that drives a hazard class.
- **MATERIAL** — a reader can still use the sheet but the standard is not met: an unmarked empty
  subheading, a missing identifier, a note relied on without stating the basis.
- **MINOR** — formal defects: ordering, numbering, a heading that does not match the wording the
  standard sets.

## Token discipline

A run stays under roughly 10,000 tokens because of *how* the reference layer is read, not because
anything is skipped.

- Read the sheet through its extracted `.salus.md`, and read sections by anchor, not the whole file.
- Read Annex VI **by identifier lookup**. One CAS number, one row. Never load the table.
- Open `annex-vi-notes.md` only when a row's Notes column is non-empty, and read only that note.
- Open the standard's text at the provision you are about to cite, not before.
- The full converted sheet is shipped beside the report so a judge can read all of it. You do not
  have to, and the two facts are not in tension: what is shipped and what is read are different
  questions.

## Before the report leaves

Run all three. A report that has not passed them has not been produced.

    python3 tools/test_docs_example.py               # gate 0: does this file still teach a shape that ships
    python3 tools/verify_conversion.py <sheet.pdf>   # gate 1: is the conversion faithful
    python3 tools/check_scope.py <sheet.salus.md>    # the scope gate: is there a rulebook for this sheet
    python3 tools/verify_citations.py <report.md>    # gate 2: does every citation exist and match
    python3 tools/validate_report.py <report.md>     # gate 3: verdict shape and the hard boundaries

The scope gate is the odd one out and runs at Stage 1b, not here: it guards the run rather than the
report, and it is the only check that can end an audit before it starts.

Both report gates read the regime out of the report's header table — the row
`| Jurisdiction (from `config/jurisdiction.md`) | EU |` — and a report that carries no such row
fails both. Write the header before you write the findings; it is what decides which rulebook the
findings are allowed to stand on. See `tools/CONTEXT.md` § *Which jurisdiction a report gate believes*
for why that row, and not the config file, is what the gates trust.

Gate 3 is the one that catches you. It scans the report for permission language in English and
Russian and voids the run if it finds any. Run these as cold subagents with no knowledge of how
the audit went, or run them as scripts — either way the checker must not be the thing that made
the claim.
