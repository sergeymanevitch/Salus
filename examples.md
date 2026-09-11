# Worked audits

Three sheets, three verdicts, one of each. Every one is a real run against the standards in
`reference/`, and each is shipped in full under `audits/` with the rendering the auditor read and
the fidelity report for that rendering, so any finding here can be opened and disagreed with.

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

## What these three are meant to teach

1. **A finding names a provision, a revision, and a date.** Not one of the three is decoration.
   `[F-01]` turns on a date in an article; `[F-02]` turns on a row and a note in a revision that
   was rebuilt the day this was written; every citation says when it was last confirmed current.
2. **A pass is part of the report.** Two of the three runs list what was checked and held. An audit
   that only lists breakage is a complaint.
3. **The auditor's limits go in the report, not in the small print.** Every one of the three
   declares its blind spots, including on the run where they did not bite.
4. **Three verdicts and no fourth.** There is no score, no percentage, and nothing that could be
   read as permission to use a material. `tools/validate_report.py` enforces that over the text
   after the fact; see `README.md`.
