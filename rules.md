# How Salus audits

One pass, seven stages, in this order. Later stages depend on earlier ones: you cannot check a
provision until you know which revision of the standard applies, and you cannot know that until
you have read the sheet's own header. Do not reorder them.

Stop conditions are named at each stage. When a stage says stop, stop — do not "check the rest
anyway." A verdict reached on a document you could not read is worse than no verdict.

**If you have no shell** — you are a Claude project, or any AI tool without a terminal — the stages
still run, and you must not pretend otherwise in either direction:

- **Stage 1a cannot be performed.** Read the sheet as supplied and **record in the report that the
  rendering was not verified**. That is a fact about the audit and belongs in it.
- **Stage 1b is performed by eye.** Read the first page and Section 15 for the standard the sheet
  declares. If it is not one this folder ships, stop — the verdict is CANNOT VERIFY, out of scope.
- **Stage 2's arithmetic is yours.** `tools/check_age.py` is not available to you.
- **Stages 3 to 6 are unchanged.** They are reading, and reading is what you do.
- **The report gates run later, on a terminal, over the finished report.** A report you write here
  has not passed them, and the section *Before the report leaves* is not satisfied. Say so in the
  report rather than claiming a check nobody made — and `README.md` § *Where it runs* is the
  honest account of what that costs.

---

## Stage 0 — Settings

Read `config/jurisdiction.md`. It names the regime this installation audits under: `EU` or `US`,
the house age gate (`policy_max_age_years`), and the day the run speaks for (`run_date`).

- `python3 tools/read_config.py` says what all four settings resolve to, and fails by name on one
  that cannot be honoured as written. It is the only script that parses that file; the scope gate
  and Gate 3 both ask it rather than reading the file themselves.
- Not filled in → **CANNOT VERIFY**, reason: jurisdiction not configured. Stop.
- The report records the run date and, where a house-policy finding is made, the threshold it
  rests on. Gate 3 refuses a report that carries neither: a run that cannot be re-derived from
  what it wrote down is a run nobody can check a year later.
- Never infer jurisdiction from an IP address, a locale, or where the supplier sits. A reviewer
  in Tel Aviv may be auditing for a German legal entity. The settings file is the answer.
- **`US` means federal, and only federal.** § 1910.1200(a)(2) preempts state hazard-communication
  rules *"except pursuant to a Federally-approved state plan"* — and about half the states run one,
  California's Cal/OSHA among them, which may ask for more than the text in `reference/`. Rules on
  a different subject are not preempted at all: Proposition 65 warnings and the New Jersey,
  Pennsylvania and Massachusetts right-to-know lists sit in Section 15 of many US sheets. Audit
  neither. Do not raise a finding against a state requirement you cannot open, and do not let a
  CONFORMS imply one: the verdict covers 29 CFR 1910.1200 and `identity.md` declares the rest.

## Stage 1 — Legibility, then scope

Two questions, in this order: can the sheet be read at all, and is it a sheet this folder has a
rulebook for. Either one can end the run before a single provision is opened.

### 1a — Legibility

Extract the sheet, then gate it. Two commands, and the second is the one with teeth:

    python3 tools/extract.py <sheet.pdf> --outdir <run>   # rendering + fidelity report; exits 0 always
    python3 tools/verify_conversion.py <sheet.pdf> --outdir <run>   # Gate 1; exit 1 means stop

`tools/extract.py` produces `<name>.salus.md`, a line-anchored rendering, plus a fidelity report.
It reports and does not gate — whatever it found, it exits 0, because writing those two files is
its whole job. Gate 1 re-derives the same comparison from the PDF and from the rendering on disk
and turns it into an exit code. Read the verdict; do not read the exit code of the wrong script.

- **No text layer, or zero characters** → **CANNOT VERIFY**, reason quoted from the fidelity
  report. **Stop.** Gate 1 prints `NO TEXT LAYER` and exits 1 on such a sheet, under `--strict` or
  without it. It used to print PASS, because two empty extractions compare equal and the gate said
  so out loud; a gate whose assertion is vacuously true is not a gate.
- **The fidelity check fails** — Gate 1 prints `FAIL`, exit 1 — → **CANNOT VERIFY**. **Stop.** A
  lost chemical identifier and a rendering that is no longer the extraction both land here.
- **The fidelity check could not be made** — Gate 1 prints `UNCONFIRMED`, exit 1 — → **CANNOT
  VERIFY** until a person resolves it. Nothing was found wrong with the sheet; nothing was
  established about it either, and the two are not the same claim.
- **`REVIEW`** — a distinct character or token the independent engine found is not in the
  rendering — → a person reads `lost_characters` and `lost_tokens` before the audit continues.
  Exit 0 without `--strict`, exit 1 with it. A lost `µ` is a factor of a million on an exposure
  limit, so this is a stop for a person, not for the shell.
- Text extracted but no section headings found at all → **CANNOT VERIFY**. Stop.
- Partial: some sections legible, others empty → continue, and record each unreadable section as
  `not assessed — unreadable`, never as a failure.

### 1b — Scope

    python3 tools/check_scope.py <sheet.salus.md>     # the scope gate; exit 2 means stop

Read the sheet's own declaration of the standard it was **compiled to** — suppliers put it on the
first line, in the header, or in Section 15.

- **It declares a standard from a third regime — GB/T 16483, JIS Z 7253, GOST 30333, SOR/2015-17
  and the like — and declares neither 2020/878 nor 1910.1200** → **CANNOT VERIFY**, reason: out of
  scope. **Stop.** Name the standard the sheet declares, say that `reference/` does not ship it,
  and make no judgement about the sheet in its own regime. Run no further stages.
- It declares a third regime **and** the configured standard → continue. A sheet written for two
  markets is audited against the configured one, and the third declaration is not a finding.
- It declares the *other* standard this folder ships — a US sheet under `jurisdiction: EU`, or the
  reverse → continue. That is Stage 3's business and it is a finding there, not a stop: both
  rulebooks are here, so the comparison is real and says something useful.
- It declares nothing → continue. Stage 3 infers the revision from the issue date and says so.

Why this stops the run rather than becoming a finding: an auditor that does not hold the standard a
document was written to cannot say whether the document meets it. Measuring it against a different
standard yields one observation — the wrong ruler was used — restated once per provision, which
reads like a list of defects and is not one. This gate exists because exactly that was filed here
on 2026-09-11, before it existed. See `README.md` § *An incident, and the gate it produced*, and
the two runs in `audits/` that record it.

The stop is evidence-based, and only evidence-based: it fires on what the sheet **declares**, never
on a country name, an address, a language, an emergency telephone number or a chemical inventory
list. A sheet that tells a German reader its components appear on China's IECSC inventory is an EU
sheet with an inventory paragraph. Adding a regime to the gate's list is a deliberate edit to
`tools/check_scope.py`, and making a sheet pass by deleting one is forbidden outright.

A word is not a declaration either, and that cuts the other way — towards the stop, not away from
it. `REACH` is a regulation and an ordinary English verb, and *"Keep out of reach of children"* is
GHS precautionary statement P102, printed on sheets of every regime including the ones this folder
does not hold. The gate reads `REACH` as a declaration of Annex II only where the sheet writes it
as one: prepared, compiled, issued or conforming to it, or Annex II named beside it. Read loosely,
that one line of boilerplate was enough to suppress the stop on a sheet compiled to GB/T 16483.

## Stage 2 — Age gate *(house policy, not a provision)*

Find the date of issue or last revision. Compare with the run date.

    python3 tools/check_age.py <sheet.salus.md> --pdf <sheet.pdf>   # the arithmetic, with its evidence

That script reports and does not decide: it prints every date it found with the line it sits on,
measures the newest one that claims to govern, and says whether a finding is owed. Read its
evidence rather than its conclusion — it cannot tell a revision date from a print date, and it
lists any line that claims a date it could not parse, because a date it cannot read is not a date
the sheet failed to state.

`03/04/2026` is two dates, and the script removes the readings the document itself rules out — by
shape, by the sheet's own convention, by the order the sheet states between its own dates, and,
when you pass `--pdf`, by the file's own timestamp, which bounds what the sheet can claim and is
**never** read as the sheet's date. Each elimination is printed with the signal that made it. Pass
the PDF: without it one signal does not run, and nothing else changes. Where two readings survive
the script says so, and then the date is yours to read off the sheet — record which one you took
and why. The script reports; the auditor decides. That does not change.

- **≥ 5 years old → DOES NOT CONFORM.** The reason is recorded as a **policy gate**, and it is
  marked in the report as carrying no provision, because neither 2020/878 nor 1910.1200 sets an
  expiry. The rule exists because formulations change faster than sheets are reissued, and a
  sheet from 1997 read in 2026 is describing a different product. The remedy is a reissued sheet,
  or a written statement from the manufacturer that the composition has not changed.
- **No date found anywhere → CANNOT VERIFY.** Do not guess from a file timestamp.
- Under five years → record the age and continue.

The age gate never silently ends the audit. Continue through the remaining stages and report
everything you found, so the reviewer writing to the supplier has the whole list at once.

## Stage 3 — Which revision the sheet was compiled to

Look for the sheet's own declaration. Suppliers state it in the header — *"Conforms to Regulation
(EC) No. 1907/2006 (REACH), Annex II, as amended by Commission Regulation (EU) 2020/878"* — or
inside Section 15, or not at all.

Then open `reference/STANDARDS-LEDGER.md` and compare against the dates, not against your memory.

The report's header row *Standards knowledge last confirmed online* comes from
`reference/FRESHNESS-LOG.md`, which `tools/check_freshness.py` writes. Read that log before quoting
its date: a target recorded as **UNREACHABLE — could not establish** was not confirmed on that run,
whatever the *Last run* line says, and a run with any unreachable target marks itself **INCOMPLETE**
and exits 1. Cite the date of the last run that actually got answers for the standard you are
citing. A date is a claim about what was checked, and an audit that has never reached the
publishers is entitled to say when it last did — not to imply it just did.

- **Declared revision superseded and its transition window closed** → finding, citing the article
  that closed it. For the EU that is 2020/878 Article 2, window closed 2022-12-31.
- **Declared revision superseded but the window is still open** → **not a finding.** Record it as
  a dated note: which revision, which deadline, how long is left. For US mixtures the window runs
  to 2027-11-19 under § 1910.1200(j)(3)(i), so most US sheets sit here today.
- **No declaration** → do not treat this as a failure by itself. Infer the applicable revision
  from the issue date against the ledger, and say in the report that you inferred it.
- **Compiled for the other regime** → a sheet built to 29 CFR 1910.1200 and audited under
  `jurisdiction: EU` has not been compiled to Annex II at all, and the reverse holds too. This is a
  finding, and it cites the article that makes the annex mandatory — for the EU, 2020/878 Article 1,
  *"Annex II to Regulation (EC) No 1907/2006 is replaced by the text in the Annex to this
  Regulation."* Report it once, at Stage 3, and continue: the remaining stages still say useful
  things about a sheet in the wrong format.

## Stage 4 — Structure: the sixteen sections

Check that all sixteen sections are present, numbered, in order, and carry content.

- EU: Annex II to 2020/878, Part A, sections 1–16, and the subheadings each section names.
- US: § 1910.1200(g)(2)(i)–(xvi) for the headings and their order; § 1910.1200(g)(3) for the rule
  that a subheading with nothing to report must be *marked* as such rather than left blank.

A blank subheading that is not marked is a finding under (g)(3) in the US and under the
corresponding Annex II requirement in the EU. An empty section is a finding. A missing section is
a finding. Quote the section number and the heading as it appears in the sheet.

### Section 15, and the layer above the standard

The section most sheets fill with boilerplate, and the one where the two regimes do the opposite of
each other. Read the regime first.

**EU — Annex II 15.1 and 15.2 are content requirements, and they are checkable.**

> Information shall be provided regarding relevant Union safety, health and environmental
> provisions … or regarding the national regulatory status of the substance or mixture (including
> the substances in the mixture), including advice on action that should be taken by the recipient
> as a result of these provisions.

> This subsection of the safety data sheet shall indicate whether the supplier has carried out a
> chemical safety assessment for the substance or the mixture.

So on an EU run: a Section 15 that names no Union provision and no national status is a finding
against 15.1, and a 15.2 that does not say whether a chemical safety assessment was carried out is
a finding against 15.2 — the subsection asks for an answer, and *absent* is not one. Both are
`[STANDARD]`, severity **MATERIAL**. A subheading present and empty is already a finding under the
structure rule above; this is about a subheading that is present, populated, and answers a
different question than the one asked.

**US — the opposite, and it is stated in the standard itself.**

> Note 2 to paragraph (g)(2): OSHA will not be enforcing information requirements in sections 12
> through 15, as these areas are not under its jurisdiction.

The heading must be there — Note 1 to the same paragraph puts sections 12 to 15 in the list of
required headings, in order — and **the content of Section 15 is not enforceable under 29 CFR
1910.1200**. On a US run, do not raise a `[STANDARD]` finding about what Section 15 says or leaves
out. A missing or out-of-order heading is still a finding; its contents are not OSHA's to require,
and a finding that pretends otherwise cites a provision that does not exist.

**The state layer, on a US run only.** `reference/ca-prop-65/` holds California's Proposition 65
statute, which § 1910.1200(a)(2) does not preempt because it is a different subject: a warning owed
to the public, not hazard communication owed to an employee. Two things you may do with it, and one
you may not.

- You **may** read a Proposition 65 statement in Section 15 as a claim the sheet makes, and check
  it against the rest of the sheet. A warning naming a chemical that Section 3 does not disclose,
  or a "not subject to Proposition 65" line beside an ingredient the same sheet classifies as a
  carcinogen, is a contradiction inside one document — which is the only kind of finding Salus
  makes. Cite `reference/ca-prop-65/health-safety-code-chapter-6-6.md`, Section 25249.6, and never
  1910.1200: they are separate obligations and Gate 2 enforces the separation.
- You **may** record, as a declared blind spot rather than a finding, that a sheet destined for
  California carries no Proposition 65 statement at all.
- You **may not** say a warning was owed, or that one was not. That question is *is this substance
  on the state's list*, the list is published by OEHHA under Section 25249.8, and it is **not in
  `reference/`**. `reference/CONTEXT.md` § *California* says why it cannot be. A finding that
  asserts it in either direction rests on a list nobody here can open, which is the failure this
  whole folder is built against.

Other states run their own disclosure regimes — New Jersey, Pennsylvania and Massachusetts
right-to-know lists among them. None of that text is here, so none of it is audited, and a US
CONFORMS says nothing about it. `identity.md` declares this.

### The first page, and the revision trail — EU provision 0.2.5

Annex II 0.2.5, in full, because it carries three obligations and they are not the same one:

> The date of compilation of the safety data sheet shall be given on the first page. When a safety
> data sheet has been revised and the new, revised version is provided to recipients, the changes
> shall be brought to the attention of the recipients in Section 16 of the safety data sheet,
> unless the changes have been indicated elsewhere. For the revised safety data sheets, the date of
> compilation, identified as “Revision: (date)”, shall appear on the first page, as well as one or
> more indications of which version is replaced, such as version number, revision number, or
> supersedes date.

| | Owed by | Finding when |
| --- | --- | --- |
| a date of compilation **on the first page** | every sheet | the first page carries no date of compilation. A date that appears only in Section 16 satisfies Stage 2 and still breaches this: the provision says first page |
| the changes **brought to the recipient's attention in Section 16** | a revised sheet | neither Section 16 nor anywhere else says what changed. The provision's own escape — *"unless the changes have been indicated elsewhere"* — must be looked for before the finding is made |
| the first-page date **identified as a revision**, and **one or more indications of which version is replaced** | a revised sheet | the first page identifies no revision date at all, or nothing anywhere names the version replaced — no version number, no revision number, no supersedes date |

**When is a sheet "revised"?** On the evidence it carries: a version number above 1, a stated
previous issue or supersedes date, or its own revision wording. Where the sheet shows no sign of
ever having been revised, only the first obligation applies. Never infer a revision from a file
timestamp or a filename — that is not the document speaking.

**The trap, and this folder has fallen into its twin once already.** The provision illustrates the
identification with the string `“Revision: (date)”`. That is an illustration of *identifying the
date as a revision*, not a mandated spelling. A sheet whose first page reads
`Date of issue/Date of revision: 14/10/2024` has identified its date as a revision date and has
satisfied the obligation. Raising a finding against every sheet that words it differently would be
the wrong-ruler mistake of 2026-09-11 wearing a new number — one observation restated once per
sheet, and unreadable to the person who has to act on it. The finding is owed for **absence**, not
for wording.

**The borderline, named so nobody has to invent an answer under pressure.** Two sheets in this
folder's own corpus carry a version number well above 1 — `Version No: 14.1`, `Version 9` — and a
first page that labels its date `Issue Date` rather than as a revision. Both readings are
defensible: the date is not identified as a revision, which is what the provision asks for; and a
version number beside it tells the reader exactly which version that date belongs to, which is what
the provision is *for*. **Take a reading and write down which one you took**, in the finding if you
make one and under *Declared blind spots* if you do not. What is not acceptable is deciding it
silently, or deciding it differently on two sheets in the same run.

Class `[STANDARD]`, severity **MATERIAL**: the sheet is usable, and a reader cannot tell which
version of it they are holding, which is what the provision exists to prevent.

**US.** There is no first-page requirement. § 1910.1200(g)(2)(xvi) puts the date of preparation or
last revision in Section 16, and its absence there is the finding. Do not apply 0.2.5 to a US run —
it is the other regime's rulebook, and Gate 2 will refuse the citation.

## Stage 5 — Classification: Section 3 against CLP Annex VI

This is where sheets fail most often, and it is the stage that makes Salus an auditor rather than
a checklist.

**US runs stop before this stage.** 29 CFR 1910.1200 has no harmonised classification list, and
none is shipped for it. Under `jurisdiction: US`, record Section 3 as *not assessed for
classification correctness*, say so in the report's blind spots, and go to Stage 6. Citing CLP
Annex VI against a US sheet would be a finding under a regulation that does not govern it — the
exact false finding this folder is built to prevent.

**Both halves of that are now enforced, and were not until 2026-09-11.** `tools/verify_citations.py`
reads the regime out of the report's own header row and fails any finding whose `WHERE IN THE
STANDARD` names a file outside that regime's corpus: an EU run may cite `reference/eu-2020-878/`
and `reference/eu-clp-annex-vi/`, a US run may cite `reference/us-osha-hcs/` and nothing else.
`tools/validate_report.py` fails a US report that performed checks and nowhere records Section 3 as
*not assessed for classification correctness*. Until then the rule held because it was obeyed, which
is not the same thing as holding — it had already been broken once here, and was found by a person.

For each ingredient row in Section 3, on an EU run:

1. Read the identifiers: CAS number, EC number, Index number, REACH registration number.
2. Look the substance up in `reference/eu-clp-annex-vi/annex-vi-table-3-extract.md`, **by CAS or
   Index number**. Read one row. Do not read the file as prose — this is the whole reason a run
   costs a few thousand tokens instead of forty thousand.
3. **No row** → not harmonised. Record `self-classification, not checked` and move on. You have
   no provision to test it against and must not invent one.
4. **Row found** → compare the hazard class and category codes and the hazard statement codes in
   the sheet with the row.
   - Identical → passes. Say so; a pass is part of the report.
   - Sheet declares **more** than the row → not a finding. A supplier may classify more strictly
     than the harmonised minimum.
   - Sheet declares **less** than the row → check the Notes column first.
5. **Notes column.** If the row carries a note, open
   `reference/eu-clp-annex-vi/annex-vi-notes.md` and read that note before writing anything. Most
   of them are conditional releases from part of the harmonised classification, and a supplier
   relying on one is not in breach — but the sheet has to show it relied on it. Note L, for
   example, releases certain petroleum substances from the carcinogen classification only where
   the DMSO extract is below 3 % measured by IP 346. The finding in that case is not "wrong hazard
   code"; it is that the sheet departs from a harmonised classification **without recording the
   basis** the note requires. Write it that way.

## Stage 6 — Internal consistency

The standard requires a coherent document, not sixteen unrelated lists. Check that the same fact
told twice is told the same way.

| Check | What contradicts what |
| --- | --- |
| Flash point | the value in Section 9 against every other mention of it, and against the flammability class declared in Section 2 |
| Concentration | each ingredient's percentage band in Section 3 against any concentration limit the Annex VI row sets, and against the hazard statements in Section 2 |
| Hazard statements | the H-codes in Section 2 against the H-codes listed in Section 16 and against those in Section 3 |
| Physical state | Section 9 against Section 1's product type |
| Emergency contact | present in Section 1.4, and a number, not a placeholder |
| Storage and handling | Section 7 against the hazards declared in Section 2 |
| Disposal, transport, regulatory | Sections 13–15 present and populated, with the US caveat in `identity.md` |

Report a contradiction as a contradiction: quote both values, name both sections, and say that
the sheet does not let a reader determine which is correct. Do not pick a winner — you have no
basis to, and choosing one would be advising about the material.

---

## How a finding is written

Every finding carries five things. A finding missing any of them is not shippable, and a label
with nothing written under it is missing: `tools/verify_citations.py` reads the body, not the word.

    [F-03] [STANDARD] BLOCKING — Section 3 departs from Annex VI without the Note L basis
      WHAT   Section 3 lists "Distillates (petroleum), hydrotreated heavy naphthenic",
             CAS 64742-52-5, at >=25 - <=50 %, classified "Asp. Tox. 1, H304".
      WHERE  page 2, line 110 of BG - HCF MSDS 510231_UK_EN.pdf
      RULE   CLP Annex VI Table 3 row 649-465-00-7 reads, in the hazard-class, hazard-statement
             and Notes columns: "Carc. 1B | H350 | GHS08 Dgr | H350 | | | L".
             Note L reads: "The harmonised classification as a carcinogen applies unless it can
             be shown that the substance contains less than 3 % of dimethyl sulphoxide extract
             as measured by IP 346"
      WHERE IN THE STANDARD
             reference/eu-clp-annex-vi/annex-vi-table-3-extract.md, row 649-465-00-7
             reference/eu-clp-annex-vi/annex-vi-notes.md, Note L
             revision: 02008R1272-20260701
             confirmed current: 2026-09-11
      WHY    The harmonised entry classifies this substance as a category 1B carcinogen. The
             sheet does not carry that classification and does not state that the Note L
             condition was met, so a reader cannot tell whether the departure is lawful.

Two details in that example are not cosmetic, and `tools/verify_citations.py` enforces both.

**Every quoted string is checked, however short.** The gate pulls each string between double
quote marks out of the RULE and looks for it in the file the finding names — `"Carc. 1B"`, `"H350"`
and `"Note L"` exactly as readily as a whole sentence. Quote the standard's own words, at whatever
length says the thing, and quote them as they read.

There was a floor here until 2026-09-11: strings shorter than twelve characters were skipped, and
this file defended that by saying two short quotes on one line are read as one quote running from
the first closing mark to the next opening one. **That was never true of the regex that does the
reading.** Its character class cannot cross a quote mark, so `"Carc. 1B", column "L"` yields two
needles and not one. What the floor did instead was leave the hazard classes, the H-codes and the
Note letters — the atoms of a classification finding, and the strings a reader is least able to
check by eye — unverified, on a justification that a reader could have disproved in one line of
Python. It is gone.

**The example above is itself run through the gate**, by `tools/test_docs_example.py`, which lifts
it out of this file and puts it through the real citation and boundary checks. It has to be: this
is the file an auditor reads to learn how to cite, and a format taught here that the gate rejects
would be worse than no example at all. Run it after editing this section.

`WHERE IN THE STANDARD` is three parts, not one: the file and the row, the revision it belongs
to, and the date that revision was last confirmed current. A finding is checkable in time as well
as in text — a report read six months from now still says what Salus knew when it was written.

## Two classes of finding, never mixed

| Class | Marked | Has a provision | Example |
| --- | --- | --- | --- |
| **Standard violation** | `[STANDARD]` | yes, always | Section 3 classification against Annex VI |
| **Policy gate** | `[HOUSE POLICY — no provision]` | no, and it says so | the five-year age gate |

Both can produce DOES NOT CONFORM. They must never look alike on the page. A reader has to be
able to tell at a glance which findings the law requires and which this installation requires,
because those two carry different weight in a conversation with a supplier.

The marker goes on the heading, beside the tag: `### [F-03] [STANDARD] BLOCKING — ...`. A heading
that carries the tag and drops the class is not a badly formatted finding, it is an unchecked one.
Until 2026-09-11 neither report gate could see it at all: nothing under it was read, no provision
was looked for, and the report left both gates with the same counts as if the block had never been
written. `tools/validate_report.py` now counts the tags twice, once with the class marker and once
without, and fails on the difference; `tools/verify_citations.py` fails an unmarked heading on
sight, by name, before any other check runs.

## Severity

Three levels, and severity never changes the verdict — any finding of either class produces DOES
NOT CONFORM. Severity orders the list so the reviewer knows what to raise first.

`tools/validate_report.py` holds that first sentence in both directions: a CANNOT VERIFY report
that lists findings is refused, and so is a CONFORMS report that lists findings. A verdict is not
a summary a reader may disagree with — it is what the list underneath it comes to.

- **BLOCKING** — the sheet cannot serve its purpose: a missing or empty section, a superseded
  revision past its window, a classification that understates a harmonised entry, a contradiction
  in a value that drives a hazard class.
- **MATERIAL** — a reader can still use the sheet but the standard is not met: an unmarked empty
  subheading, a missing identifier, a note relied on without stating the basis.
- **MINOR** — formal defects: ordering, numbering, a heading that does not match the wording the
  standard sets.

## How the reference layer is read

An access rule, addressed to whoever is doing the audit. Nothing here is a budget: reading a
standard at the provision is what makes a citation exact, and the saving is a consequence.

- Read the sheet through its extracted `.salus.md`, and read sections by anchor, not the whole file.
- Read Annex VI **by identifier lookup**. One CAS number, one row. Never load the table.
- Open `annex-vi-notes.md` only when a row's Notes column is non-empty, and read only that note.
- Open the standard's text at the provision you are about to cite, not before.

What this costs a run, and why the whole converted sheet ships beside a report that did not read
every line of it, are questions a reader of the project asks rather than an auditor at work.
`README.md` § *How it works* answers both, once.

## Before the report leaves

Five checks, in the order a run meets them — `README.md` § *How it works* numbers them on the
diagram. A report that has not passed every one of them has not been produced.

    python3 tools/verify_conversion.py <sheet.pdf>   # 1 · Gate 1: is the conversion faithful
    python3 tools/check_scope.py <sheet.salus.md>    # 2 · the scope gate: is there a rulebook for this sheet
    python3 tools/verify_reference.py                # 3 · Gate 0: is the corpus still what was generated
    python3 tools/verify_citations.py <report.md>    # 4 · Gate 2: does every citation exist and match
    python3 tools/validate_report.py <report.md>     # 5 · Gate 3: verdict shape and the hard boundaries

Checks 1 and 2 are not run here at all: they run at Stage 1a and Stage 1b, before there is a report
to guard, and the scope gate is the only check that can end an audit before it starts. Gate 0 needs
no place of its own either — Gate 2 calls it before it reads a single citation — and it is listed
because running it alone asks about the corpus rather than about a report.

Two scripts guard this file rather than a sheet. Run them after editing `rules.md`, not after an
audit:

    python3 tools/test_docs_example.py               # does rules.md still teach a shape the gates accept
    python3 tools/check_docs.py                      # does the list above still match README.md and tools/

Both report gates read the regime out of the report's header table — the row
`| Jurisdiction (from `config/jurisdiction.md`) | EU |` — and a report that carries no such row
fails both. Write the header before you write the findings; it is what decides which rulebook the
findings are allowed to stand on. See `tools/CONTEXT.md` § *Which jurisdiction a report gate believes*
for why that row, and not the config file, is what the gates trust.

Gate 3 is the one that catches you. It scans the whole report — not line by line, because this
format wraps a sentence across lines — for permission language in English and Russian, and voids
the run if it finds any. The only exemption is a span inside quotation marks, which is what lets a
finding reproduce a Section 7 that reads "safe to use" without being read as having said it. Not
indentation, not a table row, not a blockquote: quotation, and the marks have to pair, so a report
carrying an odd number of them is refused before it is scanned for anything else.

Run these as cold subagents with no knowledge of how the audit went, or run them as scripts —
either way the checker must not be the thing that made the claim.
