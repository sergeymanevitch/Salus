#!/usr/bin/env python3
"""Read config/jurisdiction.md, and be the only place that knows how.

    python3 tools/read_config.py              # what this installation is set to, or fail by name
    python3 tools/read_config.py --config <path>

Four settings live in that file. Until this script existed, one of them was read by a script and
three were read by nobody: `check_scope.py` parsed `jurisdiction` and `policy_max_age_years`,
`organisation` and `run_date` were honoured because `rules.md` says to honour them. That is a rule,
and a rule is not a guard. `policy_max_age_years: five` is not a number; `run_date: 2027-01-01` ages
every sheet by four extra months; `jurisdiction: eu` is fine and `jurisdiction: EUR` is not, and a
model reading the file will often sail past all three because it can see what was meant.

So this parses the file, states what each setting resolves to, and fails by name when one of them
cannot be honoured as written. It is imported rather than copied: `check_scope.py` asks it which
regime is configured, and `validate_report.py` asks it what this installation's age policy is, so
there is one implementation of "what the settings say" and not three that drift (AD-15).

WHAT IT DOES NOT DO

It does not decide anything about a sheet, and it is not part of the gate chain. A setting can be
well formed and wrong — only the person filling the file in knows whether this installation audits
for a German legal entity or a US plant, which is the whole argument of `config/CONTEXT.md`.

It reads the first ```yaml block in the file, and the prose around that block is documentation for
a person. A key written outside the block is not configuration and is not read.
"""
import argparse
import datetime
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT = os.path.join(ROOT, "config", "jurisdiction.md")

REGIMES = {
    "EU": "Commission Regulation (EU) 2020/878, with CLP Annex VI for classification",
    "US": "29 CFR 1910.1200",
}


def _block(text):
    """The settings are the fenced yaml block. Everything else in that file is prose, and prose
    naming a key — "`jurisdiction` selects which standard" — is not a setting."""
    m = re.search(r"```ya?ml\n(.*?)```", text, re.S)
    return m.group(1) if m else text


def _value(block, key):
    m = re.search(rf"(?m)^\s*{key}\s*:\s*(.*)$", block)
    if not m:
        return None
    raw = m.group(1).split("#")[0].strip()
    return raw.strip("\"'")


def load(path=None):
    """Return (settings, problems). Settings carry what could be read; problems name what could
    not. Callers decide which problems stop them: the scope gate stops on the jurisdiction alone,
    because `rules.md` Stage 0 does, and reports the rest."""
    path = path or DEFAULT
    settings = {"path": path, "jurisdiction": None, "organisation": "",
                "policy_max_age_years": None, "run_date": None, "resolved_run_date": None}
    problems = []
    if not os.path.exists(path):
        return settings, [f"{path} does not exist — rules.md Stage 0: the run stops"]
    block = _block(open(path, encoding="utf-8", errors="replace").read())

    juris = _value(block, "jurisdiction")
    if not juris:
        problems.append(f"{path} names no jurisdiction")
    elif juris.upper() not in REGIMES:
        problems.append(f"{path} sets jurisdiction: {juris}, which is not a regime Salus ships "
                        "— EU or US, and there is no third value")
    else:
        settings["jurisdiction"] = juris.upper()

    settings["organisation"] = _value(block, "organisation") or ""

    age = _value(block, "policy_max_age_years")
    if age is None:
        problems.append(f"{path} names no policy_max_age_years — set it to your organisation's "
                        "rule, or to 0 to turn the age gate off. It has no default")
    elif not re.fullmatch(r"\d+", age):
        problems.append(f"{path} sets policy_max_age_years: {age}, which is not a whole number of "
                        "years. A gate that cannot read its own threshold does not run")
    else:
        settings["policy_max_age_years"] = int(age)

    run = _value(block, "run_date")
    today = datetime.date.today()
    if run is None:
        problems.append(f"{path} names no run_date — `auto` is the answer unless you are "
                        "reproducing a past run")
    elif run.lower() == "auto":
        settings["run_date"], settings["resolved_run_date"] = "auto", today
    else:
        try:
            when = datetime.date.fromisoformat(run)
        except ValueError:
            problems.append(f"{path} sets run_date: {run}, which is neither `auto` nor an ISO "
                            "date (YYYY-MM-DD)")
        else:
            settings["run_date"], settings["resolved_run_date"] = run, when
            if when > today:
                problems.append(f"{path} sets run_date: {run}, which is in the future. The age "
                                "gate and every transition window are measured from that day, so "
                                "a date not yet reached ages every sheet it reads")
    return settings, problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=None,
                    help="the settings file to read; defaults to config/jurisdiction.md beside "
                         "this script, not beside your working directory")
    a = ap.parse_args()
    path = os.path.abspath(a.config) if a.config else DEFAULT
    settings, problems = load(path)

    if problems:
        for p in problems:
            print(f"FAIL  {p}")
        print(f"\n{len(problems)} problem(s). This installation is not configured, and rules.md "
              "Stage 0 is what happens next: CANNOT VERIFY, and the run stops.")
        return 1

    regime = settings["jurisdiction"]
    org = settings["organisation"] or "(not set — the report header says so)"
    age = settings["policy_max_age_years"]
    print(f"  OK  jurisdiction: {regime} — {REGIMES[regime]}")
    print(f"  OK  organisation: {org}")
    print(f"  OK  policy_max_age_years: {age} — "
          + ("the age gate is off" if age == 0 else
             "house policy, resting on no provision; a finding it produces is marked "
             "[HOUSE POLICY — no provision] and names this number"))
    print(f"  OK  run_date: {settings['run_date']} → {settings['resolved_run_date'].isoformat()}")
    print("\nEvery setting can be honoured as written. What they decide is in rules.md Stage 0 "
          "and config/CONTEXT.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
