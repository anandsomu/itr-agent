# ITR Agent — Prepare Indian Income-Tax Returns with Claude Code

**ITR Agent is an open-source [Claude Code](https://claude.com/claude-code) agent that helps you
prepare an Indian income-tax return from your own documents, one PAN at a time.** It works out
**which ITR form applies to you** (ITR-1, ITR-2, ITR-3, or ITR-4) from your income sources, reads
your Form 16, AIS, and TIS, reconciles every figure, computes your tax under the old and new
regimes, assembles a schema-valid ITR JSON, and walks you through finalizing it in the official
Income-Tax utility and filing it yourself.

It is a preparation and reconciliation assistant for Indian taxpayers and their helpers (family
members, friends, early-stage practitioners). **It assists only — it never logs in, files, pays, or
e-verifies on your behalf.** You review and submit everything.

---

## What it does

- **Picks the right form for you.** From your income sources it determines whether you should file
  **ITR-1 (Sahaj), ITR-2, ITR-3, or ITR-4 (Sugam)** — and flags when business/F&O activity means
  ITR-3, or when a case is beyond an individual return.
- **Ingests your documents** — Form 16, AIS (Annual Information Statement), TIS (Taxpayer
  Information Summary), the portal pre-filled JSON, broker capital-gains/P&L statements, and your
  prior-year return.
- **Reconciles every number** against AIS/TIS and flags mismatches (it treats AIS capital-gains cost
  data as unreliable and uses your broker statement as the source of truth).
- **Computes income and tax** across all heads — **Salary, House Property, Capital Gains (STCG/LTCG
  under s.111A / s.112A, grandfathering), Business/Profession, and Other Sources** — and compares
  the **old vs new regime**.
- **Handles foreign assets** — builds **Schedule FA** for overseas holdings (e.g. US stocks via
  INDmoney/Vested/IBKR), on the correct calendar-year basis, plus foreign dividends and FTC/Form 67.
- **Assembles a schema-valid ITR JSON** and validates it against the official Income-Tax Department
  schema for the chosen form with the bundled validator.
- **Guides the filing "last-mile"** — pay self-assessment tax, add the challan, generate the final
  file through the official offline utility (which stamps the required integrity hash), upload, and
  e-verify.

## Forms & scope

| Form | For | Status |
|---|---|---|
| **ITR-2** | Individuals/HUF with capital gains, foreign assets, multiple house properties, income > ₹50L (no business) | ✅ Most deeply validated path |
| **ITR-1 (Sahaj)** | Resident individuals ≤ ₹50L — salary, one house, other sources | Supported via the same SOP |
| **ITR-3** | Individuals/HUF with business/professional income (incl. F&O/intraday) — superset of ITR-2 + business schedules | Supported via the research protocol |
| **ITR-4 (Sugam)** | Presumptive business/profession (44AD/44ADA/44AE), ≤ ₹50L | Supported via the research protocol |

Every form follows the same step sequence and the same filing last-mile; form-specific schedules
(e.g. ITR-3's Business & Profession / P&L / Balance Sheet) are handled using that form's official
schema and the agent's documented research protocol. **Highly complex returns — business income
with audit, for example — should still involve a qualified professional.**

## How it works (the flow)

1. You drop a PAN's documents into `pans/<alias>/inputs/`.
2. The agent presents an **upfront requirements checklist**, ingests and reconciles everything, and
   **determines the correct ITR form** from your situation — keeping durable per-PAN state in
   `pans/<alias>/state.json`.
3. It computes the return, confirms the regime, and assembles a schema-valid JSON for that form.
4. It hands you clear steps to pay any tax due and finalize the file through the official utility,
   then upload and e-verify.

The full playbook — guardrails, per-PAN memory model, form-determination logic, step sequence (SOP),
correction flow, and the hard-won filing gotchas — lives in
**[`itr-agent-guide.md`](./itr-agent-guide.md)**.

## Quickstart

**1. Install Claude Code** — <https://claude.com/claude-code>

**2. Clone this repo and open it in Claude Code:**
```bash
git clone git@github.com:anandsomu/itr-agent.git
# (no SSH key? use HTTPS: git clone https://github.com/anandsomu/itr-agent.git)
cd itr-agent
claude
```

**3. Start the agent** — in Claude Code, invoke the agent and let it guide you:
```
@itr-agent
```
(Or just describe your task — e.g. "help me file my ITR" — and read `itr-agent-guide.md` for the full flow.)

**4. Tell the agent who you're filing for** — e.g. *"prepare a return for my dad"*. The agent
creates that person's workspace itself (`pans/<alias>/`), presents the document checklist, and tells
you exactly where to drop the files. Your only manual step is copying in the documents (Form 16,
AIS, TIS, pre-filled JSON, broker statements, prior-year return, …) — the agent handles all the
setup, form selection, computation, and reconciliation from there, through to a schema-valid JSON
ready to finalize and file.

## Repository layout

| Path | What it is |
|---|---|
| `.claude/agents/itr-agent.md` | The agent definition (invoked as `@itr-agent`) |
| `CLAUDE.md` | Project instructions, loaded automatically |
| `itr-agent-guide.md` | The operating playbook (source of truth) |
| `itr2-rules.md` | Cited rules pack (ITR-2; other forms' packs are built as needed) |
| `validate_itr_json.py` | Validates a candidate return against the official schema |
| `pans/dashboard.py` | Compact progress board across all PANs |
| `memory/` | General, form-agnostic learnings |
| `pans/<alias>/` | Each PAN's documents + state — **git-ignored, stays local** |
| `schema/` | Official AY-specific schema + offline utility — fetch per year (git-ignored) |

## Privacy & safety

- **Your tax data never leaves your machine via git.** Every `pans/<alias>/` folder (documents,
  `state.json`, filed artifacts) is git-ignored. Always run `git status` before pushing.
- The agent **does not authenticate, file, pay, or e-verify** — those actions are always yours.
- The AY-specific JSON schema and offline utility are public Income-Tax Department downloads and are
  not bundled (they change yearly); the agent points you to the current ones.

## Disclaimer

This is a tooling aid, **not professional tax advice**. Tax law changes and edge cases abound —
verify every figure yourself and consult a qualified chartered accountant or tax professional where
appropriate. No warranty; use at your own risk.

---

<sub>**Topics / keywords:** income-tax, ITR, ITR-1, ITR-2, ITR-3, ITR-4, India, income-tax-return,
tax-filing, AIS, TIS, capital-gains, Schedule-FA, foreign-assets, new-tax-regime, presumptive-tax,
Claude-Code, AI-agent, tax-automation, incometax.gov.in. &nbsp; Suggested GitHub topics:
`income-tax` `itr` `itr-2` `itr-3` `india` `tax-filing` `claude-code` `ai-agent` `capital-gains`
`ais` `tax-automation`.</sub>
