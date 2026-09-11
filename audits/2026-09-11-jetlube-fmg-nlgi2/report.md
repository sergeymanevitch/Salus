# Salus audit report

| | |
| --- | --- |
| Sheet | `JET-LUBE - FMG™ NLGI 2_EU_GB_EN_1.4.pdf` — FMG™ NLGI 2, Whitmore Manufacturing LLC, distributed by Whitmore Europe Limited |
| Jurisdiction (from `config/jurisdiction.md`) | EU |
| Standard applied | Commission Regulation (EU) 2020/878, with CLP Annex VI for classification |
| Run date | 2026-09-11 |
| Standards knowledge last confirmed online | 2026-09-11 — see `reference/FRESHNESS-LOG.md` |
| Conversion gate | PASS — the rendering reproduces the extraction byte for byte, and nothing the independent engine found is missing from it |

## VERDICT: DOES NOT CONFORM

Three findings, all against the standard; none against house policy. Seven checks passed and are
listed with the same weight, because a report that shows only what broke cannot be argued with.

Each finding names the provision and quotes it. Open the file named and disagree with any of them.

---

## Findings

### [F-01] [STANDARD] MATERIAL — Section 2.1 carries a statement of the kind Annex II forbids

    WHAT   Section 2.1, under the heading "Adverse physicochemical, human health and
           environmental effects", reads: "To our knowledge, this product does not present any
           particular risk, provided it is handled in accordance with good occupational hygiene
           and safety practice." Section 2.1 declares the mixture "Not classified".
    WHERE  rendering lines 59-61, of JET-LUBE - FMG™ NLGI 2_EU_GB_EN_1.4.salus.md
    RULE   Regulation (EU) 2020/878, Annex II, Part A, subsection 0.2.4: "any other statements
           indicating that the substance or mixture is not hazardous or any other statements that
           are inconsistent with the classification of that substance or mixture shall not be
           used."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II Part A subsection 0.2.4
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    0.2.4 names the forbidden form by example — "no health effects", "harmless" — and then
           closes the list with any other statement indicating the mixture is not hazardous. The
           sentence in 2.1 is of that form. The finding does not turn on whether the sentence is
           true: the provision bars the construction itself, because a general reassurance placed
           where the adverse effects belong is not a statement a reader can check against
           sections 9 to 12. The same subsection 2.1 requires those effects to be listed "in such
           a way as to allow non-experts to identify the hazards"; here the sentence stands in
           their place.

### [F-02] [STANDARD] MATERIAL — a revised sheet with no indication of what changed

    WHAT   The first page reads "Issue date: 12/21/2020 Revision date: 3/5/2025 Supersedes
           version of: 11/14/2022 Version: 1.4". Section 16 carries the abbreviations list and
           the full text of EUH210, and nothing on the revision. No change marking, change bar or
           summary of changes appears anywhere in sections 1 to 16.
    WHERE  rendering line 4 (header block); Section 16 at rendering lines 381-436
    RULE   Regulation (EU) 2020/878, Annex II, Part A, subsection 0.2.5: "When a safety data sheet
           has been revised and the new, revised version is provided to recipients, the changes
           shall be brought to the attention of the recipients in Section 16 of the safety data
           sheet, unless the changes have been indicated elsewhere."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II Part A subsection 0.2.5
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    0.2.5 sets two obligations for a revised sheet. The first — a revision date on the
           first page and an indication of which version is replaced — this sheet meets: both the
           date and the superseded version are in the header. The second is not met. Version 1.4
           replaces the version of 14 November 2022, and a recipient holding that earlier version
           cannot tell from this document which of its sixteen sections moved. The escape clause
           does not apply: Salus read every section and found no indication of changes elsewhere.

### [F-03] [STANDARD] MATERIAL — Section 9 records flammability as not applicable to a solid

    WHAT   Section 9.1 states "Physical state : Solid", "Appearance : Grease." and
           "Flammability : Not applicable". Three lines below it states "Flash point : > 221 °C
           Cleveland Open Cup Method".
    WHERE  rendering lines 187, 189, 195 and 198
    RULE   Regulation (EU) 2020/878, Annex II, Part A, subsection 9.1, point (f) Flammability:
           "Applies to gases, liquids and solids. It shall be indicated whether the substance or
           mixture is ignitable, i.e. capable of catching fire or being set on fire, even if not
           classified for flammability."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II Part A subsection 9.1 point (f)
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    The sheet's own Section 9 puts this mixture in the solid state, and point (f) states in
           its first sentence that it applies to solids. "Not applicable" therefore records that a
           property does not apply in a case where the provision says it does, and the indication
           the point actually calls for — whether the mixture is ignitable — is absent. The
           provision anticipates exactly this sheet's situation: it requires the indication "even
           if not classified for flammability", and this mixture is not classified. The flash
           point stated three lines below is a different characteristic and does not supply it.

---

## What passed

### [P-01] [STANDARD] Compiled to the revision in force, and declared

    WHAT   The header on every page reads "according to the REACH Regulation (EC) 1907/2006
           amended by Regulation (EU) 2020/878". Revision date 3/5/2025, Version 1.4.
    WHERE  rendering lines 3-4, repeated at lines 74, 148, 218, 287, 360, 419
    RULE   Regulation (EU) 2020/878, Article 2: "By way of derogation from Article 3, safety data
           sheets not complying with the Annex to this Regulation may continue to be provided
           until 31 December 2022."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Article 2
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    The transition window Article 2 opened closed on 31 December 2022. This sheet was
           revised on 5 March 2025, after it closed, and names the current Annex II revision by
           number. No transition question arises, and the revision declared is the one the
           ledger records as in force.

### [P-02] [STANDARD] All sixteen sections present, numbered and in order

    WHAT   Sections 1 to 16 appear once each, in ascending order, each carrying content. No
           section is empty, none is missing, and the document's own pagination runs 1/7 to 7/7
           with no gap.
    WHERE  rendering lines 8, 54, 81, 86, 98, 108, 125, 136, 185, 225, 240, 261, 290, 295, 333, 381
    RULE   Regulation (EU) 2020/878, Annex II, Part B: "The safety data sheet shall include the
           following 16 headings in accordance with Article 31(6) and in addition the subheadings
           also listed except section 3, where only subsection 3.1 or subsection 3.2 needs to be
           included as appropriate:"
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II Part B
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    The sixteen headings match the Part B list in wording and order, and the subheadings
           Part B names are present under each. Section 3 carries 3.2 only, which is what Part B
           permits for a mixture.

### [P-03] [STANDARD] Section 3 states the basis on which it lists nothing

    WHAT   Section 3.2 reads: "This mixture does not contain any substances to be mentioned
           according to the criteria of section 3.2 of REACH Annex II". The subheading is present
           and the statement is in it; the section is not blank.
    WHERE  rendering lines 81-83
    RULE   Regulation (EU) 2020/878, Annex II, subsection 3.2: "The product identifier, the
           concentration or concentration ranges and the classifications shall be provided for at
           least all substances referred to in points 3.2.1 or 3.2.2."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II subsection 3.2
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    The obligation in 3.2 is to list the substances that meet the 3.2.1 or 3.2.2 criteria.
           The sheet states that none do, and marks the subheading rather than leaving it empty,
           which is what passes here. Whether that statement is correct is outside what this
           auditor can see — no substance is named, so no Annex VI lookup was possible and none
           was made. See Declared blind spots.

### [P-04] [STANDARD] Section 2.1 states plainly that the mixture is not classified

    WHAT   Section 2.1 reads "Classification according to Regulation (EC) No. 1272/2008 [CLP]"
           followed by "Not classified".
    WHERE  rendering lines 55-57
    RULE   Regulation (EU) 2020/878, Annex II, subsection 2.1: "If the mixture does not meet the
           criteria for classification in accordance with Regulation (EC) No 1272/2008, this shall
           be clearly stated."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II subsection 2.1
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    The provision requires the absence of classification to be stated, not left to
           inference from an empty field. It is stated, under the CLP heading, in two words.

### [P-05] [STANDARD] Section 2.2 and Section 16 agree, and the statement is written out in full

    WHAT   Section 2.2 lists "EUH210 - Safety data sheet available on request." Section 16, under
           "Full text of H- and EUH-statements:", repeats "EUH210 Safety data sheet available on
           request." No other hazard or EUH statement appears anywhere in the sheet.
    WHERE  rendering line 64 (Section 2.2) and lines 432-433 (Section 16)
    RULE   Regulation (EU) 2020/878, Annex II, subsection 2.1: "If the classification, including
           the hazard statements, is not written out in full, reference shall be made to section
           16 where the full text of each classification, including each hazard statement, shall
           be given."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II subsection 2.1
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    The one statement the sheet carries is written out in full in both places, in the same
           words. Stage 6 checks that the same fact told twice is told the same way; here it is.

### [P-06] [STANDARD] Section 1.4 gives emergency services and states their limits

    WHAT   Section 1.4 gives a 24-hour chemical emergency number for inside and outside the
           USA/Canada, a Great Britain number "+44.1865.407333", five National Poisons Information
           Service centres on "0344 892 0111", each marked "Only for healthcare professionals",
           and NHS 111. These are numbers, not placeholders.
    WHERE  rendering lines 26-51
    RULE   Regulation (EU) 2020/878, Annex II, subsection 1.4: "If availability of such services
           is limited for any reasons, such as hours of operation, or if there are limits on
           specific types of information provided, this shall be clearly stated."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II subsection 1.4
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    The provision's second obligation is the one sheets usually drop: where access to a
           service is restricted, the restriction has to be on the page. This sheet marks the
           restriction against each of the five NPIS centres, in the table, beside the number.

### [P-07] [STANDARD] Section 2.3 addresses PBT, vPvB and endocrine disruption

    WHAT   Section 2.3 states "Contains no PBT and/or vPvB substances ≥ 0.1% assessed in
           accordance with REACH Annex XIII", and that the mixture contains no substance on the
           Article 59(1) list for endocrine disrupting properties, nor identified as such under
           Regulation (EU) 2017/2100 or (EU) 2018/605, "at a concentration equal to or greater
           than 0,1 %".
    WHERE  rendering lines 65-66 and 76-78
    RULE   Regulation (EU) 2020/878, Annex II, subsection 2.3: "For a mixture, information shall
           be provided for each such substance that is present in the mixture at a concentration
           equal to or greater than 0,1 % by weight."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II subsection 2.3
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    All three limbs the subsection names — Annex XIII criteria, the Article 59(1) list, and
           the 2017/2100 / 2018/605 criteria — are addressed, each against the 0,1 % threshold the
           provision sets. That the answer is negative in each case is a disclosure, and it is the
           disclosure the provision asks for.

---

## Noted, not a finding

**The sheet clears the house age gate.** Revision date 5 March 2025, run date 2026-09-11 — one
year and six months. `config/jurisdiction.md` sets `policy_max_age_years: 5`. No policy finding
arises on this run, and none is recorded.

**Section 9 gives no reasons for its "Not available" entries.** Eleven properties — odour
threshold, melting point, boiling point, decomposition temperature, pH, log Kow, vapour pressure,
density, relative density, particle size — are marked "Not available" with no reason given.
Subsection 9.1 requires the absence to be "clearly indicated, giving the reasons where possible".
It is clearly indicated. Whether giving a reason was possible is a fact about the supplier's data,
not about this document, so Salus cannot test the condition the obligation hangs on and does not
raise it as a finding. It is recorded here because a reviewer writing to the supplier may want to
ask.

**Section 16 carries no literature references and no classification method.** Points (c) and (d)
of Annex II section 16 name both. The list they sit in is introduced by "such as", not by a
"shall" attaching to each item, so Salus does not raise them as breaches. Point (a) of the same
list is raised as [F-02], and only because subsection 0.2.5 states the same obligation
independently, in mandatory terms.

**Section 15.1 lists a US inventory under "National regulations".** The sheet records TSCA status
for a GB/EU-market document. Subsection 15.1 requires national regulatory status to be given
"where relevant", which is a judgement about the market this sheet serves, not a test this auditor
can run on the page. Not raised.

## Declared blind spots

- **Omissions are invisible.** Section 3 names no substance. Salus cannot know whether a substance
  meeting the 3.2.1 or 3.2.2 criteria was left out, and nothing above is a statement about what is
  in this product.
- **No classification was checked against CLP Annex VI on this run.** Stage 5 looks up each
  ingredient row by CAS or Index number; there are no rows, so no lookup was performed and no
  harmonised entry was compared. This is not the same as finding the classification correct.
- **Self-classification is not checked.** The mixture's own "Not classified" rests on the
  supplier's evaluation of its ingredients. No shipped provision says what correct would be for a
  mixture-level classification, so it is recorded, not tested.
- **No value was re-measured.** The flash point above 221 °C, the kinematic viscosity above
  25 mm²/s and the VOC content below 0,1 % are checked for agreement with the rest of the sheet,
  not for truth.
- **Sections 4 to 8 and 10 to 15 were checked for presence, for marked subheadings and for the
  consistency listed in `rules.md` Stage 6, not clause by clause.** A finding absent from this
  report is not a clause proved met.
- **The sheet, not the shipment.** Whether version 1.4 is the version that travelled with the
  container in the warehouse is outside this document.
- **US per-subheading content is not citable** — not applicable to this run, which is EU.

## What this verdict is not

DOES NOT CONFORM is a statement about a document and about nothing else. It is not a statement
about the grease, and no part of this report is. What the three findings need is a corrected sheet
from the supplier; what the material needs, if anything, is decided by the specialists this report
goes to, under whatever regulations and internal rules their organisation carries.
