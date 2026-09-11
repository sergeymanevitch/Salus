# Standards ledger

Which revision of each standard is in force, and on what date this folder last confirmed it.

Salus is built to work with no network. That does not make it ignorant of the calendar — it makes
it carry the calendar. A standard is not a version number, it is a set of dates: published,
applies from, and the end of the window in which the previous revision may still lawfully be used.
A sheet compiled to a superseded revision **inside a live transition window is compliant**, and
calling that a failure would be a false finding.

Every date below is quoted from the shipped text of the standard itself, not from a secondary
source. The article or paragraph is named so a reader can open the file and check it.

---

## EU — Commission Regulation (EU) 2020/878

Replaces Annex II to Regulation (EC) No 1907/2006 (REACH), the annex that governs how a safety
data sheet must be compiled.

| Date | What it is | Where it is stated |
| --- | --- | --- |
| 2020-06-26 | published, OJ L 203/28 | header of `eu-2020-878/regulation-2020-878.md` |
| 2020-07-16 | enters into force (20th day after publication) | Article 3, first paragraph |
| 2021-01-01 | applies from | Article 3, second paragraph |
| 2022-12-31 | **end of transition** — until this date, sheets not complying with the new Annex II "may continue to be provided" | Article 2 |

**Consequence for an audit run after 2022-12-31.** A sheet that declares compliance with Annex II
*as amended by Regulation (EU) 2015/830* is compiled to a revision that can no longer lawfully be
supplied. This is a finding against Article 2, and it is a finding about the *sheet's declared
revision*, not about the chemistry.

Last confirmed current: **2026-09-11**, against
`http://publications.europa.eu/resource/celex/32020R0878`.

---

## EU — Regulation (EC) No 1272/2008 (CLP), Annex VI

The harmonised classification and labelling list. For a substance that appears in Annex VI
Table 3, the classification is set by law and is not the supplier's to choose.

| Date | What it is |
| --- | --- |
| 2026-07-01 | start of validity of the consolidated text shipped here (CELEX `02008R1272-20260701`) |

Annex VI is amended by ATP regulations several times a year. That is why this folder ships the
consolidated text rather than the 2008 original: citing the original would be citing rows that
have since been replaced.

This is not hypothetical. The first build of this folder shipped the consolidation of
2025-02-01, which was current when the work started. `tools/check_freshness.py`, run before
submission, reported three later consolidations — 2025-09-01, 2026-05-01 and 2026-07-01 — and the
reference layer was rebuilt against the last of them. The row this auditor cites most,
Index 649-465-00-7, is unchanged between the two; the point is that nobody knew that until the
check was run.

Last confirmed current: **2026-09-11**, against
`http://publications.europa.eu/resource/celex/02008R1272-20260701`. The check that matters is
whether a *later* consolidated version exists; if one does, the extract in
`eu-clp-annex-vi/annex-vi-table-3-extract.md` is stale and must be rebuilt before it is cited.

---

## US — 29 CFR 1910.1200 (Hazard Communication)

The 2024 revision aligned the standard with GHS Revision 7. Its own paragraph (j) sets the
calendar, and that calendar is still running.

| Date | What it is | Where it is stated |
| --- | --- | --- |
| 2024-05-20 | start of the transition window | § 1910.1200(j)(4) |
| 2024-07-19 | effective date of the revised section | § 1910.1200(j)(1) |
| 2026-05-19 | **substances** — manufacturers, importers and distributors must comply with all modified provisions | § 1910.1200(j)(2)(i) |
| 2027-11-19 | **mixtures** — the same obligation for mixtures | § 1910.1200(j)(3)(i) |

**Consequence for an audit run today.** Paragraph (j)(4) says that between 2024-05-20 and the
applicable date above, a preparer "may comply with either this section or § 1910.1200 revised as
of July 1, 2023, or both during the transition period." Most safety data sheets describe
**mixtures**. For a mixture, the window does not close until **2027-11-19**, so a US sheet that
follows the pre-2024 text is still lawful today and Salus must not report it as non-compliant.
Salus reports the fact and names the deadline.

Last confirmed current: **2026-09-11**, against the eCFR point-in-time snapshot for 2026-09-01.
The section carries amendments through 91 FR 6760 (2026-02-13).

---

## How to re-confirm

    python3 tools/check_freshness.py          # needs network; compares against the ledger
    python3 tools/build_reference.py          # re-downloads and regenerates reference/

`check_freshness.py` does not edit this file. It prints what it found and leaves the decision to
a person, because promoting a newly published revision into "in force" is a legal reading, not a
string comparison.
