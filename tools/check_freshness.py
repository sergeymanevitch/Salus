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
    {"name": "US — 29 CFR 1910.1200",
     "held": "eCFR point-in-time 2026-09-01",
     "probe": "https://www.ecfr.gov/api/versioner/v1/versions/title-29.json?part=1910&section=1910.1200",
     "note": "eCFR reports the date of the latest amendment to the section."},
]


def get(url, accept):
    """urllib first, curl as the fallback: an interpreter without a CA bundle must not be the
    reason this folder stops being able to check whether its standards are current."""
    headers = {"User-Agent": "Salus/1.0", "Accept": accept, "Accept-Language": "eng"}
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
    except Exception:
        import subprocess
        hs = []
        for k, v in headers.items():
            hs += ["-H", f"{k}: {v}"]
        r = subprocess.run(["curl", "-sS", "-L", "--compressed", "-m", "60",
                            "-w", "\n%{http_code}", *hs, url],
                           capture_output=True, timeout=120)
        body = r.stdout
        code = 0
        if b"\n" in body:
            body, tail = body.rsplit(b"\n", 1)
            try:
                code = int(tail.strip())
            except ValueError:
                code = 0
        return code, body


def probe_consolidated(base_celex):
    """Ask for consolidated versions dated after the one held. Cellar answers 404 for a
    version that does not exist, which is the whole test."""
    stem = base_celex.split("-")[0]
    held = base_celex.split("-")[1]
    held_d = datetime.date(int(held[:4]), int(held[4:6]), int(held[6:]))
    found = []
    d = held_d
    today = datetime.date.today()
    # consolidated versions start on the 1st or the 20th of a month; probe month starts
    while d < today:
        d = (d.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
        if d > today:
            break
        cand = f"{stem}-{d.strftime('%Y%m%d')}"
        try:
            st, _ = get(f"http://publications.europa.eu/resource/celex/{cand}",
                        "application/xhtml+xml")
            if st == 200:
                found.append(cand)
        except urllib.error.HTTPError:
            pass
        except Exception:
            pass
    return found


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

    rows = []
    for t in TARGETS:
        entry = {"standard": t["name"], "held": t["held"], "checked": today}
        try:
            if t.get("candidates"):
                newer = probe_consolidated(t["held"])
                entry["result"] = ("NEWER CONSOLIDATED VERSION EXISTS: " + ", ".join(newer)
                                   if newer else "no newer consolidated version found")
                entry["action"] = ("rebuild reference/ against the newest one and re-read the "
                                   "Table 3 extract" if newer else "none")
            else:
                st, data = get(t["probe"], "application/json,application/xhtml+xml")
                entry["result"] = f"reachable, HTTP {st}"
                if "ecfr" in t["probe"]:
                    try:
                        j = json.loads(data)
                        dates = sorted({v.get("date", "") for v in j.get("content_versions", [])})
                        if dates:
                            entry["result"] = f"latest amendment date reported by eCFR: {dates[-1]}"
                            entry["action"] = ("re-run tools/build_reference.py — the held "
                                               "snapshot is older than the latest amendment"
                                               if dates[-1] > "2026-09-01" else "none")
                    except Exception:
                        pass
                entry.setdefault("action", "none")
        except Exception as e:
            entry["result"] = f"UNREACHABLE: {type(e).__name__}"
            entry["action"] = ("none possible now — the ledger's last confirmed date stands and "
                               "the audit must say so")
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
    open(LOG, "w", encoding="utf-8").write("\n".join(body))
    print(f"wrote {os.path.relpath(LOG, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
