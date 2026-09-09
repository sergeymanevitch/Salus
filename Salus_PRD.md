# Salus Product Requirements Document

**Evidence-grounded, jurisdiction-aware pre-audit of Safety Data Sheets**

**Version:** 2.0  
**Date:** 9 September 2026  
**Status:** Implementation-ready draft  
**Owner:** Sergey Manevitch  
**Product name:** Salus  
**Initial jurisdiction profiles:** United States Federal OSHA HCS and European Union REACH Annex II with supporting CLP checks  
**Architecture:** Interpretable Context Methodology (ICM), composed Pipeline plus Knowledge Bundle  
**Release target:** Competition-ready minimum viable product (MVP)

---

## 1. Executive summary

Salus is a folder-based AI system that performs an evidence-grounded pre-audit of a Safety Data Sheet (SDS) across all 16 sections. It checks document structure, jurisdiction-dependent content, conditional applicability, selected scientific and regulatory relationships between sections, evidence quality, and the internal integrity of the generated audit result.

Salus does not certify legal compliance, issue a legal opinion, replace a qualified regulatory professional, or reconstruct a complete chemical classification from incomplete data. It produces reviewable findings tied to exact SDS evidence, approved regulatory sources, normalized requirements, a versioned derived rule, and an explicit applicability rationale.

The product's defining requirement is not merely that it generates an audit report. Salus must validate that report before release. Every audit therefore passes through an independent result-validation stage and a fail-closed release gate. If the result cannot be validated, Salus withholds the normal final report and produces a validation-failure report.

Salus is arranged as an ICM workspace. Folder numbering carries sequence, hierarchy scopes context, plain files carry state, each working folder has one job, and every intermediate output is inspectable and editable. Stable regulations, policies, schemas, and rule definitions are separated from per-run artifacts. No stage loads the entire workspace.

### 1.1 MVP proposition

The MVP prioritizes depth, traceability, and reliable uncertainty handling over broad jurisdiction coverage. It includes:

- one SDS per audit;
- PDF or extracted-text input;
- complete S01-S16 coverage;
- US Federal OSHA HCS and EU REACH Annex II profiles;
- selected supporting CLP checks only where required to evaluate SDS content;
- a controlled initial set of cross-section rules;
- exact evidence and source traceability;
- a full per-audit validation stage;
- a test harness with golden, adversarial, and regression fixtures;
- versioned regulatory source and rule packages;
- human review gates at defined stage boundaries.

### 1.2 Product principle

> No conclusion without evidence. No definitive failure without established applicability. No released report without validation.

---

## 2. Problem statement

Manual SDS review is slow, repetitive, and vulnerable to omission. A reviewer must navigate 16 sections, distinguish jurisdictional requirements, assess conditional provisions, compare values and statements across sections, verify sources, and decide whether missing information is a true nonconformity or merely insufficient evidence.

Existing lightweight AI approaches commonly fail because they:

- check only whether section headings exist;
- apply jurisdictional rules without proving applicability;
- confuse official law, guidance, and derived interpretation;
- treat a missing keyword as a definitive violation;
- use one physical property as a complete classification decision;
- invent citations or replacement wording;
- generate a plausible report without validating whether its evidence, counts, conclusions, and citations are internally coherent;
- load too much context at once, weakening focus and traceability.

Salus addresses these failures with a staged and observable audit pipeline, a closed and versioned knowledge base, explicit uncertainty states, and a final validation gate.

### 2.1 User pain points

1. Reviewing all 16 sections requires repeated navigation and comparison.
2. US and EU requirements differ in content, applicability, terminology, effective dates, and transition logic.
3. Scientific checks often require several parameters, units, test conditions, and exceptions.
4. Supplier SDSs may be scanned, multilingual, poorly extracted, internally inconsistent, or incomplete.
5. LLM-generated reports may sound certain even when underlying evidence is weak.
6. Regulatory updates can invalidate rules unless source and rule versions are controlled.
7. Long reports are difficult to verify if findings do not expose exact evidence and provenance.
8. A generated result is not trustworthy merely because it is well formatted.

---

## 3. Product vision, objectives, and constraints

### 3.1 Vision

Create a transparent and dependable SDS pre-auditor that a lubricant specialist, environment-health-and-safety professional, or regulatory reviewer can inspect, challenge, reproduce, and improve without relying on hidden orchestration.

### 3.2 Objectives

#### O1. Complete coverage
Every numbered SDS section receives a recorded terminal evaluation state.

#### O2. Evidence-grounded findings
Every definitive finding identifies exact document evidence, an approved source, a normalized requirement, rule ID and version, applicability rationale, and evaluation.

#### O3. High-value consistency checks
Salus detects selected contradictions and unresolved relationships between sections while avoiding unsupported automatic reclassification.

#### O4. Explicit uncertainty
Missing or unsuitable evidence results in `MISSING_EVIDENCE`, `REVIEW_REQUIRED`, or `NOT_EVALUATED`, not a fabricated PASS or FAIL.

#### O5. Validated final result
Every report undergoes independent evidence, citation, applicability, rule-execution, coherence, and completeness checks before release.

#### O6. Controlled change
Official sources, normalized requirements, and derived rules remain separate and versioned. Updates require impact analysis, regression testing, approval, and activation.

#### O7. ICM observability
A cold agent and a human reviewer can determine where the system is, what each stage reads, what it produced, and why it stopped by inspecting files alone.

### 3.3 Non-goals

The MVP will not:

- issue a certificate of compliance;
- provide legal advice or regulatory authorization;
- authorize shipment, workplace use, or market placement;
- perform complete substance or mixture classification from incomplete data;
- infer undisclosed composition;
- replace toxicologists, regulatory counsel, qualified SDS authors, or competent authorities;
- cover California Proposition 65, state Right-to-Know overlays, or non-US/EU country packs;
- perform live unattended regulatory updates;
- silently rewrite or activate rules;
- guarantee OCR accuracy;
- perform definitive transport classification;
- rewrite an SDS as an authoritative corrected document;
- process bulk libraries or provide enterprise integrations in the MVP.

### 3.4 Product boundaries

Salus is a pre-audit and review-support system. Its output describes what the available evidence supports within a named jurisdiction profile, source package, rule package, and capability version. A PASS means only that the evidence satisfied a specific executed check. It does not mean the entire SDS or product is compliant.

---

## 4. Users and jobs to be done

### 4.1 Primary users

- **SDS reviewer:** obtain complete section coverage and prioritized, traceable findings.
- **Lubricant specialist:** compare supplier SDS content with physical, chemical, and product knowledge.
- **EHS professional:** screen an SDS before workplace introduction.
- **Regulatory specialist:** investigate applicability, sources, assumptions, and remediation needs.
- **Rule maintainer:** update sources and derived logic without destroying prior baselines.
- **Competition judge or evaluator:** reproduce expected results and inspect system rigor.

### 4.2 Core jobs

- Audit one SDS against US, EU, or both profiles.
- Identify missing mandatory content only when applicability is established.
- Identify internal contradictions and unresolved scientific relationships.
- Distinguish a true failure from missing evidence or expert-review need.
- Trace each conclusion from source document to rule and regulatory basis.
- Verify the generated audit before releasing it.
- Re-run the same audit against a controlled package and obtain materially equivalent results.
- determine system status by inspecting stage outputs.

### 4.3 User stories

- As a reviewer, I want every SDS section evaluated so selective analysis cannot hide omissions.
- As a lubricant specialist, I want Sections 2, 3, 8, 9, 11, 12, and 14 cross-checked so high-value inconsistencies are visible.
- As a regulatory specialist, I want each conditional requirement to expose its trigger facts and exceptions.
- As a maintainer, I want each derived rule linked to authoritative source text and regression fixtures.
- As a user, I want Salus to say when it cannot decide.
- As a reviewer, I want the final report validated against the underlying SDS and its own detailed findings.
- As an evaluator, I want a cold agent to walk the workspace without relying on prior chat history.

---

## 5. Architecture

### 5.1 Architectural decision

Salus uses a composed ICM form:

- **Pipeline:** one SDS audit is the repeating unit and moves through ordered stages.
- **Knowledge Bundle:** regulations, sources, requirements, rules, schemas, terminology, and reference examples form stable navigable knowledge.
- **Independent test harness:** fixtures and expected results test Salus from outside the normal audit run.

### 5.2 ICM invariants adopted by Salus

1. One folder has one job.
2. Root routing files remain small and stable.
3. Numbered folders encode execution order.
4. Every working folder has an explicit `CONTEXT.md` contract.
5. Stable factory knowledge is structurally separated from per-run products.
6. Every intermediate output is a human-editable surface.
7. A stage loads only its declared inputs and references.
8. Interfaces use plain Markdown and JSON with explicit links and provenance.
9. Filesystem state determines pipeline state.
10. New runs begin from a copied run template, not a blank folder.

### 5.3 Required root contract

The Salus root contains only four Markdown files plus two folders:

```text
Salus/
├── README.md
├── identity.md
├── examples.md
├── rules.md
├── reference/
└── tests/
```

No other file may be placed at root. This is a project-specific constraint.

- `README.md` is human-facing orientation, setup, operation, limitations, and navigation.
- `identity.md` defines Salus's role, authority boundary, behavior, and refusal conditions.
- `examples.md` demonstrates correct inputs, findings, uncertainty, validation failure, and prohibited behavior.
- `rules.md` is the compact execution router and global operating contract.
- `reference/` contains the complete internal ICM pipeline, stable knowledge, schemas, templates, scripts, and run artifacts.
- `tests/` contains the independent test territory.

The normal ICM entry-file responsibilities are intentionally distributed across these four required root files. The internal pipeline router is `reference/CONTEXT.md`.

### 5.4 Target workspace structure

```text
Salus/
├── README.md
├── identity.md
├── examples.md
├── rules.md
├── reference/
│   ├── CONTEXT.md
│   ├── _shared/
│   │   ├── CONTEXT.md
│   │   ├── definition-of-done.md
│   │   ├── terminology.md
│   │   ├── result-model.md
│   │   ├── severity-model.md
│   │   ├── confidence-model.md
│   │   ├── evidence-policy.md
│   │   ├── citation-policy.md
│   │   ├── applicability-policy.md
│   │   ├── validation-policy.md
│   │   └── security-policy.md
│   ├── _knowledge/
│   │   ├── CONTEXT.md
│   │   ├── source-register/
│   │   ├── official-sources/
│   │   ├── normalized-requirements/
│   │   ├── derived-rules/
│   │   ├── jurisdiction-profiles/
│   │   ├── section-requirements/
│   │   ├── cross-section-rules/
│   │   └── regulatory-history/
│   ├── _schemas/
│   ├── _templates/
│   ├── _scripts/
│   ├── runs/
│   └── stages/
│       ├── 01_intake/
│       ├── 02_extract/
│       ├── 03_qualify/
│       ├── 04_determine-applicability/
│       ├── 05_audit-structure/
│       ├── 06_audit-sections/
│       ├── 07_validate-cross-section/
│       ├── 08_construct-findings/
│       ├── 09_validate-results/
│       ├── 10_generate-report/
│       └── 11_release-gate/
└── tests/
    ├── README.md
    ├── CONTEXT.md
    ├── _schemas/
    ├── _templates/
    ├── fixtures/
    ├── expected-results/
    ├── regression/
    ├── validation/
    └── test-runs/
```

Every stage folder contains `CONTEXT.md`, `references/`, and `output/`. Empty speculative directories must not be created before their contents and owner are defined.

### 5.5 Stage-contract requirements

Each stage `CONTEXT.md` must contain:

- one-sentence job;
- exact working inputs for the current run;
- exact stable references;
- explicit `Do NOT load` exclusions;
- short numbered process;
- hard limits and stop conditions;
- named outputs and locations;
- one concrete human check or a documented automated gate;
- handoff condition;
- failure behavior.

A stage contract links to policy and reference files instead of repeating their content.

### 5.6 Run isolation

Each audit receives a unique run ID and a copied run template under `reference/runs/`. A run contains source input metadata, stage outputs, validation records, final artifacts, package versions, warnings, and approval status. A stage must not read prior runs unless a regression or comparison task explicitly names them.

---

## 6. Audit pipeline

### 6.1 Stage 01: Intake

**Job:** register the input and requested audit scope.

**Inputs:** one PDF or text SDS; requested jurisdiction; optional intended market, language, product type, and user-supplied context.

**Outputs:** immutable input copy or stable reference, checksum, input manifest, scope record, run ID.

**Gate:** confirm the correct document and jurisdiction request were captured.

**Stop conditions:** missing file, unsupported type, encrypted/unreadable input, ambiguous request that prevents safe execution.

### 6.2 Stage 02: Extract

**Job:** extract source text and location anchors without interpreting compliance.

**Outputs:** page/block text, table captures, OCR indicators, extraction warnings, and an evidence map retaining original wording.

**Requirements:** do not normalize away units, symbols, decimal conventions, language, qualifiers, or table relationships. Preserve original and extracted values separately.

**Gate:** sampling confirms that critical pages and tables can be located in the original.

### 6.3 Stage 03: Qualify

**Job:** determine whether the extracted artifact is sufficiently complete and reliable to audit.

**Checks:** page coverage, section detection feasibility, OCR corruption, missing pages, duplicate pages, language support, table integrity, and whether the artifact is actually an SDS.

**Outputs:** qualification record and capability limits.

**Gate:** auditability status is `QUALIFIED`, `QUALIFIED_WITH_LIMITATIONS`, or `REJECTED`.

### 6.4 Stage 04: Determine applicability

**Job:** establish which requirements and rules may run.

**Inputs:** selected jurisdiction, SDS metadata, product facts, substance/mixture evidence, use context, dates, and active source-package transition logic.

**Outputs:** applicability matrix with trigger facts, unanswered questions, effective-date logic, exceptions, and rationale.

**Gate:** no conditional rule proceeds as definitive if its trigger facts are unresolved.

### 6.5 Stage 05: Audit structure

**Job:** map the document to S01-S16 and evaluate section presence, order, headings, and empty/omitted/unavailable distinctions.

**Outputs:** section map and structural findings.

**Constraints:** section numbers and semantic headings take priority over exact English spelling. Translation and formatting variants must not fail solely because wording differs.

### 6.6 Stage 06: Audit sections

**Job:** execute the approved content checks for each of the 16 sections.

**Outputs:** one check record per active section rule, including evidence, applicability, result, and missing inputs.

**Gate:** every active section rule has a terminal state.

### 6.7 Stage 07: Validate cross-section relationships

**Job:** execute approved multi-section consistency and screening rules.

**Outputs:** comparison records recording all source values, units, conditions, rule inputs, exceptions, and conclusion limits.

**Constraint:** screening evidence must not be presented as a completed legal or scientific classification.

### 6.8 Stage 08: Construct findings

**Job:** convert failed, inconsistent, uncertain, and material informational check records into discrete findings.

**Outputs:** normalized finding set and section coverage matrix.

**Constraints:** unrelated issues remain separate; duplicates are linked or consolidated without loss of provenance; every finding follows the finding schema.

### 6.9 Stage 09: Validate results

**Job:** independently test the complete result set against the SDS, active knowledge package, schemas, and internal-coherence rules.

**Outputs:** validation record, defect list, release recommendation, and corrected result set only when corrections are fully evidence-based and traceable.

**Independence requirement:** this stage must not simply restate Stage 08. It must re-open sampled or risk-ranked evidence, verify citations, recompute counts, and challenge applicability and result-state selection.

### 6.10 Stage 10: Generate report

**Job:** create the human-readable report and machine-readable result from validated findings only.

**Outputs:** `audit-report.md`, `audit-result.json`, and concise validation summary.

**Constraint:** a finding that has not passed validation cannot enter the normal final report.

### 6.11 Stage 11: Release gate

**Job:** decide whether final artifacts may be released.

**Outputs:** release decision, package manifest, validation report, and either released artifacts or a validation-failure report.

**Rule:** fail closed. Blocking validation defects prevent release of a normal completed audit.

---

## 7. Functional requirements

### 7.1 Input and preprocessing

- **FR-001:** Accept one PDF or text SDS per run.
- **FR-002:** Reject or constrain unsupported, unreadable, encrypted, malformed, or non-SDS inputs without fabricating an audit.
- **FR-003:** Assign a unique run ID and compute an input checksum.
- **FR-004:** Preserve the original input unchanged.
- **FR-005:** Extract page/block coordinates where available.
- **FR-006:** Record extraction method, quality warnings, and affected pages.
- **FR-007:** Detect document language and preserve source-language wording.
- **FR-008:** Detect sections, subsections, tables, values, units, qualifiers, and test conditions.
- **FR-009:** Store original evidence separately from normalized analysis.
- **FR-010:** Record available metadata, including product identifier, supplier, revision date, language, and stated region.

### 7.2 Applicability

- **FR-020:** Support US, EU, or dual-profile selection.
- **FR-021:** Display profile ID and version in every report.
- **FR-022:** Determine substance versus mixture only from evidence.
- **FR-023:** Record unknown status when evidence does not support a determination.
- **FR-024:** Apply effective dates, transition periods, responsible-actor facts, and grandfathering logic from approved source records.
- **FR-025:** Evaluate conditional EU provisions from explicit trigger facts.
- **FR-026:** Permit `NOT_APPLICABLE` only with a recorded rationale.
- **FR-027:** Convert unresolved trigger facts into `MISSING_EVIDENCE` or `REVIEW_REQUIRED`.
- **FR-028:** Keep jurisdiction conclusions separate in dual-profile audits.

### 7.3 Structural audit

- **FR-030:** Map all detected sections to S01-S16.
- **FR-031:** Check presence and sequence.
- **FR-032:** Recognize translated and stylistic heading variants.
- **FR-033:** Distinguish omitted sections, present-but-empty sections, unavailable information, and extraction failure.
- **FR-034:** Identify duplicate or ambiguous section mappings.
- **FR-035:** Produce a complete section coverage matrix.

### 7.4 Section audit minimum scope

1. **Identification:** product identifier, supplier/responsible-party information, contact evidence, emergency telephone, recommended use, restrictions, and jurisdiction-dependent fields.
2. **Hazard identification:** classifications, label elements, signal word, pictogram references, hazard statements, precautionary statements, and other hazards.
3. **Composition:** substance/mixture status, identifiers, concentrations or ranges, trade-secret treatment, classifications, and applicable special forms.
4. **First aid:** exposure routes, symptoms/effects, immediate medical attention, and special treatment.
5. **Firefighting:** suitable and unsuitable media, specific hazards, combustion products, and protective equipment.
6. **Accidental release:** personal precautions, emergency procedures, environmental precautions, containment, and cleanup.
7. **Handling and storage:** safe handling, hygiene, incompatibilities, storage conditions, and specific use.
8. **Exposure controls/PPE:** occupational limits, source and jurisdiction, engineering controls, PPE, units, and ingredient linkage.
9. **Physical and chemical properties:** jurisdiction-required properties, values, units, methods, conditions, applicability, and omission rationale.
10. **Stability and reactivity:** reactivity, stability, hazardous reactions, conditions/materials to avoid, and decomposition products.
11. **Toxicology:** likely routes, symptoms, immediate/delayed effects, acute/chronic endpoints, numerical measures, data basis, and limitations.
12. **Ecology:** ecotoxicity, persistence, degradability, bioaccumulation, mobility, and other effects as applicable.
13. **Disposal:** treatment methods, contaminated packaging, and jurisdictional limitations.
14. **Transport:** UN information, class, packing group, environmental hazards, special precautions, and mode-specific limitations where available.
15. **Regulatory:** relevant regulatory information with jurisdiction and source traceability, without assuming a universal TSCA, Prop 65, or inventory-statement requirement.
16. **Other information:** preparation/revision date, change history, abbreviations, references, and other supplied notes.

### 7.5 Initial cross-section rule set

- **XR-01:** Section 1 identifier versus document and supplied label identifier.
- **XR-02:** Section 2 classifications versus Section 3 disclosed ingredient information, as a review screen only unless all classification inputs are available.
- **XR-03:** Section 2 flammability versus Section 9 flash point, initial boiling point, physical state, method, and units.
- **XR-04:** Section 2 aspiration classification versus Sections 3 and 9, including composition basis, kinematic viscosity, temperature, product type, and applicable exceptions.
- **XR-05:** Section 2 acute-toxicity classification versus Section 11 endpoint evidence, requiring route, species, value type, data basis, and mixture relevance.
- **XR-06:** Section 5 firefighting guidance versus Section 10 reactivity and decomposition statements.
- **XR-07:** Section 7 storage and incompatibility guidance versus Section 10 conditions and materials to avoid.
- **XR-08:** Section 8 occupational limits versus Section 3 disclosed ingredients and selected jurisdiction sources.
- **XR-09:** Section 12 environmental statements versus Sections 2 and 14.
- **XR-10:** Section 14 transport statements versus Sections 2 and 9 as a review screen, not an automatic transport determination.
- **XR-11:** Section 16 revision metadata versus profile transition logic and claimed rule baseline.
- **XR-12:** repeated values and claims across the document, including product name, physical state, flash point, and ingredient identifiers.

No cross-section rule becomes active until its inputs, logic, limitations, authoritative basis, owner, version, and positive/negative/insufficient-evidence tests are approved.

### 7.6 Finding generation

- **FR-070:** Produce one finding per discrete issue.
- **FR-071:** Quote source evidence exactly and identify its location.
- **FR-072:** Link each finding to a check ID and rule version.
- **FR-073:** Cite the official source record and normalized requirement.
- **FR-074:** State the jurisdiction and applicability rationale.
- **FR-075:** Separate result, severity, confidence, and human-review status.
- **FR-076:** List missing inputs.
- **FR-077:** Provide a conservative next action.
- **FR-078:** Identify checks not performed and why.
- **FR-079:** Do not invent corrected regulatory or scientific facts.

### 7.7 Validation and release

- **FR-080:** Validate every final finding before report generation.
- **FR-081:** Verify that every quote exists at its recorded location.
- **FR-082:** Verify source and rule references against the active package.
- **FR-083:** Verify applicability, required inputs, units, conditions, and exceptions.
- **FR-084:** Detect contradictory result states.
- **FR-085:** Reconcile summary counts with detailed findings.
- **FR-086:** Validate S01-S16 terminal coverage.
- **FR-087:** Validate report schema and required metadata.
- **FR-088:** Assign every validation defect a blocking or non-blocking class.
- **FR-089:** Fail closed on blocking defects.
- **FR-090:** Produce a machine-readable validation record and human-readable validation report.

---

## 8. Result, severity, and confidence models

### 8.1 Result states

- **PASS:** evidence satisfies one executed check within declared scope.
- **FAIL:** a cited mandatory requirement is demonstrably unmet and applicability is established.
- **INCONSISTENT:** two or more material document statements cannot be reconciled.
- **MISSING_EVIDENCE:** required information to execute or conclude the check is absent or unusable.
- **REVIEW_REQUIRED:** evidence indicates a material issue, but expert judgment or additional data is needed.
- **NOT_APPLICABLE:** the rule does not apply and the reason is recorded.
- **NOT_EVALUATED:** processing, extraction, capability, or package limitations prevented evaluation.

A PASS is check-specific and must never be presented as certification of the entire document.

### 8.2 Severity

- **Critical:** credible immediate risk of materially incorrect hazard communication or a severe mandatory omission, supported by high-quality evidence.
- **Major:** established mandatory gap, material inconsistency, or missing evidence that blocks reliable assessment.
- **Minor:** limited traceability, formatting, or clarity issue that does not presently alter the core hazard message.
- **Informational:** observation, limitation, or improvement opportunity without a compliance conclusion.

Severity is independent of confidence and result.

### 8.3 Confidence

- **High:** direct evidence, clear applicability, complete rule inputs, and direct source mapping.
- **Medium:** evidence is substantially complete but requires normalization or bounded interpretation.
- **Low:** extraction, context, or applicability is materially uncertain.

Low-confidence items cannot be definitive FAIL findings unless a human validator explicitly approves the conclusion and the approval is recorded.

---

## 9. Finding and output schemas

### 9.1 Required finding fields

1. Finding ID
2. Check ID
3. Rule ID and version
4. Result
5. Severity
6. Confidence
7. Jurisdiction
8. Applicability rationale
9. SDS section or sections
10. Exact document evidence
11. Evidence location
12. Normalized facts
13. Official source record
14. Normalized requirement
15. Evaluation
16. Missing inputs
17. Recommended action
18. Human review required
19. Validation status
20. Validation notes

### 9.2 Final artifacts

A released run produces:

```text
audit-report.md
audit-result.json
validation-report.md
release-manifest.json
```

If release is blocked, the run produces:

```text
validation-failure-report.md
validation-result.json
release-manifest.json
```

The normal audit report must not be labeled released.

### 9.3 Report structure

1. Document and run identification
2. Scope and selected profiles
3. Source, rule, schema, and model/package versions
4. Extraction and qualification warnings
5. Executive summary
6. Jurisdiction-level outcome
7. S01-S16 coverage matrix
8. Prioritized findings
9. Checks with missing evidence
10. Checks not evaluated
11. Validation summary
12. Limitations
13. Required human review
14. Provenance and release record

---

## 10. End-result validation specification

### 10.1 Validation objectives

Per-audit validation must establish that the final result is:

- grounded in the submitted SDS;
- scoped to the correct jurisdiction and time;
- produced by active approved rules;
- internally consistent;
- complete for the declared capability;
- transparent about uncertainty and limitations;
- safe to present as a pre-audit result.

### 10.2 Validation gates

#### V1. Input identity
Verify checksum, filename, run ID, and that the audited artifact is the registered input.

#### V2. Extraction coverage
Verify page count, extraction warnings, missing pages, and evidence-locator usability.

#### V3. Section coverage
Verify S01-S16 each has a terminal state and no section was silently skipped.

#### V4. Evidence integrity
Verify each quoted passage and value exists at the recorded location and that normalization did not change meaning.

#### V5. Citation integrity
Verify each citation points to an approved source record, correct provision, correct source type, and active source version.

#### V6. Applicability integrity
Verify jurisdiction, date, product type, substance/mixture status, conditional triggers, exceptions, and unresolved facts.

#### V7. Rule-execution integrity
Verify active version, complete required inputs, compatible units, test conditions, exception handling, and allowed conclusion strength.

#### V8. Finding integrity
Verify schema, uniqueness, result/severity/confidence compatibility, rationale, missing inputs, and recommended action.

#### V9. Cross-finding coherence
Verify no unresolved PASS/FAIL conflict, no duplicated definitive findings, and consistent jurisdiction labels.

#### V10. Summary reconciliation
Recalculate counts by result, severity, section, and jurisdiction and compare them with all summaries.

#### V11. Remediation safety
Verify no invented values, classifications, supplier details, legal declarations, or authoritative replacement text.

#### V12. Limitations completeness
Verify extraction, capability, source-age, rule-coverage, and unevaluated-check limitations are visible.

#### V13. Artifact completeness
Verify all required files, metadata, versions, and signatures/approvals exist.

#### V14. Release decision
Apply blocking rules and record release, release-with-declared-limitations, or blocked status.

### 10.3 Blocking defects

The following always block normal release:

- missing or mismatched input identity;
- a definitive finding with no verifiable evidence;
- a definitive finding with no approved regulatory basis;
- unresolved applicability for a definitive FAIL;
- invented evidence, source, rule, or value;
- contradictory definitive outcomes for the same check and jurisdiction;
- incomplete section coverage hidden from the report;
- summary counts that cannot be reconciled;
- missing validation record;
- unapproved or inactive rule package;
- evidence suggesting prompt injection affected execution;
- corrupted extraction that materially affects conclusions without disclosure.

### 10.4 Non-blocking defects

A non-blocking defect may permit release with declared limitations only when it cannot change a definitive conclusion. Examples include minor formatting defects, non-critical locator imprecision where the quote remains verifiable, or an informational check not executed due to a documented capability limit.

### 10.5 Error correction

Validation may correct clerical or deterministic defects, such as a count or schema formatting error, if the correction is logged. Validation must not silently alter substantive conclusions. A substantive defect returns the result to the responsible earlier stage, preserving both pre-correction and corrected artifacts.

---

## 11. Knowledge and rule architecture

### 11.1 Knowledge layers

Salus maintains separate layers:

1. **Official sources:** authoritative legal and regulatory text.
2. **Official guidance:** non-binding explanatory material, labeled as guidance.
3. **Normalized requirements:** concise statements with source location, scope, effective date, applicability, exceptions, and status.
4. **Derived rules:** executable or prompt-executable interpretations with inputs, logic, limits, tests, owner, approval, and version.
5. **Reference data:** controlled lists, units, terminology, aliases, and mappings with provenance.

A rule may link to a requirement. It must not copy a requirement in a way that creates a second source of truth.

### 11.2 Source record fields

- source ID;
- full title;
- issuing authority;
- source type;
- jurisdiction;
- authoritative URL;
- retrieved date;
- publication and effective date;
- transition dates;
- version or consolidation status;
- exact provision location;
- checksum or captured snapshot identifier;
- affected normalized requirements and rules;
- reviewer and approval status.

### 11.3 Derived rule fields

- stable rule ID;
- title and purpose;
- jurisdiction;
- version;
- status: draft, active, deprecated, withdrawn;
- authoritative requirement links;
- required inputs;
- optional inputs;
- data types and units;
- applicability triggers;
- exclusions and exceptions;
- decision logic;
- allowed result states;
- maximum allowed conclusion strength;
- known limitations;
- positive test;
- negative test;
- insufficient-evidence test;
- adversarial test where relevant;
- owner, reviewer, approval date;
- change history.

### 11.4 Source hierarchy

Binding legal text outranks official guidance. Official guidance outranks third-party interpretation. Third-party material may support research but cannot independently support a definitive legal finding. Salus must disclose when an interpretation is derived rather than directly stated.

---

## 12. Regulatory baseline and update control

### 12.1 Initial baseline

The initial source package must include, at minimum:

- current 29 CFR 1910.1200 text and appendices;
- OSHA's 2024 HCS final-rule materials;
- current OSHA transition-date notices and enforcement guidance relevant to the active release;
- Commission Regulation (EU) 2020/878;
- current consolidated REACH Annex II baseline used by the project;
- only those CLP provisions needed by active SDS checks;
- official supporting guidance clearly separated from binding law.

### 12.2 Update workflow

1. Monitor named official sources.
2. Capture candidate source and retrieval metadata.
3. Compare it with the approved snapshot.
4. Identify changed provisions, effective dates, transitions, and affected jurisdictions.
5. Map changes to normalized requirements and derived rules.
6. Create a draft source and rule package.
7. run unit, golden, adversarial, and full regression suites.
8. perform reference-integrity checks.
9. obtain qualified human approval.
10. activate the new package without deleting the previous package.
11. record migration and compatibility notes.

No web-connected model may silently update or activate rules.

### 12.3 Temporal behavior

Every audit records the SDS revision date where available, audit date, active source package, and transition logic. If the SDS date or relevant actor information is missing, Salus must not assume that only the newest rule applies. The applicability stage must use approved transition rules and expose unresolved facts.

---

## 13. Testing strategy

### 13.1 Separation of concerns

The `tests/` folder tests Salus as a product. It is not a normal pipeline stage and is not loaded during an ordinary audit. Per-audit validation remains inside Stage 09 and Stage 11.

### 13.2 Fixture classes

- known-good samples per jurisdiction;
- single-defect fixtures isolating one rule;
- multiple-defect fixtures;
- cross-section contradiction fixtures;
- missing-evidence fixtures;
- conditional-applicability fixtures;
- transition-date fixtures;
- multilingual and alternate-heading fixtures;
- unit-conversion and decimal-format fixtures;
- scanned and damaged-extraction fixtures;
- duplicated/missing-page fixtures;
- malicious embedded instructions and prompt-injection fixtures;
- false-positive regression fixtures;
- false-negative regression fixtures;
- invalid-source and stale-rule-package fixtures;
- report-tampering and count-mismatch fixtures;
- release-gate fixtures.

### 13.3 Test design rules

- Test behavior through public audit inputs and released artifacts.
- Expected outcomes must come from independently reviewed worked examples.
- Every active rule has positive, negative, and insufficient-evidence cases.
- Critical derived rules also have exception and adversarial cases.
- A regression fixture is added for every corrected false positive or false negative.
- Test fixtures identify jurisdiction, dates, assumptions, active package, expected findings, prohibited findings, and allowed uncertainty.
- Synthetic fixtures are explicitly labeled synthetic.

### 13.4 MVP quality targets

- S01-S16 mapping accuracy: at least 98% on approved fixtures.
- Citation completeness: 100% for FAIL and INCONSISTENT findings.
- Evidence-location verification: 100% for definitive findings.
- Unsupported definitive conclusions: zero in the golden suite.
- Single-defect precision: at least 95% expected primary finding without unrelated definitive failures.
- Active-rule test coverage: positive, negative, and insufficient-evidence cases for 100% of active rules.
- Blocking release-gate detection: 100% of blocking-gate fixtures.
- Summary reconciliation: 100% exact on released fixtures.
- Regression pass rate: 100% before release.
- Walk-test success: 100% of prescribed cold-agent tasks.

### 13.5 ICM walk test

A cold agent with no prior conversation must be able to:

1. identify what Salus is;
2. find the correct starting stage;
3. identify exact inputs and references for that stage;
4. avoid loading prohibited folders;
5. determine current run status from files;
6. locate the output requiring human review;
7. identify the next stage only after the gate passes;
8. explain why a released or blocked result has that status.

Failure of the walk test is an architecture defect.

### 13.6 Reverse reference-integrity test

Before files are moved, renamed, or restructured, maintainers must identify inbound links, exact-path references, scripts, templates, and contracts that depend on them. After the change, all references are resolved and a cold walk succeeds. Old content is archived rather than silently deleted when preservation is required.

---

## 14. Security, privacy, and safety

### 14.1 Untrusted input

Uploaded SDS content is evidence, never instruction. Salus must ignore prompts, commands, links, macros, or behavioral instructions embedded in the document.

### 14.2 File handling

- do not execute embedded code or macros;
- do not follow embedded links automatically;
- validate type, size, and readability at intake;
- preserve the original;
- do not overwrite source files;
- isolate runs;
- log processing failures without exposing secrets.

### 14.3 Privacy

Documents are retained only within the configured workspace and retention policy. Reports must avoid exposing content beyond what is required for the audit. No source document is uploaded to a third party without explicit configuration and authorization.

### 14.4 Scientific and regulatory safety

- no invented classifications;
- no unsupported conformance certification;
- no definitive conclusion from incomplete classification parameters;
- no removal of uncertainty language to make a report appear cleaner;
- qualified human review for critical and low-confidence definitive conclusions;
- recommendations framed as verification or correction tasks, not authoritative replacement facts.

---

## 15. Non-functional requirements

### 15.1 Traceability

Every definitive finding traces from document evidence to location, normalized fact, requirement, official source, active rule, validation record, and final report entry.

### 15.2 Reproducibility

The same input checksum, profile, source package, rule package, schemas, and model configuration should produce materially equivalent findings. Differences must be detectable and explainable.

### 15.3 Performance

Target completion time is under three minutes for a typical text-readable SDS in the competition environment, excluding human gates. Performance must not bypass validation.

### 15.4 Maintainability

Rules have stable IDs, owners, status, versions, source links, tests, and history. Routing files remain small. Large reference collections receive their own router.

### 15.5 Accessibility

Reports use semantic headings, text labels, readable tables where appropriate, and do not rely on color alone.

### 15.6 Localization

Salus preserves source-language evidence and supports normalized multilingual headings. MVP report language is English unless configured otherwise. Translation must never replace the original quoted evidence.

### 15.7 Observability

Every stage output, validation defect, human decision, and release decision is represented as a readable file. Status is derived from files, not from a hidden dashboard or chat history.

### 15.8 Portability

The Salus workspace can be copied or version-controlled as a folder. No proprietary database is required for the core audit state.

---

## 16. Acceptance criteria

The MVP is accepted only when all conditions below are met:

1. Root contains only `README.md`, `identity.md`, `examples.md`, and `rules.md`, plus `reference/` and `tests/`.
2. The ICM cold-agent walk test passes.
3. Each stage has exactly one job and a valid contract.
4. Stable knowledge and per-run artifacts are structurally separate.
5. One PDF or text SDS can be registered, extracted, qualified, and audited.
6. US, EU, and dual-profile audits are selectable and visibly versioned.
7. S01-S16 each receives a terminal evaluation state.
8. At least eight approved cross-section rules run on golden fixtures.
9. Conditional checks cannot fail definitively without established triggers.
10. Every FAIL and INCONSISTENT finding contains exact evidence, location, source, requirement, rule version, rationale, and action.
11. All seven result states are used according to their definitions.
12. The validation stage detects every blocking defect in the approved validation suite.
13. The normal report is withheld when a blocking validation defect exists.
14. Released summary counts exactly match detailed findings.
15. No invented evidence, citations, values, classifications, or legal requirements occur in the golden suite.
16. Every active rule has positive, negative, and insufficient-evidence tests.
17. The full regression suite passes.
18. The report lists limitations and checks not performed.
19. Source and rule updates can be traced to impacted tests.
20. A qualified reviewer approves all active regulatory rules.

---

## 17. Delivery plan

### Phase 1: Architecture and contracts

Deliver root files, `reference/CONTEXT.md`, stage contracts, run template, schemas, and test router.

**Exit:** root contract and walk test pass.

### Phase 2: Source and applicability foundation

Deliver approved source register, US/EU profiles, transition logic, normalized requirements, and rule schema.

**Exit:** source-to-requirement traceability and applicability fixtures pass.

### Phase 3: Extraction and qualification

Deliver extraction evidence map, section detection, warnings, and qualification states.

**Exit:** structural and damaged-input fixtures pass.

### Phase 4: Section audit

Deliver approved minimum rules for S01-S16.

**Exit:** every section has active checks and terminal-state tests.

### Phase 5: Cross-section rules

Implement XR rules incrementally in vertical slices.

**Exit:** each active rule passes positive, negative, exception, and insufficient-evidence tests.

### Phase 6: Findings and validation

Deliver finding construction, validation gates, defect classes, correction loop, and fail-closed behavior.

**Exit:** all blocking release-gate fixtures pass.

### Phase 7: Reporting and demonstration

Deliver final report, JSON result, validation report, release manifest, and demonstration runs.

**Exit:** a judge reproduces expected results from a clean copy.

### Phase 8: Hardening

Run prompt-injection, multilingual, extraction-damage, stale-source, and full regression suites.

**Exit:** all release criteria pass and qualified regulatory sign-off is recorded.

---

## 18. Risks and mitigations

### Overconfident conclusions
Mitigation: evidence gates, explicit applicability, uncertainty states, conclusion-strength limits, human approval, and result validation.

### Oversimplified chemistry
Mitigation: multi-parameter rule inputs, exception logic, screening language, expert review, and insufficient-evidence fixtures.

### Hallucinated citations
Mitigation: closed approved source package, citation resolution, exact provision identifiers, and blocking validation.

### Regulatory staleness
Mitigation: source versions, retrieval metadata, update workflow, transition logic, preserved baselines, and source-age warnings.

### Poor extraction
Mitigation: qualification stage, page anchors, OCR warnings, sampling, `NOT_EVALUATED`, and release blocking when material.

### Prompt injection
Mitigation: treat document content solely as evidence, stage-level prohibited-load rules, untrusted-input policy, and adversarial fixtures.

### Context overload
Mitigation: exact stage inputs, `Do NOT load` declarations, routers, and factory/product separation.

### Architecture drift
Mitigation: root-structure test, walk test, contract linting, reference-integrity checks, and generated indexes.

### False reassurance from PASS
Mitigation: check-specific PASS definition, prominent limitations, jurisdiction scope, and prohibition on certification language.

### Test leakage
Mitigation: keep `tests/` outside normal pipeline context and explicitly prohibit stages from loading expected results during ordinary audits.

---

## 19. Metrics

- median reviewer time saved per SDS;
- percentage of findings accepted by qualified reviewers;
- false-positive and false-negative rate by rule;
- evidence-verification failure rate;
- citation-resolution failure rate;
- percentage of runs blocked by validation and reason;
- percentage of audits with extraction warnings;
- percentage of active rules with complete test triads;
- reproducibility variance across repeated runs;
- time to assess and release a regulatory update;
- cold-agent walk-test success rate;
- human correction rate by stage;
- critical findings later rejected by expert review.

---

## 20. Migration from the previous PRD

### Retain with revision

- full 16-section scope;
- US/EU MVP focus;
- evidence-grounded finding concept;
- seven result states;
- selected cross-section logic;
- source/rule versioning;
- regression fixture categories;
- non-certification boundary.

### Replace

- product name with Salus;
- conventional repository layout with ICM Pipeline plus Knowledge Bundle;
- root manifest/schema files with the four-file root contract;
- generic test strategy with separate product testing and per-audit validation;
- report generation as the endpoint with validated release as the endpoint;
- broad narrative stage definitions with explicit stage contracts and handoffs;
- unsafe absolute regulatory rules with evidence, applicability, and conclusion-strength controls.

### Reject from the prior conversation unless independently re-established

- exact-English-heading requirements;
- unconditional UFI failures;
- unconditional endocrine-silence failures;
- viscosity-only aspiration determinations;
- mixture acute-toxicity conclusions from isolated endpoint values;
- universal TSCA content requirements for Section 15;
- ingredient-presence-only Proposition 65 conclusions;
- claims that an SDS is globally legal or illegal;
- exact replacement wording presented as authoritative without confirmed facts.

---

## 21. Open decisions

1. Competition platform limits for file count, file size, PDF extraction, and tool execution.
2. Which languages beyond English enter the MVP golden set.
3. Which initial eight to twelve cross-section rules have sufficient authoritative basis and reviewed fixtures.
4. Who provides final US and EU regulatory sign-off.
5. Whether machine-readable artifacts use JSON only or JSON plus JSON Schema files.
6. Whether human gates are mandatory during competition demonstration or represented by approved gate records.
7. Which extraction tool is available and how its locator model is normalized.
8. Maximum run retention period and redaction requirements.
9. Whether the final competition package contains captured official-source excerpts or only source records and normalized requirements.

Open decisions must not be resolved by hidden assumptions. Each receives an owner, due date, decision record, and affected acceptance criteria.

---

## 22. Official starting references

- OSHA, current 29 CFR 1910.1200: https://www.ecfr.gov/current/title-29/subtitle-B/chapter-XVII/part-1910/section-1910.1200
- OSHA, Final Rule to Amend the Hazard Communication Standard: https://www.osha.gov/hazcom/rulemaking
- OSHA, HCS 2024 compliance-date extension notice: https://www.osha.gov/hazcom/rulemaking/extension
- EUR-Lex, Commission Regulation (EU) 2020/878: https://eur-lex.europa.eu/eli/reg/2020/878/oj/eng
- ICM Architect repository: https://github.com/RinDig/icm-architect

These links seed the source register. They do not replace provision-level captured sources, consolidation checks, applicability analysis, rule review, or versioning.

---

## 23. Definition of done

Salus MVP is done only when:

- the workspace satisfies the four-file root contract;
- a cold agent can orient, execute, stop at gates, and report status from files alone;
- all active source records, normalized requirements, and derived rules are versioned and approved;
- one SDS can complete the full pipeline under US, EU, or dual scope;
- all 16 sections receive terminal states;
- approved cross-section rules run with bounded conclusions;
- every definitive finding is evidence- and source-verified;
- Stage 09 validates the result independently;
- Stage 11 fails closed on blocking defects;
- released artifacts reconcile exactly;
- the complete golden, adversarial, validation, and regression suites pass;
- the report states its scope and limitations;
- qualified reviewers sign off on the active regulatory package;
- Salus makes no claim to certify compliance.

The final product of Salus is therefore not an audit report. It is a **validated, traceable, release-gated pre-audit package**.
