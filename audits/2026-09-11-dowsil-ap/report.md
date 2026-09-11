# Salus audit report

| | |
| --- | --- |
| Sheet | `DOWSIL™ AP Silicone Adhesive Sealant White - DE(EN).pdf` — DOWSIL™ AP Silicone Adhesive/Sealant White, Dow Deutschland Anlagengesellschaft mbH |
| Jurisdiction (from `config/jurisdiction.md`) | EU |
| Standard applied | Commission Regulation (EU) 2020/878, with CLP Annex VI for classification |
| Run date | 2026-09-11 |
| Standards knowledge last confirmed online | 2026-09-11 — see `reference/FRESHNESS-LOG.md` |
| Conversion gate | PASS — every distinct character, token and chemical identifier found by the independent engine is present in the shipped rendering |

## VERDICT: CONFORMS

On every point checked, this sheet meets the standard. Six checks are listed below with the
provision each one rests on, so a reader can disagree with any of them by opening the file named.

The points Salus did not check are listed under Declared blind spots. CONFORMS means the six
checks passed; it does not mean the sheet is perfect and it says nothing about the product.

---

### [P-01] [STANDARD] Compiled to the revision in force

    WHAT   The header on every page reads "Safety Data Sheet according to Reg. (EU) 2020/878".
           Revision Date 23.09.2021, Version 4.0, Date of last issue 08.04.2021.
    WHERE  page 1, header block, and repeated in every page header
    RULE   Regulation (EU) 2020/878, Article 3: "It shall apply from 1 January 2021."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Article 3
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    The sheet was revised on 23 September 2021, after the regulation began to apply, and
           declares that revision by name. No transition question arises.

### [P-02] [STANDARD] All sixteen sections present, numbered and in order

    WHAT   Sections 1 to 16 appear once each, in ascending order, each carrying content. No
           section is empty and none is missing.
    WHERE  rendering lines 14, 39, 91, 175, 208, 244, 264, 292, 518, 571, 593, 1109, 1420, 1440,
           1492, 1552
    RULE   Regulation (EU) 2020/878, Annex II, Part A, Section 3 opening: "This section of the
           safety data sheet shall describe the chemical identity of the ingredient(s) of the
           substance or mixture, including impurities and stabilising additives as set out below."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II Part A
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    The headings and their order match the sixteen the Annex sets out. The provision quoted
           is the opening of one of them, shown as the form the Annex uses throughout.

### [P-03] [STANDARD] Section 3 — D4 matches its harmonised entry exactly

    WHAT   Section 3 lists "octamethylcyclotetrasiloxane [D4]", CAS 556-67-2, EC 209-136-7,
           Index 014-018-00-1, at >= 0,2 - <= 0,29 %, classified "Flam. Liq. 3; H226 / Repr. 2;
           H361f / Aquatic Chronic 1; H410" with "M-Factor (Chronic aquatic toxicity): 10".
    WHERE  rendering page 2, Section 3 ingredient table
    RULE   CLP Annex VI Table 3 row 014-018-00-1 reads: "Repr. 2 Aquatic Chronic 1 | H361f *** H410 | GHS08 GHS09 Wng"
           and carries "M = 10" in the concentration-limits column.
    WHERE IN THE STANDARD
           reference/eu-clp-annex-vi/annex-vi-table-3-extract.md, row 014-018-00-1
           revision: 02008R1272-20260701
           confirmed current: 2026-09-11
    WHY    Every harmonised element matches: hazard classes Repr. 2 and Aquatic Chronic 1, hazard
           statements H361f and H410, M-factor 10. The sheet additionally declares Flam. Liq. 3 /
           H226, which the harmonised entry does not cover. Classifying more strictly than the
           harmonised minimum for a class the entry is silent on is the supplier's to do, so this
           is not a divergence.

### [P-04] [STANDARD] Section 3 — two ingredients correctly left to self-classification

    WHAT   Section 3 lists "titanium dioxide", CAS 13463-67-7, at <= 2,0 %, classified "Carc. 2;
           H351"; and "Bis[(2-ethyl-2,5-dimethylhexanoyl)oxy](dimethyl)stannane", CAS 68928-76-7,
           at >= 0,01 - <= 0,02 %, with the Index-No. field shown as "–".
    WHERE  rendering page 2, Section 3 ingredient table
    RULE   Regulation (EU) 2020/878, Annex II, Section 3.2: "The product identifier, the
           concentration or concentration ranges and the classifications shall be provided for at
           least all substances referred to in points 3.2.1 or 3.2.2."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II Section 3.2
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    Neither substance appears in the Annex VI extract for this corpus, and the sheet itself
           shows no Index number for the stannane. Where there is no harmonised entry the supplier
           classifies, and Salus has no provision against which to call that classification wrong.
           What the standard does require here — identifier, concentration range, classification —
           is present for both. That is what passed. Whether the classifications are correct is
           outside what this auditor can see; see Declared blind spots.

### [P-05] [STANDARD] Section 2.3 discloses the PBT/vPvB substances above the threshold

    WHAT   Section 2.3 states that the product contains D4, identified by the ECHA Member State
           Committee as meeting the PBT and vPvB criteria of Annex XIII, and D6, identified as
           meeting the vPvB criteria. Section 3 puts D4 at >= 0,2 - <= 0,29 % and D6 at
           >= 0,36 - <= 0,43 %.
    WHERE  Section 2.3, rendering lines 70-76; concentrations in Section 3
    RULE   Regulation (EU) 2020/878, Annex II, subsection 2.3: "For a mixture, information shall
           be provided for each such substance that is present in the mixture at a concentration
           equal to or greater than 0,1 % by weight."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II subsection 2.3
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    Both substances sit above the 0,1 % threshold at which the disclosure obligation bites,
           and both are disclosed by name in 2.3 with a pointer to Section 12. The concentrations
           in Section 3 and the disclosure in Section 2.3 agree.

### [P-06] [STANDARD] Sections 2 and 9 agree on flammability

    WHAT   Section 9 states "Flash point closed cup >100 °C". Section 2.1 states "Not a hazardous
           substance or mixture according to Regulation (EC) No. 1272/2008." and declares no
           flammable-liquid hazard for the mixture.
    WHERE  Section 9 rendering line 540; Section 2.1 rendering lines 41-43
    RULE   Regulation (EU) 2020/878, Annex II, Section 9, on mixtures: "flash point(s) of the
           substance(s) with the lowest flash point(s) shall be indicated."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II Section 9
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    A closed-cup flash point above 100 °C is well above the range in which a
           flammable-liquid classification arises, so the absence of one in Section 2 is
           consistent with the value in Section 9. The mixture is separately labelled with
           EUH208, EUH210 and EUH212, which are supplemental statements and not a classification.

---

## Noted, not a finding

**The sheet is 4 years and 11.6 months old.** Revision date 23.09.2021, run date 2026-09-11. The
house gate in `config/jurisdiction.md` is `policy_max_age_years: 5`, so this sheet clears it by
twelve days. It is recorded here because the reviewer who reads this report in October will be
looking at a sheet that no longer clears it, and neither standard would have told them so — no
provision sets an expiry.

## Declared blind spots

- **Omissions are invisible.** If this product contains a substance the supplier did not list,
  Salus cannot know it. Nothing above is a statement about what is in the product.
- **Two of the four listed substances were not checked for correctness.** Titanium dioxide and the
  stannane have no harmonised Annex VI entry in the shipped extract, so their classification is
  the supplier's own and no provision here says what correct would be. This bit on this run: see
  [P-04].
- **No value was re-measured.** The flash point above 100 °C is checked for agreement with the
  rest of the sheet, not for truth.
- **US per-subheading content is not citable** — not applicable to this run, which is EU.
- **Sections 4 to 8 and 10 to 16 were checked for presence and for the consistency listed in
  rules.md Stage 6, not clause by clause.** A conforming verdict covers the six checks above.

## What this verdict is not

CONFORMS is not a release, a clearance, or an approval, and it is not a statement about the
sealant. It means one document met one standard on the points listed, on one date. What happens
next belongs to the specialists this report goes to, under whatever regulations and internal rules
their organisation carries.
