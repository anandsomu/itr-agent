#!/usr/bin/env python3
"""Graphical memory board for all PANs.

Reads every pans/<PAN>/state.json and prints a compact, low-token progress
board so the agent can see the whole picture at a glance without re-reading or
grepping the full JSON. Run at session start; open the full state.json only
when a specific detail is needed.

Usage:
  python3 pans/dashboard.py            # print board for all PANs
  python3 pans/dashboard.py <PAN>      # print board + detail for one PAN
  python3 pans/dashboard.py --write    # also refresh pans/DASHBOARD.md
"""
import json, sys, glob, os

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = ["S0","S1","S2","S3","S4","S5","S6","S7","S8","S9","S10","S11","S12","S13"]
STEP_NAMES = {
    "S0":"Form","S1":"Ingest","S2":"Salary","S3":"CapGains","S4":"VDA",
    "S5":"OtherSrc","S6":"AIS-recon","S7":"Losses","S8":"Regime",
    "S9":"Deduct/Tax","S10":"Assemble","S11":"Validate","S12":"Review","S13":"Prove",
}
GLYPH = {"done":"✓","in_progress":"◐","blocked":"■","todo":"·","na":"–"}


def load_all():
    out = []
    for p in sorted(glob.glob(os.path.join(HERE, "*", "state.json"))):
        try:
            out.append((os.path.basename(os.path.dirname(p)), json.load(open(p))))
        except Exception as e:
            out.append((os.path.basename(os.path.dirname(p)), {"_error": str(e)}))
    return out


def inr(n):
    if n is None:
        return "?"
    try:
        return "₹" + format(int(round(n)), ",")
    except Exception:
        return str(n)


def step_strip(d):
    cells = []
    for s in STEPS:
        st = d.get("steps", {}).get(s, {}).get("status", "todo")
        cells.append(f"{s}{GLYPH.get(st,'?')}")
    return " ".join(cells)


def next_step(d):
    for s in STEPS:
        st = d.get("steps", {}).get(s, {}).get("status", "todo")
        if st in ("todo", "in_progress", "blocked"):
            return s, st
    return None, None


def board(pans):
    lines = []
    lines.append("ITR MEMORY BOARD  (legend: ✓done ◐wip ■blocked ·todo –n/a)")
    lines.append("=" * 68)
    for name, d in pans:
        if d.get("_error"):
            lines.append(f"{name}: ERROR {d['_error']}")
            continue
        fig = d.get("figures", {})
        sal = fig.get("salary", {}).get("gross_17_1")
        os_t = fig.get("os", {}).get("total_os")
        tax = fig.get("taxes_paid", {}).get("total_current_year")
        oq = len(d.get("open_questions", []))
        ns, nst = next_step(d)
        done = sum(1 for s in STEPS if d.get("steps", {}).get(s, {}).get("status") == "done")
        lines.append("")
        lines.append(f"● {name}  {d.get('assessee_name','?')}  [{d.get('form','?')}, AY {d.get('ay','?')}]  regime:{d.get('regime',{}).get('choice','?')}")
        lines.append(f"  progress {done}/{len(STEPS)} steps   next: {ns} {STEP_NAMES.get(ns,'')} ({nst})   open-Qs: {oq}")
        lines.append(f"  {step_strip(d)}")
        lines.append(f"  salary {inr(sal)} | other-src {inr(os_t)} | taxes-paid {inr(tax)} | json {d.get('current_json') or '—'}")
    lines.append("")
    lines.append("Detail: python3 pans/dashboard.py <PAN>  |  full: pans/<PAN>/state.json")
    return "\n".join(lines)


def detail(name, d):
    lines = [board([(name, d)]), "", f"── DETAIL: {name} ──"]
    lines.append("Open questions:")
    for q in d.get("open_questions", []):
        lines.append(f"  [{q.get('id')}] ({q.get('blocking_step')}) {q.get('question')}")
    lines.append("Recent history:")
    for h in d.get("history", [])[-5:]:
        lines.append(f"  {h.get('when')}: {h.get('event')}")
    lines.append("Decisions:")
    for dec in d.get("decisions", []):
        lines.append(f"  {dec.get('when')}: {dec.get('what')} — {dec.get('why')}")
    return "\n".join(lines)


def main():
    args = [a for a in sys.argv[1:]]
    write = "--write" in args
    args = [a for a in args if a != "--write"]
    pans = load_all()
    if args:
        name = args[0]
        match = [(n, d) for n, d in pans if n == name]
        text = detail(*match[0]) if match else f"No state for PAN {name}"
    else:
        text = board(pans)
    print(text)
    if write:
        with open(os.path.join(HERE, "DASHBOARD.md"), "w") as f:
            f.write("```\n" + board(pans) + "\n```\n")
        print("\n[wrote pans/DASHBOARD.md]")


if __name__ == "__main__":
    main()
