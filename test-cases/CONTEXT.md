# test-cases/ — the documents Salus is tested against

Two folders, and the line between them is the point. Nothing here is ever edited to make a run come
out a particular way: what a sheet says is the evidence a finding is checked against.

| Folder | What it holds | Its contract |
| --- | --- | --- |
| `sds/` | 22 safety data sheets exactly as their suppliers published them | `sds/CONTEXT.md` |
| `sds-constructed/` | 2 files altered here, to reach paths no real sheet in the corpus reaches | `sds-constructed/CONTEXT.md` |

## Why they are kept apart

A corpus of real documents stops being evidence the moment one altered file is mixed into it. A
reader checking a finding has to be able to tell, without asking anyone, whether the document in
front of them is what a supplier issued. The folder name is that answer, and it is the only form of
the answer that survives being copied, forwarded, or read six months from now.

## What a human checks before a file is added

- It is in the folder that matches what it is — issued by a supplier, or made here.
- That folder's `CONTEXT.md` gains a row naming the file, what it is, and why it is kept.
- If it cites a substance the Annex VI extract does not already cover, the extract is rebuilt in the
  same commit. `sds/CONTEXT.md` says how that set is chosen.
- **Nothing generated lives here.** A rendering and its fidelity report belong to the run that made
  them, under `audits/<run>/`. Running `tools/extract.py` or Gate 1 against a corpus sheet without
  `--outdir` will drop both beside the PDF; they are gitignored, and they still do not belong here.
