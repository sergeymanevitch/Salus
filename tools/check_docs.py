#!/usr/bin/env python3
"""Hold the documents to the folder they describe: the diagrams, and the facts written twice.

    python3 tools/check_docs.py            # diagrams, the check sequence, the revisions
    python3 tools/check_docs.py --render   # also render both diagrams, if mermaid-cli is here

A diagram is a claim like any other, and until this script existed it was the only kind of claim
in this folder that nothing checked. Both diagrams in README.md drifted for a day: the run
flowchart still showed the three gates of one morning, and the maintenance diagram had not been
touched since before Gate 0 existed. Neither was caught by a gate. They were caught by eye.

It began as check_diagrams.py and was renamed when it grew the revision check below: the job is
not the pictures, it is every fact this folder states in more than one place.

This is a documentation gate, not an audit gate. Nothing here reads a sheet. Run it after editing
README.md, rules.md, or tools/CONTEXT.md.

WHAT IT PROVES

1.  The diagrams are structurally sound: every node an edge names is defined, every id a class
    line names is a node, every class is declared, no id is defined twice with two labels, and
    **no decision node is a dead end**. A diamond with arrows in and none out is a decision with
    no consequence, which is how Gate 0 was first drawn into the second diagram.
2.  Every script a diagram names exists in tools/.
3.  The four places that state the sequence of checks agree with each other:
        - README.md, the run flowchart               (CHECK n, and the script under it)
        - README.md, "The gates, one at a time"      (the numbered command block)
        - rules.md, "Before the report leaves"       (the numbered command block)
        - tools/CONTEXT.md, the ordered table        (which scripts are gates at all)
    It does not decide which of them is right. It refuses to let them disagree, because a reader
    who finds two answers has no way to tell which one the code does.
4.  Every script in tools/ is named in both README.md and tools/CONTEXT.md, and the count
    tools/CONTEXT.md opens with is the number of scripts actually there.
5.  Every revision this folder names is the revision it downloaded. The owner of that fact is
    reference/<standard>/PROVENANCE.md, which is generated output and hashed by Gate 0 — not
    prose, and not a constant in a script. A CELEX id or an eCFR point-in-time date written in
    README.md, rules.md, the ledger, the freshness log or any script must be one of those, and
    every one of those must appear in the ledger. The revision id 02008R1272-20260701 had three
    writers across five locations and no owner; a builder pointing at a revision the folder does
    not hold is the way that ends badly.

WHAT IT DOES NOT PROVE

It does not render the diagrams unless --render is passed and mermaid-cli is installed; without
that, "this is valid mermaid" is checked structurally and not by the renderer that will draw it.
And agreement is not truth: four documents can agree and all four be wrong about the code. What
this gate removes is the cheaper failure, where they quietly stop agreeing and nobody notices.

It compares the statements it knows about. A fifth statement of the same fact, in a file not
listed here, would drift unseen — which is the argument for not writing one.
"""
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Scripts that are not checks and must not appear in the run flowchart: the reporter, the two
# maintenance scripts, the settings reader, and the two gates that guard this repository rather
# than a sheet.
NOT_A_CHECK = {"extract.py", "build_reference.py", "check_freshness.py",
               "test_docs_example.py", "check_docs.py", "read_config.py"}

# What a revision id looks like in each publisher's vocabulary. CELEX numbers name an EU act and
# its consolidation date; the eCFR is a point in time and nothing else.
CELEX = re.compile(r"\b\d{5}[A-Z]\d{4}(?:-\d{8})?\b")
ECFR_DATE = re.compile(r"(?:eCFR point-in-time |versioner/v1/full/)(\d{4}-\d{2}-\d{2})")

# Everything that may state a revision. audits/ is deliberately absent: a filed report states the
# revision it was made under and keeps it, and Gate 2 checks that against the ledger already.
STATES_A_REVISION = ["README.md", "rules.md", "examples.md", "identity.md", "CLAUDE.md",
                     os.path.join("reference", "STANDARDS-LEDGER.md"),
                     os.path.join("reference", "FRESHNESS-LOG.md")]

NUMBER_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
                "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}

NODE_DEF = re.compile(r"\b(\w+)([\[\{\(])\"(.*?)\"[\]\}\)]")
EDGE = re.compile(r"\b(\w+)\s*(?:--+>|-\.-*->|--+|===+>)\s*(?:\|(?:\"[^\"]*\"|[^|]*)\|\s*)?(\w+)\b")
CLASS_LINE = re.compile(r"^\s*class\s+([\w, ]+)\s+(\w+)\s*$", re.M)
CLASSDEF_LINE = re.compile(r"^\s*classDef\s+(\w+)\b", re.M)
SCRIPT = re.compile(r"\b([a-z_]+\.py)\b")


def read(*parts):
    return open(os.path.join(ROOT, *parts), encoding="utf-8").read()


def mermaid_blocks(text):
    return re.findall(r"```mermaid\n(.*?)```", text, re.S)


def parse_block(block):
    """Return (nodes, edges, skeleton). Nodes map id -> label; a node may be defined inline at
    either end of an edge, so definitions are collected first and blanked out before edges are
    read — otherwise a label containing an arrow would be parsed as one."""
    nodes = {}
    dupes = []
    for ident, _open, label in NODE_DEF.findall(block):
        if ident in nodes and nodes[ident] != label:
            dupes.append(ident)
        nodes[ident] = label
    skeleton = NODE_DEF.sub(lambda m: m.group(1), block)
    edges = []
    for line in skeleton.split("\n"):
        line = line.strip()
        if not line or line.startswith(("classDef", "class ", "%%", "flowchart", "subgraph", "end")):
            continue
        edges.extend(EDGE.findall(line))
    return nodes, edges, dupes


def check_structure(block, n, problems):
    nodes, edges, dupes = parse_block(block)
    where = f"diagram {n}"

    for ident in dupes:
        problems.append(f"{where}: node `{ident}` is defined twice with two different labels — "
                        "mermaid keeps the first and the second silently does nothing")

    if block.count('"') % 2:
        problems.append(f"{where}: an odd number of quotation marks — a label is left open")

    connected = set()
    for src, dst in edges:
        connected.update((src, dst))
        for ident in (src, dst):
            if ident not in nodes:
                problems.append(f"{where}: edge names `{ident}`, which is never defined — "
                                "mermaid draws a bare box, so a typo becomes a new node")

    for ident in nodes:
        if ident not in connected:
            problems.append(f"{where}: node `{ident}` is defined and never connected to anything")

    # The rule this gate was written after. A rectangle with no way out is a terminal and is
    # fine — CANNOT VERIFY, VOID, delivered. A diamond with no way out is a decision whose
    # outcomes are not drawn, which is how Gate 0 first entered the maintenance diagram: four
    # arrows in, none out. Either draw what it decides, or do not draw it as a decision.
    outgoing = {src for src, _ in edges}
    for ident, label in nodes.items():
        if re.search(r"\b" + re.escape(ident) + r"\{", block) and ident not in outgoing:
            head = label.split("<br/>")[0]
            problems.append(f"{where}: `{ident}` ({head}) is a decision with no outgoing edge — "
                            "a gate that decides nothing. Draw its outcomes, or draw it as a step")

    declared = set(CLASSDEF_LINE.findall(block))
    for idents, name in CLASS_LINE.findall(block):
        if name not in declared:
            problems.append(f"{where}: class `{name}` is applied but never declared with classDef")
        for ident in [i.strip() for i in idents.split(",") if i.strip()]:
            if ident not in nodes:
                problems.append(f"{where}: class line names `{ident}`, which is not a node here")
    return nodes


def held_revisions():
    """What the folder actually downloaded, read off the provenance records. These files are
    generated by build_reference.py and rehashed by Gate 0, so this is the one statement of the
    fact that cannot be edited without a gate noticing."""
    held = set()
    for prov in sorted(glob.glob(os.path.join(ROOT, "reference", "*", "PROVENANCE.md"))):
        text = open(prov, encoding="utf-8").read()
        held |= set(CELEX.findall(text)) | set(ECFR_DATE.findall(text))
    return held


def check_revisions(problems):
    held = held_revisions()
    if not held:
        problems.append("no PROVENANCE.md under reference/ names a revision — either the corpus "
                        "was never built, or the records that own that fact are gone")
        return
    ledger_path = os.path.join(ROOT, "reference", "STANDARDS-LEDGER.md")
    ledger = open(ledger_path, encoding="utf-8").read() if os.path.exists(ledger_path) else ""

    for name in STATES_A_REVISION + [os.path.join("tools", os.path.basename(p))
                                     for p in sorted(glob.glob(os.path.join(ROOT, "tools", "*.py")))]:
        path = os.path.join(ROOT, name)
        if not os.path.exists(path):
            continue
        text = open(path, encoding="utf-8").read()
        for said in sorted(set(CELEX.findall(text)) | set(ECFR_DATE.findall(text))):
            if said not in held:
                problems.append(
                    f"{name} names revision `{said}`, which is not what this folder downloaded. "
                    f"reference/*/PROVENANCE.md records " + ", ".join(sorted(held))
                    + " — a document naming a revision the corpus does not hold sends a reader "
                      "to a text that is not there")
    for revision in sorted(held):
        if revision not in ledger:
            problems.append(
                f"the corpus holds revision `{revision}` and reference/STANDARDS-LEDGER.md never "
                "names it. The ledger is where a person decides which revision is in force; a "
                "revision that arrives without being written up there is in force by accident")


def numbered_commands(text, heading, stop):
    """Read a block of `python3 tools/<script>  # n · …` lines out of a documented section."""
    if heading not in text:
        return None
    body = text[text.index(heading):]
    body = body[:body.index(stop)] if stop in body else body
    found = {}
    for script, num in re.findall(r"python3 tools/([a-z_]+\.py).*?#\s*(\d+)\s*·", body):
        found[int(num)] = script
    return found


def main(argv):
    problems = []
    readme = read("README.md")
    rules = read("rules.md")
    context = read("tools", "CONTEXT.md")

    blocks = mermaid_blocks(readme)
    if len(blocks) < 2:
        print(f"FAIL  README.md holds {len(blocks)} mermaid diagram(s); the file describes two")
        return 1

    named_scripts = set()
    flow_checks = {}
    check_numbers_seen = set()
    for i, block in enumerate(blocks, 1):
        nodes = check_structure(block, i, problems)
        for label in nodes.values():
            named_scripts.update(SCRIPT.findall(label))
            num = re.search(r"CHECK (\d+)", label)
            if num:
                check_numbers_seen.add(int(num.group(1)))
                scripts = SCRIPT.findall(label)
                if not scripts:
                    problems.append(f"diagram {i}: a node says CHECK {num.group(1)} and names no "
                                    "script — the number is the only thing a reader can check")
                else:
                    flow_checks[int(num.group(1))] = scripts[0]
        # An edge label may refer to a check without renaming its script ("CHECK 3 above"), but
        # the number it names has to be one that exists.
        for num in re.findall(r"CHECK (\d+)", block):
            check_numbers_seen.add(int(num))
        named_scripts.update(SCRIPT.findall(block))

    for script in sorted(named_scripts):
        if not os.path.exists(os.path.join(ROOT, "tools", script)):
            problems.append(f"a diagram names tools/{script}, which does not exist")

    readme_list = numbered_commands(readme, "## The gates, one at a time", "\nRun them from any")
    rules_list = numbered_commands(rules, "## Before the report leaves", "\nChecks 1 and 2 are not")
    if readme_list is None:
        problems.append("README.md § 'The gates, one at a time' is gone — the heading moved")
    if rules_list is None:
        problems.append("rules.md § 'Before the report leaves' is gone — the heading moved")

    statements = {"the run flowchart": flow_checks,
                  "README.md § The gates, one at a time": readme_list,
                  "rules.md § Before the report leaves": rules_list}
    baseline = flow_checks
    for name, other in statements.items():
        if other is None or other == baseline:
            continue
        for num in sorted(set(baseline) | set(other)):
            if baseline.get(num) != other.get(num):
                problems.append(
                    f"check {num} is `{baseline.get(num) or 'absent'}` in the run flowchart and "
                    f"`{other.get(num) or 'absent'}` in {name}")

    stray = sorted(n for n in check_numbers_seen if n not in baseline)
    for num in stray:
        problems.append(f"a diagram refers to CHECK {num}, which no node defines")

    # tools/CONTEXT.md decides which scripts are gates at all; the diagram decides their order.
    gates_in_context = set()
    for row in re.findall(r"^\|[^|]*\|\s*`([a-z_]+\.py)`\s*\|(.*)$", context, re.M):
        script, job = row
        if re.search(r"\*\*(Gate \d|the scope gate)\*\*", job):
            gates_in_context.add(script)
    missing = gates_in_context - set(baseline.values())
    for script in sorted(missing):
        problems.append(f"tools/CONTEXT.md calls tools/{script} a gate and no numbered check "
                        "names it — the run flowchart does not show it")
    extra = set(baseline.values()) - gates_in_context
    for script in sorted(extra):
        problems.append(f"the checks name tools/{script}; tools/CONTEXT.md does not list it "
                        "as a gate")

    on_disk = {os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "tools", "*.py"))}
    for script in sorted(on_disk):
        for doc, text in (("README.md", readme), ("tools/CONTEXT.md", context)):
            if script not in text:
                problems.append(f"tools/{script} exists and {doc} never names it")
    for script in sorted(set(baseline.values()) & NOT_A_CHECK):
        problems.append(f"tools/{script} is not a check and is numbered as one")

    count = re.search(r"^(\w+) scripts\.", context, re.M)
    if not count:
        problems.append("tools/CONTEXT.md no longer opens with a count of the scripts")
    else:
        claimed = NUMBER_WORDS.get(count.group(1).lower())
        if claimed != len(on_disk):
            problems.append(f"tools/CONTEXT.md opens '{count.group(1)} scripts' and tools/ holds "
                            f"{len(on_disk)}")

    check_revisions(problems)

    rendered = ""
    if "--render" in argv:
        rendered = render(blocks, problems)

    problems = list(dict.fromkeys(problems))   # two edges naming one missing node say it once
    if problems:
        for p in problems:
            print(f"FAIL  {p}")
        print(f"\n{len(problems)} problem(s). A document that disagrees with the folder is worse "
              "than no document: it is read and believed.")
        return 1

    print(f"  OK  {len(blocks)} diagram(s): every node connected, every decision has an outcome, "
          f"every script named exists")
    print(f"  OK  checks 1–{max(baseline)} agree across the flowchart, README.md and rules.md: "
          + ", ".join(f"{n} {baseline[n]}" for n in sorted(baseline)))
    print(f"  OK  {len(on_disk)} script(s) in tools/, each named in README.md and tools/CONTEXT.md, "
          "and the count says so")
    print("  OK  every revision named anywhere here is one reference/*/PROVENANCE.md records, and "
          "the ledger names each: " + ", ".join(sorted(held_revisions())))
    if rendered:
        print(f"  OK  {rendered}")
    print("\nThe documents describe the folder that is here.")
    return 0


def render(blocks, problems):
    """Optional, and honest about being optional: mermaid-cli is a node package and a browser,
    neither of which this folder ships or needs."""
    mmdc = shutil.which("mmdc")
    if not mmdc:
        print("  --  --render: mermaid-cli (mmdc) is not installed; structure was checked, "
              "rendering was not")
        return ""
    with tempfile.TemporaryDirectory() as tmp:
        for i, block in enumerate(blocks, 1):
            src = os.path.join(tmp, f"d{i}.mmd")
            open(src, "w", encoding="utf-8").write(block)
            r = subprocess.run([mmdc, "-i", src, "-o", os.path.join(tmp, f"d{i}.svg")],
                               capture_output=True, text=True)
            if r.returncode != 0:
                tail = (r.stderr or r.stdout).strip().split("\n")[-1][:300]
                problems.append(f"diagram {i} does not render: {tail}")
    return f"{len(blocks)} diagram(s) rendered with mermaid-cli"


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
