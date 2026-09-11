# Salus audit report

| | |
| --- | --- |
| Sheet | `BG - HCF MSDS 510231_UK_EN.pdf` — BG Special HCF Grease, BG Products Inc. |
| SHA-256 of the file audited | `34752e69bf899a8a…` — full digest in `BG - HCF MSDS 510231_UK_EN.fidelity.json` |
| Jurisdiction (from `config/jurisdiction.md`) | EU |
| Standard applied | Commission Regulation (EU) 2020/878, with CLP Annex VI for classification |
| Run date | 2026-09-11 |
| Standards knowledge last confirmed online | 2026-09-11 — see `reference/FRESHNESS-LOG.md` |
| Conversion gate | REVIEW — one token (`129`) appears in the independent extraction and not adjacently in the rendering; no chemical identifier diverges. Read before relying on this run. |

## VERDICT: DOES NOT CONFORM

Four findings. Two checked points passed and are listed below them, because an audit that reports
only what broke is a complaint.

---

### [F-01] [STANDARD] BLOCKING — compiled to a revision that may no longer be supplied

    WHAT   The sheet's header, repeated on all twelve pages, reads "Conforms to Regulation (EC)
           No. 1907/2006 (REACH), Annex II, as amended by Commission Regulation (EU) 2015/830 -
           United Kingdom (UK)". Regulation (EU) 2015/830 is the revision that 2020/878 replaced.
    WHERE  page 1 line 1, and the same line on every page of the sheet
    RULE   Regulation (EU) 2020/878, Article 2: "By way of derogation from Article 3, safety data
           sheets not complying with the Annex to this Regulation may continue to be provided
           until 31 December 2022."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Article 1 and Article 2
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    The derogation in Article 2 ran out on 31 December 2022. This sheet is audited on
           2026-09-11, three years and eight months after that date, so the revision it declares
           is one under which it may no longer be supplied. This is a finding about the sheet's
           declared revision, not about its chemistry.

### [F-02] [STANDARD] BLOCKING — Section 3 departs from a harmonised classification, twice, with no basis stated

    WHAT   Section 3 lists two base oils, each at >=25 - <=50 %:
             "Distillates (petroleum), hydrotreated heavy naphthenic", EC 265-155-0,
             CAS 64742-52-5, Index 649-465-00-7 — classified "Asp. Tox. 1, H304"
             "Distillates (petroleum), hydrotreated heavy paraffinic", EC 265-157-1,
             CAS 64742-54-7 — classified "Asp. Tox. 1, H304"
           Neither row carries a carcinogenicity classification, and the sheet nowhere states why.
    WHERE  page 2, lines 110-114 and 115-118 of the rendering
    RULE   CLP Annex VI Table 3 row 649-465-00-7 reads, in the hazard-class, hazard-statement
           and Notes columns: "Carc. 1B | H350 | GHS08 Dgr | H350 | | | L". Row 649-467-00-8, for
           CAS 64742-54-7, carries the same three values.
           Note L reads: "The harmonised classification as a carcinogen applies unless it can be
           shown that the substance contains less than 3 % of dimethyl sulphoxide extract as
           measured by IP 346"
    WHERE IN THE STANDARD
           reference/eu-clp-annex-vi/annex-vi-table-3-extract.md, rows 649-465-00-7 and 649-467-00-8
           reference/eu-clp-annex-vi/annex-vi-notes.md, Note L
           revision: 02008R1272-20260701
           confirmed current: 2026-09-11
    WHY    Both substances carry a harmonised classification as category 1B carcinogens. Note L
           allows a supplier to set that classification aside, but only where the DMSO extract is
           below 3 % by IP 346 — and the release is conditional on showing it. This sheet neither
           carries the harmonised classification nor records that the Note L condition was met, so
           a reader cannot tell whether the departure is lawful. The finding is the missing basis,
           not the choice of hazard code.

### [F-03] [STANDARD] BLOCKING — Section 11 contradicts the harmonised classification of two ingredients

    WHAT   Section 11 states "Carcinogenicity : No known significant effects or critical hazards."
           The same sheet lists two Annex VI category 1B carcinogens in Section 3, each present at
           >=25 - <=50 %.
    WHERE  Section 11, page 8 line 484 of the rendering, against Section 3, page 2 lines 110-118
    RULE   CLP Annex VI Table 3 row 649-465-00-7 reads "Carc. 1B | H350 | GHS08 Dgr | H350".
           Regulation (EU) 2020/878, Annex II, Section 11 requires the sheet to cover
           "carcinogenicity;" among the hazard classes it reports on.
    WHERE IN THE STANDARD
           reference/eu-clp-annex-vi/annex-vi-table-3-extract.md, row 649-465-00-7
           reference/eu-2020-878/regulation-2020-878.md, Annex II Section 11
           revision: 02008R1272-20260701
           confirmed current: 2026-09-11
    WHY    Two sections of one document say incompatible things about the same substances. Salus
           does not decide which is correct — it reports that the sheet does not let a reader
           determine that. Note that if the Note L condition in [F-02] were met and stated, this
           section could be correct; the two findings are the same gap seen from two sections.

### [F-04] [HOUSE POLICY — no provision] BLOCKING — sheet is seven years old

    WHAT   "Date of issue/Date of revision : 4/16/2019", version 5.1, "Date of previous issue :
           No previous validation". On the run date the sheet is 7 years and 5 months old.
    WHERE  page 1 line 62 of the rendering, and repeated in every page footer
    RULE   None. Neither Regulation (EU) 2020/878 nor 29 CFR 1910.1200 sets an expiry date for a
           safety data sheet. This finding rests on `config/jurisdiction.md`,
           `policy_max_age_years: 5`, and on nothing else. It is reported as a finding because
           this installation asked for it, and it is marked so that nobody mistakes it for law.
    WHERE IN THE STANDARD
           Not applicable — no provision. See rules.md, "Two classes of finding, never mixed".
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    The remedy is not a correction to this document. It is either a reissued sheet, or a
           written statement from the manufacturer that the composition has not changed and that
           this revision therefore still describes the product.

---

## What passed

### [P-01] [STANDARD] Section 3, antimony compounds — classification matches Annex VI exactly

    WHAT   Section 3 lists "antimony compounds", EC 240-028-2, CAS 15890-25-2,
           Index 051-003-00-9, at <=5 %, classified "Acute Tox. 4, H302 / Acute Tox. 4, H332 /
           Aquatic Chronic 2, H411".
    WHERE  page 2, lines 119-124 of the rendering
    RULE   CLP Annex VI Table 3 row 051-003-00-9 reads, in the hazard-class and
           hazard-statement columns: "Acute Tox. 4 * Acute Tox. 4 * Aquatic Chronic 2 | H332 H302 H411"
    WHERE IN THE STANDARD
           reference/eu-clp-annex-vi/annex-vi-table-3-extract.md, row 051-003-00-9
           revision: 02008R1272-20260701
           confirmed current: 2026-09-11
    WHY    Every hazard class and every hazard statement in the sheet matches the harmonised entry.
           This is a group entry carrying no CAS number of its own, so it is found by Index number.

### [P-02] [STANDARD] Sections 2 and 9 agree on flammability

    WHAT   Section 9 states "Flash point : Open cup: 235°C [Cleveland.]". Section 2.1 states
           "Not classified." and carries no flammability hazard statement.
    WHERE  Section 9 page 6 line 362, Section 2 page 1 lines 68-73 of the rendering
    RULE   Regulation (EU) 2020/878, Annex II, Section 9, on mixtures: "flash point(s) of the
           substance(s) with the lowest flash point(s) shall be indicated."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II Section 9
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    A flash point of 235 °C is far above the threshold at which a flammable-liquid
           classification arises, so the absence of one in Section 2 is consistent with the value
           in Section 9. The two sections agree.

---

## Declared blind spots

Stated on every report, whether or not they bit here.

- **Omissions are invisible.** If this product contains a substance the supplier did not list,
  Salus cannot know. Nothing above is a statement about what is in the product.
- **Self-classified substances were not checked for correctness.** Every substance in this sheet
  has a harmonised Annex VI entry, so this limit did not bite on this run.
- **No value was re-measured.** The flash point of 235 °C is checked for agreement with the rest
  of the sheet, not for truth.
- **US per-subheading content is not citable** — not applicable to this run, which is EU.
- **The conversion gate returned REVIEW, not PASS.** One token diverges between the two extraction
  engines. No chemical identifier does. A reader relying on this report should open
  `fidelity.json` first.

## What this verdict is not

DOES NOT CONFORM is a statement about this document against this standard on this date. It is not
a statement about the grease, about whether anyone may work with it, or about what should happen
next. Those decisions belong to the specialists this report goes to, under whatever regulations
and internal rules their organisation carries.
