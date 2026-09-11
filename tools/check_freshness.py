#!/usr/bin/env python3
"""Is the copy of each standard in reference/ still the one in force?

    python3 tools/check_freshness.py            # needs network
    python3 tools/check_freshness.py --report   # print what the ledger already knows, no network

Salus is built to run with no network, and this script is the reason that is not the same as
running blind. When there IS a connection, this asks the publishers what exists now and writes
the answer into reference/FRESHNESS-LOG.md with a date. When there is not, the audit reads that
log and knows both what it knew and HOW OLD that knowledge is — which is a different thing from
knowing nothing.

It never edits STANDARDS-LEDGER.md. Deciding that a newly published revision is now in force is a
legal reading, not a string comparison, and it belongs to a person.

A PROBE THAT DID NOT GET AN ANSWER IS NOT AN ANSWER. This script once wrote "no newer consolidated
version found" and `action: none` after every one of its probes had failed, because a dead network
and a publisher saying "that version does not exist" both arrived here as an empty list. That line
goes into FRESHNESS-LOG.md and `rules.md` Stage 3 requires a report to cite it, so the script would
have been putting a claim it never established into a compliance record. Now a probe that gets no
HTTP answer at all raises `Unreachable`, every target counts its failures, and a target with any
failure is written down as UNREACHABLE — could not establish — rather than as a clean result.

EXIT CODE. 0 when every target was reached and the log records a real answer. 1 when any target
could not be reached: the log is still written, and it says UNREACHABLE, but the run did not
establish what it set out to establish and must not be read as though it had. `--report` exits 0;
it makes no claim of its own, it prints the one on record.
"""
import argparse, datetime, json, os, re, sys, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "reference", "STANDARDS-LEDGER.md")
LOG = os.path.join(ROOT, "reference", "FRESHNESS-LOG.md")

TARGETS = [
    {"name": "EU — Commission Regulation (EU) 2020/878",
     "held": "32020R0878",
     "probe": "http://publications.europa.eu/resource/celex/32020R0878",
     "note": "The act itself is not amended; what changes is the consolidated Annex II it "
             "produced. A later amending act would appear as a new CELEX number."},
    {"name": "EU — CLP Annex VI (Regulation (EC) No 1272/2008, consolidated)",
     "held": "02008R1272-20260701",
     "probe": "http://publications.europa.eu/resource/celex/02008R1272-20260701",
     "candidates": True,
     "note": "Annex VI is amended by ATP regulations several times a year. A newer consolidated "
             "version means the Table 3 extract in reference/ is stale."},
    {"name": "California — Proposition 65 statute (HSC chapter 6.6)",
     "held": "added 1986-11-04 by initiative; sections as served on 2026-09-12",
     "probe": "https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml"
              "?lawCode=HSC&division=20.&title=&part=&chapter=6.6.&article=",
     "note": "The statute is amended by ordinary legislation and each section carries its own "
             "enactment note, so a change shows up as a changed section rather than as a new "
             "version number. This probe says the chapter is still served; it does not say the "
             "text is unchanged — tools/build_reference.py and the output hash do."},
    {"name": "US — 29 CFR 1910.1200",
     "held": "eCFR point-in-time 2026-09-01",
     "probe": "https://www.ecfr.gov/api/versioner/v1/versions/title-29.json?part=1910&section=1910.1200",
     "note": "eCFR reports the date of the latest amendment to the section."},
]


class Unreachable(Exception):
    """No HTTP answer at all. Deliberately distinct from an answer that says "not found": 404 is
    the publisher telling us something, and a refused connection is the publisher telling us
    nothing. Conflating the two is how this script came to report a silence as a confirmation."""


def get(url, accept):
    """urllib first, curl as the fallback: an interpreter without a CA bundle must not be the
    reason this folder stops being able to check whether its standards are current. If neither
    produces an HTTP status, that is Unreachable and the caller has to say so."""
    headers = {"User-Agent": "Salus/1.0", "Accept": accept, "Accept-Language": "eng"}
    first = None
    try:
        req = urllib.request.Request(url, headers={**headers, "Accept-Encoding": "gzip"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
            if r.headers.get("Content-Encoding") == "gzip":
                import gzip
                data = gzip.decompress(data)
            return r.status, data
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:
        first = f"{type(e).__name__}: {str(e)[:100]}"

    import subprocess
    hs = []
    for k, v in headers.items():
        hs += ["-H", f"{k}: {v}"]
    try:
        r = subprocess.run(["curl", "-sS", "-L", "--compressed", "-m", "60",
                            "-w", "\n%{http_code}", *hs, url],
                           capture_output=True, timeout=120)
    except Exception as e:
        raise Unreachable(f"urllib: {first}; curl: {type(e).__name__}") from e
    body = r.stdout
    code = 0
    if b"\n" in body:
        body, tail = body.rsplit(b"\n", 1)
        try:
            code = int(tail.strip())
        except ValueError:
            code = 0
    if code == 0:
        raise Unreachable(f"urllib: {first}; curl exit {r.returncode}: "
                          f"{r.stderr.decode('utf-8', 'replace').strip()[:100]}")
    return code, body


def probe_consolidated(base_celex):
    """Ask for consolidated versions dated after the one held. Cellar answers 404 for a version
    that does not exist, which is the whole test — and that is exactly why a probe that gets no
    answer cannot be folded in with one that does. Returns (found, failed, probed): an empty
    `found` means "none exists" only when `failed` is zero."""
    stem = base_celex.split("-")[0]
    held = base_celex.split("-")[1]
    held_d = datetime.date(int(held[:4]), int(held[4:6]), int(held[6:]))
    found, failed, probed = [], 0, 0
    d = held_d
    today = datetime.date.today()
    # consolidated versions start on the 1st or the 20th of a month; probe month starts
    while d < today:
        d = (d.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
        if d > today:
            break
        cand = f"{stem}-{d.strftime('%Y%m%d')}"
        probed += 1
        try:
            st, _ = get(f"http://publications.europa.eu/resource/celex/{cand}",
                        "application/xhtml+xml")
        except Exception:
            failed += 1
            continue
        if st == 200:
            found.append(cand)
        elif st != 404:
            # neither "here it is" nor "it does not exist" — we have not been told either way
            failed += 1
    return found, failed, probed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true", help="no network; print what is on record")
    a = ap.parse_args()
    today = datetime.date.today().isoformat()

    if a.report:
        if os.path.exists(LOG):
            sys.stdout.write(open(LOG, encoding="utf-8").read())
        else:
            print("No freshness log on record. Run this script with a connection at least once.")
        return 0

    NOT_ESTABLISHED = ("none possible now — this run did not establish whether a newer version "
                       "exists; the ledger's last confirmed date stands and the audit must say so")

    rows, unreached = [], 0
    for t in TARGETS:
        entry = {"standard": t["name"], "held": t["held"], "checked": today}
        try:
            if t.get("candidates"):
                newer, failed, probed = probe_consolidated(t["held"])
                if failed:
                    # The whole point of H10: an empty result list from failed probes is silence,
                    # not a finding of "nothing newer". Never write it down as one.
                    raise Unreachable(f"{failed} of {probed} probe(s) got no usable answer from "
                                      f"the publisher")
                entry["result"] = ("NEWER CONSOLIDATED VERSION EXISTS: " + ", ".join(newer)
                                   if newer else
                                   f"no newer consolidated version found ({probed} probe(s), all "
                                   f"answered)")
                entry["action"] = ("rebuild reference/ against the newest one and re-read the "
                                   "Table 3 extract" if newer else "none")
            else:
                st, data = get(t["probe"], "application/json,application/xhtml+xml")
                if st >= 400:
                    raise Unreachable(f"the publisher answered HTTP {st}")
                entry["result"] = f"reachable, HTTP {st}"
                if "ecfr" in t["probe"]:
                    j = json.loads(data)
                    dates = sorted({v.get("date", "") for v in j.get("content_versions", [])})
                    if not dates:
                        raise Unreachable("eCFR answered, but reported no version dates for this "
                                          "section — the amendment date was not established")
                    entry["result"] = f"latest amendment date reported by eCFR: {dates[-1]}"
                    # The held date comes off this target's own "held" string and is not
                    # written here a second time: one fact, one writer. A literal here was the
                    # third copy of the snapshot date in this folder.
                    held_date = re.search(r"\d{4}-\d{2}-\d{2}", t["held"]).group()
                    entry["action"] = ("re-run tools/build_reference.py — the held "
                                       "snapshot is older than the latest amendment"
                                       if dates[-1] > held_date else "none")
                entry.setdefault("action", "none")
        except Exception as e:
            unreached += 1
            detail = str(e)[:160] if isinstance(e, Unreachable) else f"{type(e).__name__}: {str(e)[:120]}"
            entry["result"] = (f"UNREACHABLE — could not establish whether a newer version exists "
                               f"({detail})")
            entry["action"] = NOT_ESTABLISHED
        rows.append(entry)
        print(f"{t['name']}\n  held    : {entry['held']}\n  result  : {entry['result']}\n"
              f"  action  : {entry['action']}\n")

    body = ["# Freshness log", "",
            "Written by `tools/check_freshness.py`. This file is the memory an offline run reads:",
            "it says what was true the last time this folder could reach the publishers, and when",
            "that was. It does not change `STANDARDS-LEDGER.md` — promoting a published revision to",
            "'in force' is a legal reading and belongs to a person.", "",
            f"Last run: **{today}**", ""]
    for e in rows:
        body += [f"## {e['standard']}", "",
                 f"- held in `reference/`: `{e['held']}`",
                 f"- checked: {e['checked']}",
                 f"- result: {e['result']}",
                 f"- action: {e['action']}", ""]
    body += ["---", "",
             "If this log is old, an audit run today does not silently pretend otherwise. "
             "`rules.md` Stage 3 requires the report to state the date above, so a reader always "
             "knows how fresh the auditor's knowledge of the calendar was.", ""]
    if unreached:
        body[body.index(f"Last run: **{today}**")] = (
            f"Last run: **{today}** — **INCOMPLETE**: {unreached} of {len(TARGETS)} target(s) "
            f"could not be reached. What is recorded for those is that nothing was established, "
            f"which is not the same as nothing having changed.")
    open(LOG, "w", encoding="utf-8").write("\n".join(body))
    print(f"wrote {os.path.relpath(LOG, ROOT)}")
    if unreached:
        print(f"UNREACHABLE: {unreached} of {len(TARGETS)} target(s) gave no usable answer. "
              f"This run did not establish that the held standards are current — it established "
              f"only that it could not ask. Exit 1.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
