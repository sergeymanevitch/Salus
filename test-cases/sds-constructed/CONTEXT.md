# Constructed fixtures

Two files, and neither is a safety data sheet as a supplier issued it. Both exist to exercise a
path the twenty-two real sheets do not reach. They are kept out of `test-cases/sds/` so nothing in
the corpus of real documents is contaminated by a file that was altered here.

| File | What it is | Why it exists |
| --- | --- | --- |
| `CONSTRUCTED - scanned sheet, no text layer.pdf` | pages 1–2 of `test-cases/sds/DEVCON - flexane-94l-resin-sds10494-en.pdf`, rasterised to an image and wrapped back into a PDF | to produce a sheet with no text layer, so the CANNOT VERIFY path has a real fixture instead of a description |
| `TRUNCATED - WEICON 116905, sections 5 to 16 removed.pdf` | pages 1–4 of a real, current WEICON sheet — Sections 1 to 4 only, out of a twenty-page document | to test the line between *unreadable* and *incomplete*. The pages that remain are perfectly legible, so this is **not** CANNOT VERIFY. Twelve of the sixteen sections are simply absent, which is a failure against the standard, and the auditor has to say the right one of those two things |

How it was made, so anyone can reproduce or discard it:

    python3 -c "import pypdf; r=pypdf.PdfReader(SRC); w=pypdf.PdfWriter(); \
                [w.add_page(p) for p in r.pages[:2]]; w.write('two.pdf')"
    sips -s format png two.pdf --out scan.png
    sips -s format pdf scan.png --out scanned.pdf

`pdftotext` returns one character from the result. That is the point: a scanned sheet is the
commonest thing a reviewer is handed that an auditor genuinely cannot read, and an auditor that
has never been shown one does not know it is supposed to stop.

## Why the truncated one matters

The two fixtures sit either side of a distinction that is easy to state and easy to get wrong under
pressure. CANNOT VERIFY means the auditor could not establish *what it was checking*. A sheet
missing twelve of its sixteen sections is not that: every word of it can be read, and what it says
is that twelve sections are gone. Calling that "cannot verify" would hide a real defect behind an
apology, and calling an unreadable scan a failure would invent one.

`audits/2026-09-11-weicon-truncated/` is the worked run.
