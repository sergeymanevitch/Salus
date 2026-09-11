# Constructed fixtures

One file, and it is **not** a manufacturer's safety data sheet. It is built here, on purpose, to
exercise a path the twenty-one real sheets do not reach.

| File | What it is | Why it exists |
| --- | --- | --- |
| `CONSTRUCTED - scanned sheet, no text layer.pdf` | pages 1–2 of `test-cases/sds/DEVCON - flexane-94l-resin-sds10494-en.pdf`, rasterised to an image and wrapped back into a PDF | to produce a sheet with no text layer, so the CANNOT VERIFY path has a real fixture instead of a description |

How it was made, so anyone can reproduce or discard it:

    python3 -c "import pypdf; r=pypdf.PdfReader(SRC); w=pypdf.PdfWriter(); \
                [w.add_page(p) for p in r.pages[:2]]; w.write('two.pdf')"
    sips -s format png two.pdf --out scan.png
    sips -s format pdf scan.png --out scanned.pdf

`pdftotext` returns one character from the result. That is the point: a scanned sheet is the
commonest thing a reviewer is handed that an auditor genuinely cannot read, and an auditor that
has never been shown one does not know it is supposed to stop.

It is kept apart from `test-cases/sds/` so nothing in the corpus of real sheets is contaminated by
a file this repository made up.
