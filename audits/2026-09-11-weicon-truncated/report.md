# Salus audit report

| | |
| --- | --- |
| Sheet | `TRUNCATED - WEICON 116905, sections 5 to 16 removed.pdf` (from `test-cases/sds-constructed/`) |
| Jurisdiction (from `config/jurisdiction.md`) | EU |
| Standard applied | Commission Regulation (EU) 2020/878, with CLP Annex VI for classification |
| Run date | 2026-09-11 |
| Standards knowledge last confirmed online | 2026-09-11 — see `reference/FRESHNESS-LOG.md` |
| Conversion gate | REVIEW — one token appears in the independent extraction and not adjacently in the rendering; no chemical identifier diverges |

## VERDICT: DOES NOT CONFORM

**Not CANNOT VERIFY**, and the distinction is the whole reason this fixture exists.

Every word of the four pages that are here is legible. The conversion gate passed the sheet through
with a single divergent token and no lost identifier. Salus could establish exactly what it was
looking at — and what it was looking at is a document missing three quarters of itself. That is a
failure against the standard, not an inability to read.

`CANNOT VERIFY` would have been the wrong answer, and the comfortable one. It would have filed a
real defect under *the auditor had a problem*, which is how a defect gets lost. Compare
`audits/2026-09-11-scanned-fixture/`, where the answer genuinely is CANNOT VERIFY: there, nothing
could be read at all, and no provision was applied.

Two findings, two passes.

---

### [F-01] [STANDARD] BLOCKING — twelve of the sixteen required sections are absent

    WHAT   The sheet carries Section 1 "Identification of the substance/mixture and of the company/
           undertaking", Section 2 "Hazards identification", Section 3 "Composition/information on
           ingredients", and Section 4 "First aid measures". It ends inside Section 4. Sections 5
           to 16 — firefighting, accidental release, handling and storage, exposure controls,
           physical and chemical properties, stability and reactivity, toxicological information,
           ecological information, disposal, transport, regulatory information, and other
           information — do not appear anywhere in the document.
    WHERE  Sections present at rendering lines 7, 46, 130 and 181; the document ends at line 256
    RULE   Regulation (EU) 2020/878, Annex II, Part A: "The safety data sheet shall include the
           following 16 headings"
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II Part A, the 16 headings
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    The requirement is not that the headings be present where the supplier has something to
           say under them; it is that the sheet include all sixteen. Twelve are missing, among
           them Section 8 exposure controls and Section 9 physical and chemical properties — the
           two a person handling the product reaches for first. There is no reading of the
           standard under which this document is complete.

### [F-02] [STANDARD] BLOCKING — the document declares its own length, and does not reach it

    WHAT   The footer of every page reads "Date of issue/Date of revision : 29/01/2026 · Date of
           previous issue : 04/11/2025 · Version : 3.5" followed by a page marker. Those markers
           read 1/20, 2/20, 3/20 and 4/20. The sheet states that it is twenty pages long. Four are
           present.
    WHERE  rendering lines 60, 124, 191 and 256
    RULE   Regulation (EU) 2020/878, Annex II, subsection 0.3.2: "All pages of a safety data sheet,
           including any annexes, shall be numbered and shall bear either an indication of the
           length of the safety data sheet"
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II subsection 0.3.2
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    The provision exists precisely so that an incomplete copy can be recognised as one. It
           did its job here: the sheet's own pagination is the evidence that sixteen pages are
           missing, and it is evidence a reader can check in four seconds without knowing anything
           about the product. Salus reports what the document says about itself. It does not
           speculate about how the pages came to be missing — a partial scan, a partial print, or
           a supplier sending an extract are all consistent with what is on the page, and telling
           them apart is not a document-compliance question.

---

## What passed

### [P-01] [STANDARD] Compiled to the revision in force, and recently

    WHAT   The header of every page reads "Conforms to Regulation (EC) No. 1907/2006 (REACH),
           Annex II, as amended by Commission Regulation (EU) 2020/878 - Germany". Date of issue
           and revision 29/01/2026, version 3.5, previous issue 04/11/2025.
    WHERE  rendering lines 1-2, and the footers at lines 60, 124, 191, 256
    RULE   Regulation (EU) 2020/878, Article 3: "It shall apply from 1 January 2021."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Article 3
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    The sheet names the current revision and was issued five years after it began to apply.
           No transition question arises, and at seven months old it is far inside the five-year
           house gate. **What is wrong with this document has nothing to do with its age or its
           revision** — which is worth stating, because those are the two things that went wrong
           in the other EU run in this folder.

### [P-02] [STANDARD] Section 3 — butane and propane match their harmonised entries

    WHAT   Section 3 lists "butane", CAS 106-97-8, EC 203-448-7, Index 601-004-00-0, at
           >=25 - <=50 %, classified "Flam. Gas 1A, H220" with "Press. Gas (Comp.), H280"; and
           "propane", CAS 74-98-6, EC 200-827-9, Index 601-003-00-5, at >=10 - <=25 %, classified
           the same way.
    WHERE  rendering lines 139-149
    RULE   CLP Annex VI Table 3 row 601-003-00-5, propane, reads in the hazard-class and
           hazard-statement columns: "Flam. Gas 1 Press. Gas | H220". Row 601-004-00-0, butane,
           reads the same.
    WHERE IN THE STANDARD
           reference/eu-clp-annex-vi/annex-vi-table-3-extract.md, rows 601-003-00-5 and 601-004-00-0
           revision: 02008R1272-20260701
           confirmed current: 2026-09-11
    WHY    The hazard statement matches exactly and both harmonised hazard classes are carried.
           The sheet writes "Flam. Gas 1A" where the harmonised row reads "Flam. Gas 1" — 1A is
           the sub-category a later amendment introduced beneath category 1, so the sheet is
           stating the harmonised classification more precisely rather than departing from it.
           That is the supplier's to do, and it is not a divergence.

---

## Declared blind spots

- **Omissions are invisible** — with a sharp edge on this run. Salus can see that Sections 5 to 16
  are missing, because the standard names them and the document declares its own page count. It
  cannot see what those twelve sections would have said, and nothing in this report is a statement
  about their content.
- **Self-classified substances cannot be called wrong.** Two ingredients in Section 3 — a
  hydrotreated light distillate at 25–50 % and an ethoxylated alcohol at 5–10 % — carry no Index
  number and no row in the shipped Annex VI extract. Their classification is the supplier's own and
  was not checked for correctness.
- **No value was re-measured.**
- **US per-subheading content is not citable here** — not applicable to this run, which is EU.
- **Nothing was assessed beyond Section 4**, because there is nothing there to assess. The
  consistency checks in `rules.md` Stage 6 that span Sections 7, 8, 9 and 16 could not run at all.

## What this verdict is not

DOES NOT CONFORM is a statement about this document against this standard on this date. It says
nothing about the penetrant spray, and nothing about whether the complete twenty-page sheet — which
exists, and is in `test-cases/sds/` — would conform. Only this copy was audited.
