# test-cases/sds/ — twenty-one real safety data sheets

These are not samples written for this repository. They are the documents suppliers publish for
their products, collected in the course of real review work, and they are here because a finding
nobody can open the source of is not checkable.

| | |
| --- | --- |
| Count | 21 |
| Suppliers | Chesterton (4), BG (2), Carboline (2), Dowsil (2), Jotun (2), Atlas Copco, Castrol, Chevron, CRC, Devcon, Jet-Lube, Loctite, RD Coatings, Weicon |
| Regimes | EU and UK-format sheets, US `USANSI` sheets, and one built for an Israeli REACH variant |
| Revisions declared | 2015/830, 2020/878, 1907/2006 alone, 29 CFR 1910.1200, and some declaring nothing at all |
| Issue dates | 2015 to 2026 — some already past the five-year house gate, one twelve days short of it |

## Why this particular set

It is a working set, not a curated one, and the awkwardness is the point:

- sheets on a **superseded** revision sit beside sheets on the current one, which is what makes the
  transition-window rule in `rules.md` Stage 3 something other than theory;
- one sheet is **AES-encrypted** and the independent extraction engine cannot open it without the
  `cryptography` package — so the conversion gate returns UNCONFIRMED rather than a verdict;
- filenames carry the currency sign as a separator and trademark symbols, which breaks naive path
  handling, and did;
- several are named **MSDS** rather than SDS, the older term.

The rows in `reference/eu-clp-annex-vi/annex-vi-table-3-extract.md` are selected by the identifiers
**these** sheets cite — the count is in that file's own header, where it is generated rather than
copied. Audit a sheet from outside this set and the extract has to be
rebuilt for it.

## On redistribution

A safety data sheet is a document a supplier is obliged to make available to anyone handling the
product; these were obtained that way and each names its supplier, product and revision date on its
own first page. They are included as evidence, unmodified, so that every finding in `audits/` and
`examples.md` can be checked against the document it describes. Nothing here has been edited. If a
supplier objects to their sheet appearing in a public repository, remove the file and rebuild the
Annex VI extract — nothing else depends on it.

The one file in `test-cases/sds-constructed/` is **not** from a supplier. It was made here, and its
folder says exactly how.
