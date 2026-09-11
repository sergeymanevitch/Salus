# Worked audits

Five runs: both jurisdictions, all three verdicts, and the two edges where a verdict is easy to get
wrong. Every one is a real run against the standards in `reference/`, and each is shipped in full
under `audits/` with the rendering the auditor read and the fidelity report for that rendering, so
any finding here can be opened and disagreed with.

| Run | Regime | Verdict | Why it is here |
| --- | --- | --- | --- |
| BG HCF | EU | DOES NOT CONFORM | how a finding cites a provision |
| DOWSIL AP | EU | CONFORMS | an audit reports what held, not only what broke |
| Carboguard 890 | **US** | DOES NOT CONFORM | the US path, and how much smaller it is |
| WEICON truncated | EU | DOES NOT CONFORM | incomplete is not the same as unreadable |
| scanned fixture | — | CANNOT VERIFY | what the auditor does when it cannot read |

The findings are abridged below. The full reports carry every citation.

---

## 1. DOES NOT CONFORM — `BG - HCF MSDS 510231_UK_EN.pdf`

A grease sheet from BG Products, UK version, issued April 2019. Four findings, two passes.
Full report: `audits/2026-09-11-bg-hcf/report.md`.

**[F-01] Compiled to a revision that may no longer be supplied.** Every page of the sheet declares
*"as amended by Commission Regulation (EU) 2015/830"*. That is the revision 2020/878 replaced, and
Article 2 of 2020/878 let non-complying sheets be supplied only *"until 31 December 2022"*. The run
date is 2026-09-11.

> This finding exists only because the auditor checked the calendar rather than the version number.
> A sheet on an older revision **inside** a live transition window is compliant, and reporting that
> as a failure would be a false finding. `reference/STANDARDS-LEDGER.md` holds the dates; the
> report cites the article that closes the window, not a rule of thumb.

**[F-02] Two base oils depart from their harmonised classification with no basis stated.** Section 3
lists CAS 64742-52-5 (Index 649-465-00-7) and CAS 64742-54-7 (Index 649-467-00-8), each at
25–50 %, each classified `Asp. Tox. 1, H304`. CLP Annex VI Table 3 classifies both as **Carc. 1B,
H350**, with Note L.

Note L is a conditional release, and the condition has to be shown:

> *"The harmonised classification as a carcinogen applies unless it can be shown that the substance
> contains less than 3 % of dimethyl sulphoxide extract as measured by IP 346"*

The sheet neither carries the harmonised classification nor records that the Note L condition was
met. **The finding is the missing basis, not the choice of hazard code** — a supplier relying on
Note L is not in breach, but a reader has to be able to tell that is what happened.

This is the shape of finding the whole design is built for. "This hazard code looks wrong" is an
opinion. "Annex VI row 649-465-00-7 says Carc. 1B / H350 / Note L, and here is the row" is an audit.

**[F-03] Section 11 contradicts Section 3.** Section 11 reads *"Carcinogenicity : No known
significant effects or critical hazards."* while Section 3 lists two Annex VI category 1B
carcinogens at 25–50 % each. Salus reports that the sheet does not let a reader determine which is
correct. It does not pick a winner — choosing one would be a statement about the material.

**[F-04] `[HOUSE POLICY — no provision]` The sheet is seven years old.** Issued 2019-04-16. Neither
standard sets an expiry, so this finding carries **no citation and says so**, in both the RULE line
and the WHERE IN THE STANDARD line. It is marked differently from the three above because a reader
has to be able to tell at a glance which findings the law requires and which this installation does.

**What passed, and why it is in the report.** `[P-01]` the antimony compounds row matches Annex VI
Index 051-003-00-9 exactly — found by Index number, because that group entry carries no CAS of its
own. `[P-02]` Section 9's flash point of 235 °C is consistent with Section 2 declaring no
flammability hazard.

---

## 2. CONFORMS — `DOWSIL™ AP Silicone Adhesive Sealant White - DE(EN).pdf`

A silicone sealant sheet from Dow Deutschland, revised September 2021. Six checks, all passed.
Full report: `audits/2026-09-11-dowsil-ap/report.md`.

- **[P-01]** declares *"according to Reg. (EU) 2020/878"* and was revised after that regulation
  began to apply — Article 3, *"It shall apply from 1 January 2021."*
- **[P-03]** D4 (CAS 556-67-2, Index 014-018-00-1) matches its harmonised row exactly: Repr. 2 /
  H361f, Aquatic Chronic 1 / H410, M = 10. The sheet **additionally** declares Flam. Liq. 3 / H226,
  which the harmonised entry does not cover — classifying more strictly than the harmonised minimum
  is the supplier's to do, so it is not a divergence.
- **[P-04]** titanium dioxide and the stannane have no harmonised entry, so their classification is
  the supplier's own. Salus records what the standard does require — identifier, concentration
  range, classification — as present, and records that it **cannot check whether the
  classifications are right.** That limit is written into the report, not left implied.
- **[P-05]** D4 and D6 are above the 0,1 % threshold at which Annex II subsection 2.3 requires
  PBT/vPvB disclosure, and both are disclosed by name.

**Noted, not a finding: the sheet clears the five-year house gate by twelve days.** Revised
2021-09-23, audited 2026-09-11. Recorded because the reviewer who opens this sheet in October will
be looking at one that no longer clears it, and no provision would have told them so.

> CONFORMS covers the six checks listed. It is not a release, not a clearance, and says nothing
> about the sealant. The report says that in its own last section.

---

## 3. CANNOT VERIFY — `CONSTRUCTED - scanned sheet, no text layer.pdf`

Full report: `audits/2026-09-11-scanned-fixture/report.md`.

The file opens, renders two pages, and both are images. `pdftotext` returns one character from the
whole document; the independent engine returns none. The audit stops at Stage 1 and **no provision
is applied.**

The report says what would change the answer — the original PDF, or an OCR layer, with the caveat
that an OCR layer is a transcription and an audit of a transcription is a weaker claim that would
be recorded as such.

> **This fixture is constructed, and the repository says so loudly.** It is pages 1–2 of a real
> Devcon sheet, rasterised and wrapped back into a PDF; the exact commands are in
> `test-cases/sds-constructed/README.md`. All twenty-one real sheets carry a text layer, so none of
> them reaches this path — and an auditor that has never been shown an unreadable sheet does not
> know it is supposed to stop.

---

## 4. DOES NOT CONFORM, on the US path — `CARBOLINE - Carboguard_890 - 0986A1NL_2_USANSI.pdf`

A coating sheet prepared under HCS 29 CFR 1910.1200, revised March 2019. Two findings, three
passes. Full report: `audits/2026-09-11-carboguard-us/report.md`.

**[F-01] Section 16 carries no date of preparation or last revision.** The date exists — *"Revision
Date: 03/25/2019"* — but in the running page header, not in the section the standard sends a reader
to. § 1910.1200(g)(2)(xvi) names it as content *of section 16*.

**[P-02] Subheadings with nothing to report are marked rather than left blank** — *"Odor threshold
Not Determined"*, *"Reasons for revision / No Information"*. This is § 1910.1200(g)(3), and it is
the provision an otherwise complete sheet most often fails, because a blank line and a line reading
"not determined" look equally tidy and only one of them complies.

**Noted, not a finding: the sheet may lawfully follow the pre-2024 text, and does.** Revised before
the 2024 rewrite took effect. § 1910.1200(j)(4) allows either text during the transition, and for
**mixtures** § 1910.1200(j)(3)(i) does not close the window until **2027-11-19**. Reporting this as
non-compliance today would be a false finding. It becomes a real one in fourteen months.

> **The US run is a much smaller audit, and the report says so out loud.** There is no harmonised
> classification list in 1910.1200 — the standard requires the preparer to classify and does not
> publish a table of correct answers. CLP Annex VI would give one, but it is EU law and does not
> govern this sheet, so Salus does not open it. Thirteen ingredients, including titanium dioxide at
> 25–<50 %, are recorded as **not assessed for classification correctness**. Two further limits bite
> here too: Appendix D's Table D.1 and Appendix B's Table B.6.1 are both published as *graphics*, so
> per-subheading content and flammable-liquid categories are not citable at all. [P-03] checks the
> flash point against the definition of a flammable liquid and states plainly that it could not
> check the category number.

## 5. DOES NOT CONFORM, not CANNOT VERIFY — `TRUNCATED - WEICON 116905`

Pages 1–4 of a real, current twenty-page WEICON sheet. Sections 1 to 4 only.
Full report: `audits/2026-09-11-weicon-truncated/report.md`.

This fixture exists to test one line that is easy to state and easy to get wrong under pressure.
Every word of the four pages is legible; the conversion gate passed it with one divergent token and
no lost identifier. Salus could establish exactly what it was looking at — and it was a document
missing three quarters of itself.

**That is a failure, not an inability.** `CANNOT VERIFY` would have been the comfortable answer, and
it would have filed a real defect under *the auditor had a problem*, which is how a defect gets
lost. Compare run 3 above, where nothing could be read at all and no provision was applied.

**[F-01]** twelve of the sixteen sections are absent, against *"The safety data sheet shall include
the following 16 headings"* — among them Section 8 exposure controls and Section 9 physical
properties, the two a person handling the product reaches for first.

**[F-02] The document convicts itself.** Every footer reads `1/20`, `2/20`, `3/20`, `4/20`. The
sheet states that it is twenty pages long and four are present — and subsection 0.3.2 requires that
pagination *precisely so that an incomplete copy can be recognised as one*. A reader can check it in
four seconds knowing nothing about the product.

**[P-01]** is worth reading beside run 1: this sheet names the current revision, is seven months
old, and clears every calendar check. What is wrong with it has nothing to do with age or revision.

---

## What these five are meant to teach

0. **Jurisdiction changes what can be checked, not how hard it is checked.** Run 4 makes fewer
   claims than run 1 because 1910.1200 publishes less that can be cited — and it says which claims
   it is not making, and why, rather than reaching for an EU table that does not govern the sheet.
1. **A finding names a provision, a revision, and a date.** Not one of the three is decoration.
   `[F-01]` turns on a date in an article; `[F-02]` turns on a row and a note in a revision that
   was rebuilt the day this was written; every citation says when it was last confirmed current.
2. **A pass is part of the report.** Four of the five runs list what was checked and held. An audit
   that only lists breakage is a complaint.
3. **The auditor's limits go in the report, not in the small print.** Every one of the five
   declares its blind spots, including on the runs where they did not bite.
4. **Three verdicts and no fourth.** There is no score, no percentage, and nothing that could be
   read as permission to use a material. `tools/validate_report.py` enforces that over the text
   after the fact; see `README.md`.
