# Salus audit report

| | |
| --- | --- |
| Sheet | `CARBOLINE - Carboguard_890 - 0986A1NL_2_USANSI.pdf` — Carboguard 890 Part A, Carboline |
| Jurisdiction (from `config/jurisdiction.md`) | **US** |
| Standard applied | 29 CFR 1910.1200, Hazard Communication |
| Run date | 2026-09-11 |
| Standards knowledge last confirmed online | 2026-09-11 — see `reference/FRESHNESS-LOG.md` |
| Conversion gate | REVIEW — three tokens appear in the independent extraction and not adjacently in the rendering; no chemical identifier diverges. The source PDF also carries damaged compressed streams, which poppler reports and recovers from. Read `fidelity.json` before relying on this run. |

## VERDICT: DOES NOT CONFORM

Two findings, three passes. This is the only US run in `audits/`; the other three are EU.

---

### [F-01] [STANDARD] MATERIAL — Section 16 carries no date of preparation or last revision

    WHAT   Section 16 "Other Information" contains the full text of the hazard statements used in
           Section 3, then "Reasons for revision / No Information", then a liability disclaimer.
           It carries no date. The revision date exists on the sheet — "Revision Date: 03/25/2019"
           — but it sits in the running page header, not in Section 16.
    WHERE  Section 16 at rendering line 602, running to the end of the document at line 625; the
           header date at rendering line 14
    RULE   29 CFR 1910.1200(g)(2)(xvi): "Section 16, Other information, including date of
           preparation or last revision."
    WHERE IN THE STANDARD
           reference/us-osha-hcs/29-cfr-1910-1200.md, paragraph (g)(2)(xvi)
           revision: 29 CFR 1910.1200, eCFR point-in-time 2026-09-01
           confirmed current: 2026-09-11
    WHY    The provision names the date as content *of section 16*, not merely of the document.
           A reader who turns to the section the standard sends them to does not find it there.
           The remedy is one line, and the information already exists elsewhere on the sheet —
           which is why this is MATERIAL and not BLOCKING.

### [F-02] [HOUSE POLICY — no provision] BLOCKING — the sheet is seven years old

    WHAT   "Revision Date: 03/25/2019". On the run date the sheet is 7 years and 5 months old.
           The printed date on the document is later, 03/26/2020, but that is when the copy was
           printed, not when the content was revised, and the age gate runs on the revision.
    WHERE  rendering line 14, repeated in the header of all ten pages
    RULE   None. 29 CFR 1910.1200 sets no expiry date for a safety data sheet. This finding rests
           on `config/jurisdiction.md`, `policy_max_age_years: 5`, and on nothing else. It is
           marked so that nobody mistakes it for a federal requirement.
    WHERE IN THE STANDARD
           Not applicable — no provision. See rules.md, "Two classes of finding, never mixed".
           revision: 29 CFR 1910.1200, eCFR point-in-time 2026-09-01
           confirmed current: 2026-09-11
    WHY    The remedy is not a correction to this document but a reissued sheet, or a written
           statement from the manufacturer that the composition has not changed. Note that the
           sheet was revised before the 2024 rewrite of this standard took effect — see the
           transition note below, which is a separate matter and is **not** a finding.

---

## What passed

### [P-01] [STANDARD] All sixteen sections present, numbered, and in the order the standard sets

    WHAT   Sections 1 to 16 each appear once, numbered, in ascending order, each carrying content:
           Identification; Hazard Identification; Composition/Information On Ingredients;
           First-aid Measures; Fire-fighting Measures; Accidental Release Measures; Handling and
           Storage; Exposure Controls/Personal Protection; Physical and Chemical Properties;
           Stability and Reactivity; Toxicological Information; Ecological Information; Disposal
           Considerations; Transport Information; Regulatory Information; Other Information.
    WHERE  rendering lines 10, 40, 109, 152, 170, 186, 208, 227, 307, 346, 371, 466, 514, 525,
           539, 602
    RULE   29 CFR 1910.1200(g)(2): "The chemical manufacturer or importer shall ensure that the
           safety data sheet is in English (although the employer may maintain copies in other
           languages as well), and includes at least the following section numbers and headings,
           and associated information under each heading, in the order listed"
    WHERE IN THE STANDARD
           reference/us-osha-hcs/29-cfr-1910-1200.md, paragraph (g)(2) and (g)(2)(i) to (xvi)
           revision: 29 CFR 1910.1200, eCFR point-in-time 2026-09-01
           confirmed current: 2026-09-11
    WHY    Every heading required by (g)(2)(i) to (xvi) is present and the order matches. The
           sheet numbers its sections "1." rather than "SECTION 1:", which the provision does not
           prescribe — it requires the section numbers and headings, and those are there.

### [P-02] [STANDARD] Subheadings with nothing to report are marked, not left blank

    WHAT   Where the sheet has nothing to report it says so rather than leaving the line empty:
           "Odor threshold  Not Determined" in Section 9, "Reasons for revision / No Information"
           in Section 16, and the same pattern through Sections 9 and 11.
    WHERE  Section 9 at rendering lines 307-345; Section 16 at lines 622-623
    RULE   29 CFR 1910.1200(g)(3): "If no relevant information is found for any sub-heading within
           a section on the safety data sheet, the chemical manufacturer, importer or employer
           preparing the safety data sheet shall mark it to indicate that no applicable
           information was found."
    WHERE IN THE STANDARD
           reference/us-osha-hcs/29-cfr-1910-1200.md, paragraph (g)(3)
           revision: 29 CFR 1910.1200, eCFR point-in-time 2026-09-01
           confirmed current: 2026-09-11
    WHY    This is the provision most often failed by an otherwise complete sheet, because a blank
           line and a line reading "not determined" look equally tidy and only one of them
           complies. This sheet marks them.

### [P-03] [STANDARD] The flash point is consistent with the flammability hazard declared

    WHAT   Section 9 states "Flash Point 89F (31C)". Section 2.1 classifies the mixture as
           "Flammable Liquid, category 3" and Section 16 carries H226, "Flammable liquid and
           vapour."
    WHERE  Section 9 at rendering line 318; Section 2.1 at lines 44-50; Section 16 at line 605
    RULE   29 CFR 1910.1200, Appendix B, B.6.1: "Flammable liquid means a liquid having a flash
           point of not more than 93 °C (199.4 °F)."
    WHERE IN THE STANDARD
           reference/us-osha-hcs/29-cfr-1910-1200.md, Appendix B, B.6.1
           revision: 29 CFR 1910.1200, eCFR point-in-time 2026-09-01
           confirmed current: 2026-09-11
    WHY    At 31 °C the liquid falls within the definition of a flammable liquid, so declaring a
           flammability hazard in Section 2 is consistent with the value in Section 9. **The
           category number was not checked.** B.6.2 assigns the four categories by reference to
           Table B.6.1, and that table is published as a graphic — it is not in `reference/` as
           text, so no provision here states what category 3 requires. See the blind spots.

---

## Noted, not a finding

**This sheet may lawfully follow the pre-2024 text of the standard, and does.** It declares
"Prepared in Accordance with HCS 29 C.F.R. 1910.1200" without naming a revision, and it was
revised on 2019-03-25, before the 2024 rewrite took effect on 2024-07-19.

§ 1910.1200(j)(4) provides that between 2024-05-20 and the applicable compliance date, preparers
"may comply with either this section or § 1910.1200 revised as of July 1, 2023, or both during the
transition period." For **mixtures** — and Carboguard 890 Part A is a mixture — § 1910.1200(j)(3)(i)
does not close that window until **2027-11-19**.

So the sheet sitting on the older text is not a failure today. It becomes one in fourteen months.
Reporting it as non-compliance now would be a false finding, which is exactly what
`reference/STANDARDS-LEDGER.md` exists to prevent.

## Declared blind spots

Stated on every report. Three of them bit on this run, and the first is the largest.

- **No classification was checked at all.** Under `jurisdiction: US` there is no harmonised
  classification list: 29 CFR 1910.1200 requires the preparer to classify, and does not publish a
  table saying what the answer must be. CLP Annex VI would give such a table, but it is EU law and
  does not govern this sheet, so Salus does not open it. Section 3's thirteen ingredients — among
  them titanium dioxide at 25–<50 % and crystalline silica at 10–<25 % — are recorded as
  **not assessed for classification correctness**. This is the single biggest difference between a
  US run and an EU one, and it is a limit of what is citable, not an oversight.
- **US per-subheading content is not citable.** Appendix D publishes Table D.1, the table of
  minimum SDS content, as a graphic. Nothing finer than (g)(2), (g)(3) and (g)(5) was checked.
- **Flammable-liquid categories are not citable either**, for the same reason — Table B.6.1 is a
  graphic. See [P-03].
- **Pictograms were not assessed.** Section 2.2 "Symbol(s) of Product" carries images, and images
  are not extractable text. Whether the right pictograms are present is outside what Salus sees.
- **Omissions are invisible.** If this coating contains a substance the supplier did not list,
  Salus cannot know.
- **No value was re-measured.** The flash point of 31 °C is checked for agreement with the rest of
  the sheet, not for truth.

## What this verdict is not

DOES NOT CONFORM is a statement about this document against this standard on this date. It is not a
statement about the coating, about whether anyone may work with it, or about what should happen
next. Those decisions belong to the specialists this report goes to.
