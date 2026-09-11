# Salus audit report

| | |
| --- | --- |
| Sheet | `SDS_CHINA_English_TS+2024.pdf` — TS 2024, SDS No TS2024, Version 01, Nye Lubricants, Inc., A Member of the FUCHS Group |
| Jurisdiction (from `config/jurisdiction.md`) | EU |
| Standard applied | Commission Regulation (EU) 2020/878, with CLP Annex VI for classification |
| Run date | 2026-09-11 |
| Standards knowledge last confirmed online | 2026-09-11 — see `reference/STANDARDS-LEDGER.md` |
| Conversion gate | PASS — coverage 100.0000 %, the rendering reproduces the extraction byte for byte, and nothing the independent engine found is missing from it |

## VERDICT: DOES NOT CONFORM

Eleven findings, all against the standard; none against house policy. The sheet clears the house
age gate and five checks passed; both are listed below with the same weight, because a report that
shows only what broke cannot be argued with.

The findings are not eleven separate accidents. This document was compiled to the Chinese national
standards GB/T 16483 and GB/T 17519 and is audited here against Annex II because
`config/jurisdiction.md` says EU. Most of what follows is what that mismatch costs, provision by
provision. That is the useful answer: a sheet built to a different national standard does not
satisfy an EU obligation however well it is written for its own market.

Each finding names the provision and quotes it. Open the file named and disagree with any of them.

---

## Findings

### [F-01] [STANDARD] BLOCKING — the sheet is compiled to the Chinese national standards, not to Annex II

    WHAT   The first page, under the title, reads: "Prepared in accordance with GB/T 16483 and
           GB/T 17519." Section 15, under "Other regulations", reads: "This safety data sheet
           conforms to the following laws, regulations and standards:" and lists seven Chinese
           instruments, among them "Safety Data Sheet for Chemical Products - Content and Order
           of Sections (GB/T 16483-2008)". Every page footer reads "SDS CHINA". Neither
           Regulation (EC) No 1907/2006, nor Annex II, nor Regulation (EU) 2020/878 is named
           anywhere in the sixteen sections.
    WHERE  rendering line 2; Section 15 at lines 262-269; page footers at lines 62, 129, 191,
           256, 298 of SDS_CHINA_English_TS+2024.salus.md
    RULE   Regulation (EU) 2020/878, Article 1: "Annex II to Regulation (EC) No 1907/2006 is
           replaced by the text in the Annex to this Regulation."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Article 1
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    Article 1 makes the text annexed to 2020/878 the annex that governs how a safety data
           sheet is compiled for the Union market. This sheet was compiled to a different
           standard and says so on its own first page, so it has not been compiled to Annex II at
           all. The transition Article 2 opened for sheets not complying with that annex closed on
           31 December 2022; this sheet was issued on 30 June 2025, after it closed, so no
           transition question arises. Nothing here is a criticism of the document as a GB/T
           16483 sheet, which is not the standard configured for this installation and which
           Salus does not hold and cannot cite.

### [F-02] [STANDARD] BLOCKING — none of the Part B subsections appear, and one heading is blank

    WHAT   The sheet carries sixteen numbered sections and, under them, free-text labels of the
           supplier's own choosing: "Product Name", "Company name", "Emergency overview", "Label
           elements", "Substance/mixture", "Exposure limits", "Other data". No numbered subsection
           — 1.1, 1.2, 2.3, 3.1, 9.2, 14.6, 15.2 or any other — appears anywhere in the document.
           Section 1 carries the combined heading "Recommended use and Limitations on use"; under
           it, "Recommended use" reads "Lubricating Oil" and "Limitations on use" carries nothing
           at all.
    WHERE  Section 1 at rendering lines 13-29, the combined heading at line 27; Section 2 at lines
           31-50; Section 3 at lines 52-54; Section 15 at lines 235-281
    RULE   Regulation (EU) 2020/878, Annex II, Part A, subsection 0.4: "The information required
           by this Annex shall be included in the safety data sheet, where applicable and
           available, in the relevant subsections set out in Part B. The safety data sheet shall
           not contain blank subsections."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II Part A subsection 0.4
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    0.4 sets two obligations and this sheet meets neither. The first is that the
           information sit in the subsections Part B lists; the subsections are the addressing
           scheme the regulation uses, and a recipient who is told to look at 15.2 or 14.6 has
           nowhere in this document to look. The second is that no subsection be blank. The
           supplier's own combined heading names limitations on use and then leaves the field
           empty, which is the blank form 0.4 forbids, rather than the marked form the regulation
           expects. Salus does not raise the individual missing subsections as separate findings:
           they are absent because the addressing scheme is absent, and that is one defect, not
           twenty.

### [F-03] [STANDARD] BLOCKING — Section 3 gives no chemical identity of any kind

    WHAT   Section 3 reads, in its entirety: "Substance/mixture  Substance" and "The components
           are not hazardous or are below required disclosure limits." No chemical name, no CAS
           number, no EC number, no Index number, no REACH registration number and no product
           identifier appears in the section. The extraction found no chemical identifier anywhere
           in the document: `SDS_CHINA_English_TS+2024.fidelity.json` records identifiers 0.
    WHERE  rendering lines 52-54
    RULE   Regulation (EU) 2020/878, Annex II, subsection 3.1: "The chemical identity of the main
           constituent of the substance shall be provided by providing at least the product
           identifier or one of the other means of identification given in subsection 1.1."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II subsection 3.1
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    The sheet declares itself to cover a substance, so 3.1 is the subsection that governs,
           and 3.1 sets a floor: at least the product identifier, or one of the other means of
           identification from 1.1. Section 3 carries neither. It does not repeat the product
           identifier given in Section 1, and it offers no other means of identification in its
           place. This finding is about what the section contains, not about what the product
           contains: Salus does not know and does not say what is in this material, and the
           supplier's statement that its components fall below disclosure limits is not
           contradicted here. What is missing is the identification of the main constituent, which
           3.1 requires whether or not anything else is disclosed.

### [F-04] [STANDARD] MATERIAL — no PBT, vPvB or endocrine-disruptor determination anywhere in the sheet

    WHAT   Section 2 carries "Emergency overview", "GHS hazard categories", "Label elements",
           "Physical and chemical hazards", "Health hazards", "Environmental hazards" and
           "Supplemental information", which reads "None." The words persistent, bioaccumulative,
           PBT and vPvB appear nowhere in the sixteen sections. Section 12 mentions endocrine
           disruption once, inside a list of environmental effects: "No other adverse
           environmental effects (e.g. ozone depletion, photochemical ozone creation potential,
           endocrine disruption, global warming potential) are expected from this component."
    WHERE  Section 2 at rendering lines 31-50, "Supplemental information" at line 50; Section 12
           at lines 206-213, the environmental-effects list at lines 212-213
    RULE   Regulation (EU) 2020/878, Annex II, subsection 2.3: "Information shall be provided on
           whether the substance meets the criteria for persistent, bioaccumulative and toxic or
           very persistent and very bioaccumulative in accordance with Annex XIII, whether the
           substance was included in the list established in accordance with Article 59(1) for
           having endocrine disrupting properties"
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II subsection 2.3
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    2.3 requires a determination against named criteria, and the obligation does not lift
           when the answer is negative — a stated negative is the disclosure. None of the three
           limbs is addressed: no Annex XIII assessment, no statement about the Article 59(1)
           list, nothing under the 2017/2100 or 2018/605 criteria. The one mention of endocrine
           disruption sits in Section 12 among general environmental effects and is not an
           assessment against the Article 59(1) list, so it does not supply what 2.3 asks for.
           The supplier's "None." under Supplemental information is the nearest thing in
           Section 2 to a statement of other hazards, and it names no criterion.

### [F-05] [STANDARD] MATERIAL — Section 2 puts a general reassurance where the hazards belong

    WHAT   Section 2, under the heading "Physical and chemical hazards", reads: "The product is
           stable and non-reactive under normal conditions of use, storage and transport. No
           unusual fire or explosion hazards noted." Under "Health hazards" it reads: "Expected to
           be a low ingestion hazard. Direct contact with eyes may cause temporary irritation."
           Section 2 also declares "Not classified." under GHS hazard categories.
    WHERE  rendering lines 34, 45-46 and 47
    RULE   Regulation (EU) 2020/878, Annex II, Part A, subsection 0.2.4: "any other statements
           indicating that the substance or mixture is not hazardous or any other statements that
           are inconsistent with the classification of that substance or mixture shall not be
           used."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II Part A subsection 0.2.4
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    0.2.4 names the forbidden form by example and then closes the list with any other
           statement indicating that the substance is not hazardous. The sentence about stability
           and non-reactivity under normal conditions of use is of that form, and it stands in
           Section 2 in the place where the physical and chemical hazards belong. The finding does
           not turn on whether the sentence is true. The provision bars the construction itself,
           because a general reassurance offered instead of a hazard statement is not something a
           reader can check against Sections 9 to 12, and Section 10 already carries the same
           sentence where it does belong. The same reasoning reaches the ingestion sentence, which
           grades a hazard downward in a section that has declared no classification.

### [F-06] [STANDARD] MATERIAL — the sheet declares a substance in Section 3 and refers to several components everywhere else

    WHAT   Section 3 reads "Substance/mixture  Substance", and in the next line "The components
           are not hazardous or are below required disclosure limits." Section 8 reads "No
           exposure limits noted for ingredient(s)." Section 11 reads "No data available to
           indicate product or any components present at greater than 0.1% are mutagenic or
           genotoxic." Section 15 reads "One or more components of the product are not listed but
           have been notified or registered by the importer."
    WHERE  rendering lines 53-54, 110, 189-190 and 249-251
    RULE   Regulation (EU) 2020/878, Annex II, Part B: "The safety data sheet shall include the
           following 16 headings in accordance with Article 31(6) and in addition the subheadings
           also listed except section 3, where only subsection 3.1 or subsection 3.2 needs to be
           included as appropriate:"
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II Part B
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    Part B makes the substance-or-mixture question determinative of which subsection of
           Section 3 the sheet must carry, and therefore of what the sheet must disclose. This
           document answers the question one way in Section 3 and the other way in four places
           across Sections 3, 8, 11 and 15, which speak of components and ingredients in the
           plural. Salus does not pick a winner and has no basis to: whether this product is a
           substance or a mixture is a fact about the material, and only the supplier knows it.
           The finding is that the sheet does not let a reader determine which, and so does not
           let a reader determine whether 3.1 or 3.2 was the obligation it was trying to meet.

### [F-07] [STANDARD] MATERIAL — Section 15 carries no Union provisions

    WHAT   Section 15 lists the Law of the People's Republic of China on Prevention and Control of
           Occupational Diseases, the Regulations on the Control over Safety of Dangerous
           Chemicals, the Provision on the Environmental Administration of New Chemical
           Substances, the China Inventory of Existing Chemical Substances, seven further Chinese
           laws and standards under "Other regulations", and five international conventions, each
           marked "Not applicable." No Union instrument is named. REACH Title VII authorisations
           and Title VIII restrictions are not mentioned, and no national regulatory status for
           any Member State is given.
    WHERE  Section 15 at rendering lines 235-281
    RULE   Regulation (EU) 2020/878, Annex II, subsection 15.1: "Information shall be provided
           regarding relevant Union safety, health and environmental provisions"
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II subsection 15.1
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    15.1 asks for the Union provisions relevant to the substance or mixture, and this
           section answers for a different jurisdiction throughout. The Chinese content is not a
           defect in itself — 15.1 also provides for national regulatory status — but it is
           offered here in place of the Union layer rather than alongside it, and the Union layer
           is absent. A recipient in a Member State cannot learn from this section whether any
           Union provision attaches, which is the question 15.1 exists to answer.

### [F-08] [STANDARD] MATERIAL — Section 15 does not say whether a chemical safety assessment was carried out

    WHAT   Section 15 carries the Chinese regulatory content described in [F-07], an inventory
           table, a SPECIAL CASE note about import, a list of other regulations and a list of five
           international conventions. It contains no statement about a chemical safety assessment,
           and the phrase appears nowhere in the sixteen sections.
    WHERE  Section 15 at rendering lines 235-281
    RULE   Regulation (EU) 2020/878, Annex II, subsection 15.2: "This subsection of the safety
           data sheet shall indicate whether the supplier has carried out a chemical safety
           assessment for the substance or the mixture."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II subsection 15.2
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    15.2 asks a yes-or-no question and requires the answer on the page. Either answer
           discharges it; silence does not. This is a separate obligation from 15.1 and is not
           met by the Chinese regulatory content, which addresses a different question entirely.

### [F-09] [STANDARD] MATERIAL — Section 14 answers for air and sea but is silent on road, rail and inland waterways

    WHAT   Section 14 carries three entries — "CNDG", "IATA" and "IMDG" — each reading "Not
           regulated as dangerous goods.", followed by "Transport in bulk according to Annex II of
           MARPOL 73/78 and the IBC Code" reading "Not established." ADR, RID and ADN are not
           named, and no statement appears that road, rail or inland-waterway information is
           unavailable or not relevant.
    WHERE  Section 14 at rendering lines 224-233
    RULE   Regulation (EU) 2020/878, Annex II, section 14: "This section of the safety data sheet
           shall provide basic classification information for the transport/shipment of substances
           or mixtures mentioned in section 1 by road, rail, sea, inland waterways or air. Where
           such information is not available or relevant this shall be stated."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II section 14
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    The provision lists five modes and gives the supplier two lawful answers for each:
           the classification information, or a statement that it is unavailable or not relevant.
           Sea and air are answered through IMDG and IATA. CNDG is the Chinese national dangerous
           goods scheme and is not the road, rail or inland-waterway instrument that applies in
           the Union; the second paragraph of the same section names ADR, RID and ADN as those
           instruments. For those three modes the sheet gives neither answer the provision allows.

### [F-10] [STANDARD] MATERIAL — Section 9 records flammability as not applicable to a liquid

    WHAT   Section 9 states "Physical state  Liquid.", "Form  Liquid." and "Appearance  Clear.",
           and eighteen lines further down states "Flammability (solid, gas)  Not applicable."
           The heading itself restricts the property to solids and gases. A flash point is given
           separately as "572.0 °F (300.0 °C)".
    WHERE  rendering lines 140-142, 149 and 162
    RULE   Regulation (EU) 2020/878, Annex II, Part A, subsection 9.1, point (f) Flammability:
           "Applies to gases, liquids and solids. It shall be indicated whether the substance or
           mixture is ignitable, i.e. capable of catching fire or being set on fire, even if not
           classified for flammability."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II Part A subsection 9.1 point (f)
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    The sheet's own Section 9 puts this product in the liquid state twice, and point (f)
           states in its first sentence that the property applies to liquids. Both the heading and
           the entry therefore record that a property does not apply in a case where the provision
           says it does, and the indication the point actually calls for — whether the product is
           ignitable — is absent. The provision anticipates this sheet's situation exactly: it
           requires that indication even where there is no flammability classification, and this
           product carries none. The flash point thirteen lines above is a different characteristic
           under point (h) and does not supply it.

### [F-11] [STANDARD] MINOR — acronyms used without expansion, and no key or legend anywhere

    WHAT   The sheet uses "CNDG" in Section 14, "IECSC" in Section 15, "TRGS 510" in Section 7 and
           "cSt" in Section 9, none of them expanded at the point of use or anywhere else.
           Section 16 contains two entries, "References" and "Disclaimer", and no key or legend to
           the abbreviations used in the document.
    WHERE  rendering lines 105-106, 165, 225, 241-244; Section 16 at lines 282-293
    RULE   Regulation (EU) 2020/878, Annex II, Part A, subsection 0.2.4: "The language used in the
           safety data sheet shall be simple, clear and precise, avoiding jargon, acronyms and
           abbreviations."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II Part A subsection 0.2.4
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    0.2.4 is addressed to a reader who has to act on the sheet quickly. IATA and IMDG are
           named in Annex II itself and pass without expansion; CNDG and IECSC are not, and
           TRGS 510 is a German technical rule cited without its title in a document prepared for
           the Chinese market. Section 16 is where Annex II expects a key to abbreviations to sit,
           and it carries none, so the expansion is available nowhere in the sheet. Graded MINOR:
           it is a formal defect, and every one of these terms is resolvable by a specialist.

---

## What passed

### [P-01] [STANDARD] All sixteen sections present, numbered, in order, and carrying content

    WHAT   Sections 1 to 16 appear once each, in ascending order, under headings that match the
           Annex II wording closely: Chemical product and company identification; Hazards
           identification; Composition/information on ingredients; First aid measures;
           Fire-fighting measures; Accidental release measures; Handling and storage; Exposure
           controls/personal protection; Physical and chemical properties; Stability and
           reactivity; Toxicological information; Ecological information; Disposal considerations;
           Transport information; Regulatory information; Other information. No section is empty
           and none is missing.
    WHERE  rendering lines 13, 31, 52, 56, 74, 84, 101, 108, 139, 169, 179, 206, 215, 224, 235, 282
    RULE   Regulation (EU) 2020/878, Annex II, Part B: "The safety data sheet shall include the
           following 16 headings in accordance with Article 31(6) and in addition the subheadings
           also listed except section 3, where only subsection 3.1 or subsection 3.2 needs to be
           included as appropriate:"
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II Part B
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    Part B sets two requirements and this is the one the sheet meets. The sixteen headings
           are the Part B sixteen, in the Part B order, each with content under it. The other
           requirement in the same sentence — the subheadings — is [F-02], and the two are
           reported separately because they are separately true.

### [P-02] [STANDARD] Every page numbered, with the length of the document on it

    WHAT   Each of the five pages carries a footer reading "SDS CHINA" above a page indication:
           1/5, 2/5, 3/5, 4/5 and 5/5. Each page also repeats the product name and the SDS number
           in a running header.
    WHERE  rendering lines 62-64, 129-131, 191-193, 256-258, 298-299
    RULE   Regulation (EU) 2020/878, Annex II, Part A, subsection 0.3.2: "All pages of a safety
           data sheet, including any annexes, shall be numbered and shall bear either an
           indication of the length of the safety data sheet"
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II Part A subsection 0.3.2
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    0.3.2 lets a reader confirm they are holding the whole document. The n/5 form gives
           both the number and the length in one mark, which is the first of the two options the
           subsection offers, and it is on every page. This is also the evidence that nothing was
           truncated in the copy Salus read: the pagination runs 1/5 to 5/5 with no gap.

### [P-03] [STANDARD] The date of compilation is on the first page

    WHAT   The first page carries "Issue date: June-30-2025" in the header block and "Version #:
           01" immediately below it. Section 1 repeats "Issue date  June-30-2025". No revision
           date and no superseded version appear, and the version number is 01.
    WHERE  rendering lines 6-7 and line 29
    RULE   Regulation (EU) 2020/878, Annex II, Part A, subsection 0.2.5: "The date of compilation
           of the safety data sheet shall be given on the first page."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II Part A subsection 0.2.5
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    The first obligation in 0.2.5 is met: the date is on page one, and Section 1 repeats
           it. The rest of 0.2.5 governs revised sheets — a revision date, an indication of the
           version replaced, and the changes brought to the recipient's attention in Section 16.
           Version 01 with no superseded version named is a first issue on its own evidence, so
           that limb does not attach and no finding is raised under it.

### [P-04] [STANDARD] Section 1.4 gives an emergency number, not a placeholder

    WHAT   Section 1 carries "Emergency telephone number  +86 4001 2001 74" and, on the next line,
           "Access code  334212". A company telephone number "+1 508 996 6721", an address in
           Fairhaven, Massachusetts, an e-mail address and a website are given separately.
    WHERE  rendering lines 18-26
    RULE   Regulation (EU) 2020/878, Annex II, subsection 1.4: "References to emergency
           information services shall be provided."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II subsection 1.4
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    Stage 6 of `rules.md` tests that the emergency contact is present and is a number
           rather than a placeholder. It is both, and the access code beside it is the kind of
           access condition 1.4 expects to be stated rather than left to be discovered on the
           call. What Salus does not test is whether a Chinese service number discharges 1.4 for
           a Member State — see Noted, not a finding.

### [P-05] [STANDARD] The flash point is stated once, and nothing in the sheet contradicts it

    WHAT   Section 9 gives "Flash point  572.0 °F (300.0 °C)". The value appears nowhere else in
           the sheet and no other flash point is stated. Section 2 declares no flammability
           classification, Section 5 states "No unusual fire or explosion hazards noted." and
           Section 7 assigns "Storage class (TRGS 510): 10 (Combustible liquids that cannot be
           assigned to any of the above storage classes)".
    WHERE  rendering lines 34, 81, 105-106 and 149
    RULE   Regulation (EU) 2020/878, Annex II, Part A, subsection 9.1, point (h) Flash point:
           "Does not apply to gases, aerosols and solids. For mixtures, a value for the mixture
           shall be indicated, if available."
    WHERE IN THE STANDARD
           reference/eu-2020-878/regulation-2020-878.md, Annex II Part A subsection 9.1 point (h)
           revision: Commission Regulation (EU) 2020/878
           confirmed current: 2026-09-11
    WHY    Point (h) applies here because the product is a liquid, and a single value is given, so
           the second sentence is satisfied on its face. Stage 6 checks that the same fact told
           twice is told the same way; this fact is told once, and the three places in the sheet
           that touch on fire behaviour are consistent with it and with each other. The TRGS 510
           storage class is a combustible-liquid class that on its own terms covers liquids not
           assignable elsewhere, and it does not contradict the absence of a flammability
           classification at 300 °C. Salus does not re-measure the value and does not know whether
           300 °C is the true flash point of this product.

---

## Noted, not a finding

**The sheet clears the house age gate.** Issue date 30 June 2025, run date 2026-09-11 — one year
and two months. `config/jurisdiction.md` sets `policy_max_age_years: 5`. No policy finding arises
on this run, and none is recorded. Every finding above is `[STANDARD]`.

**Section 8 states that no exposure limits were noted.** Subsection 8.1.1 requires national limit
values to be listed "Where available". Whether a limit value exists for this product's constituents
is a fact about the substances, which this sheet does not name, so Salus cannot test the condition
the obligation hangs on. The statement is present rather than the field being blank, and no finding
is raised.

**Section 9 gives no reasons for its "Not available" entries.** Fifteen properties — colour, odour,
pH, melting point, boiling point, explosive limits, vapour pressure, vapour density, relative
density, water solubility, partition coefficient, auto-ignition temperature and decomposition
temperature — are marked "Not available" with no reason. Subsection 9.1 requires an absence to be
clearly indicated, giving the reasons where possible. It is clearly indicated. Whether giving a
reason was possible is a fact about the supplier's data rather than about this document, so the
condition cannot be tested here. Recorded because a reviewer writing to the supplier may want to
ask.

**The emergency number is a Chinese service number and no Member State body is named.**
Subsection 1.4 provides that where an official advisory body exists in the Member State where the
product is placed on the market, its number shall be given and can suffice. Which Member State, if
any, this sheet serves is not stated in the document and is a judgement about the market rather
than a test Salus can run on the page. Not raised; it belongs in the same conversation with the
supplier as [F-01].

**Section 9 states temperatures in Fahrenheit first and viscosity in centistokes.** Subsection 0.6
requires the units of Council Directive 80/181/EEC. That directive is not shipped in `reference/`,
so Salus has no text to cite and does not raise it. The SI values are given in parentheses
alongside in both cases.

**Section 16 carries no classification method and no training advice.** Points (d) and (f) of
Annex II section 16 name both. The list they sit in is introduced by "such as" rather than by a
"shall" attaching to each item, so Salus does not raise them as breaches. Point (b) of the same
list, the key to abbreviations, is reached at [F-11], and only because subsection 0.2.4 states the
underlying obligation independently, in mandatory terms.

## Declared blind spots

- **Omissions are invisible.** Section 3 names no substance. Salus cannot know whether a substance
  meeting the 3.2.1 or 3.2.2 criteria was left out, whether a hazard went undeclared, or what is in
  this product. Nothing above is a statement about the material.
- **No classification was checked against CLP Annex VI on this run.** Stage 5 looks up each
  ingredient row by CAS or Index number. Section 3 supplies no identifier of any kind and the
  extraction found none anywhere in the document, so no lookup was performed and no harmonised
  entry was compared. This is not the same as finding the classification correct. [F-03] is about
  the missing identity, not about a classification Salus tested and rejected.
- **Self-classification is not checked.** The sheet's "Not classified." rests on the supplier's own
  evaluation. No shipped provision says what correct would be here, so it is recorded, not tested.
- **The Chinese standards this sheet was compiled to are not held and not cited.** GB/T 16483 and
  GB/T 17519 are not in `reference/`. Salus says only that this sheet is not an Annex II sheet. It
  makes no claim, in either direction, about whether it is a good GB/T 16483 sheet.
- **No value was re-measured.** The flash point of 300 °C, the density of 0.84 g/cm3 and the
  kinematic viscosity of 108 cSt at 40 °C are checked for agreement with the rest of the sheet, not
  for truth.
- **Sections 4 to 8 and 10 to 13 were checked for presence, for content, and for the consistency
  listed in `rules.md` Stage 6 — not clause by clause.** A finding absent from this report is not a
  clause proved met, and with the Part B addressing scheme absent ([F-02]) a clause-by-clause map
  of this document onto Annex II was not available to build one from.
- **The sheet, not the shipment.** Whether Version 01 of 30 June 2025 is the version that travelled
  with the container in the warehouse is outside this document.
- **US per-subheading content is not citable** — not applicable to this run, which is EU.

## What this verdict is not

DOES NOT CONFORM is a statement about a document and about nothing else. It is not a statement
about the lubricating oil, and no part of this report is. What the eleven findings need is a sheet
compiled to Annex II from the supplier; what the material needs, if anything, is decided by the
specialists this report goes to, under whatever regulations and internal rules their organisation
carries.
