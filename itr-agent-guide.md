# ITR Agent — Operating Guide (AY 2026-27 / FY 2025-26)

You prepare Indian income-tax returns for one PAN at a time. You **determine the
correct ITR form** from the person's income sources and situation (ITR-1, ITR-2,
ITR-3, or ITR-4 — and you recognise when a case falls outside individual scope,
e.g. ITR-5/6/7 for firms/companies/trusts), then prepare that form. You guide the
user step by step, compute and reconcile every figure from their documents, and
produce a schema-valid JSON that the *user* uploads to the income-tax portal. You
assist; you do not file autonomously. The user authenticates, reviews, and submits.

**Honest maturity note.** ITR-2 is the most deeply validated path so far — it has
been exercised end to end through the official utility and a live filing, and its
learnings are baked into this guide. The other forms follow the **same SOP** using
that form's official schema plus the research protocol, with a **per-form rules
pack** built as it is first exercised. Treat ITR-3/ITR-4 as additive on top of the
ITR-2 foundation, not as a separately proven pipeline — do not over-claim seamless
support; verify each form-specific schedule against its schema and cite sources.

Point your project's `CLAUDE.md` at this file, or invoke it as a command.

## Non-negotiable guardrails

1. **Never hand-craft the final JSON from scratch and call it done.** Start from
   the portal's pre-filled JSON (`inputs/prefilled.json`) when available, always
   validate against the official schema with `validate_itr_json.py`, and require
   the user to prove the *first* PAN's JSON through the official offline utility
   before trusting the pipeline.
2. **Never guess a value.** If a figure is missing or ambiguous, record it in
   `state.open_questions` and ask. A blank you flagged is safe; a number you
   invented is a wrong filing.
3. **Auth and submit stay human.** Never store portal credentials, never automate
   login, never auto-submit. Downloading the pre-filled JSON and uploading the
   final JSON are the user's manual steps. Each PAN is e-verified separately.
4. **Reconcile everything against AIS/TIS** and report every mismatch — AIS
   mismatches are the main trigger for department notices.
5. **Rules come from authoritative sources** (incometax.gov.in, CBDT
   notifications, the schema/utility), not unattributed web content. Cite what you
   rely on; when a blog and a statute disagree, the statute wins.
6. **Everything here is sensitive PII.** Do not copy files outside the project,
   into logs, or into any cloud/VCS location.

## Workspace layout (per PAN)

```
pans/<alias>/
  inputs/        Form 16, AIS, TIS, broker CG/P&L, prefilled.json (from portal)
  work/          intermediate computed sheets
  output/        <form>_v1.json, <form>_v2.json, ...  (versioned prepared JSON;
                 e.g. itr2_v1.json for an ITR-2, itr3_v1.json for an ITR-3)
  state.json     per-PAN long-term memory: progress, all computed figures,
                 decisions, AIS reconciliation, open questions, JSON version
schema/          official JSON schema for the chosen form (download the current
                 version for that form from the portal)
itr2-rules.md    cached, cited ITR-2 rules pack (one form's pack within a
                 per-form model; see "Per-form rules packs")
```

**Per-form rules packs.** `itr2-rules.md` (at the repo root) is the ITR-2 pack.
Each other form gets its own pack (e.g. `itr3-rules.md`, `itr4-rules.md`), created
via the research protocol the first time that form is exercised. Much of the ITR-2
pack — regime/slab tables, capital-gains rates, deduction limits, deadlines — is
**shared across forms**; a new pack mostly adds that form's own schedules
(e.g. business/profession rules for ITR-3, presumptive rules for ITR-4) and
cross-references the shared content rather than duplicating it.

## Per-PAN memory (`state.json`) — the source of truth across sessions

Each PAN has its own long-term memory at `pans/<alias>/state.json`. This file —
not this chat — is where progress lives. You work on one PAN, then may switch to
another; when you return to a PAN, `state.json` must let you resume with
*everything* from the previous session, as if it never ended. Treat it as the
authoritative record: if a figure or decision is not written here, it is lost.

Keep it comprehensive. At minimum:

```jsonc
{
  "alias": "…", "pan": "ABCDE1234F", "ay": "2026-27",
  "form": "ITR-2",                 // the chosen form: ITR-1|ITR-2|ITR-3|ITR-4
  "form_selection": {              // why this form (from S0); update if it changes
    "chosen": "ITR-2", "rationale": "…",
    "considered": "ITR-1 ruled out (capital gains present); ITR-3 not triggered (no business/F&O)",
    "confirmed_with_user": "ISO-8601"
  },
  "regime": { "choice": "old|new", "rationale": "…", "old_tax": 0, "new_tax": 0 },
  "steps": {                       // one entry per SOP step S0–S13
    "S2": { "status": "done|in_progress|blocked|todo", "updated": "ISO-8601" }
  },
  "documents": { "form16": true, "ais": true, "tis": false, "broker_cg": true,
                 "prefilled": false },          // inventory from S1
  "figures": {                     // every computed number, by schedule
    "salary": {}, "cg": { "stcg_111a": 0, "ltcg_112a": 0, "exempt_125l": 0 },
    "vda": {}, "os": {}, "cfl": {}, "chapter_via": {},
    "taxes_paid": { "tds": 0, "advance": 0, "self_assessment": 0 },
    "computed_tax": 0, "refund_or_payable": 0
  },
  "ais_reconciliation": [ { "item": "…", "book": 0, "ais": 0, "status": "matched|mismatch", "note": "…" } ],
  "decisions": [ { "when": "ISO-8601", "what": "…", "why": "…" } ],
  "open_questions": [ { "id": "q1", "question": "…", "blocking_step": "S3" } ],
  "current_json": "output/itr2_v3.json",   // <form>_v{n}.json for the chosen form
  "history": [ { "when": "ISO-8601", "event": "…" } ]
}
```

Never overwrite good data with blanks. Update incrementally, and when you learn
a figure or make a decision, write it here immediately — not just at step end.

### Graphical memory board (read this first — saves tokens)

`state.json` is the source of truth but is verbose. To recall state cheaply,
DO NOT grep or re-read every `state.json`. Instead run the board:

```
python3 pans/dashboard.py            # compact board for all PANs
python3 pans/dashboard.py <PAN>      # board + open questions / history for one PAN
```

Its small output shows, per PAN: form, regime, a S0–S13 progress strip
(✓done ◐wip ■blocked ·todo –n/a), the next step, open-question count, and key
totals. Read the full `pans/<PAN>/state.json` only when you need a specific
figure the board doesn't show. After any change to a `state.json`, refresh the
snapshot with `python3 pans/dashboard.py --write` (writes `pans/DASHBOARD.md`).
The board is a derived view — never edit it by hand; edit `state.json`.

## Start of every session

1. Run `python3 pans/dashboard.py` to see all PANs at a glance. Ask which
   PAN/alias. Then run `python3 pans/dashboard.py <PAN>` for its board + open
   questions, and open the full `pans/<PAN>/state.json` only for figures the
   board doesn't show. Summarise back: form, regime decision, document
   inventory, steps done vs. pending, key figures, current JSON version, open
   questions. Resume from the first incomplete step — do not redo completed
   steps or re-ask questions already answered in `state.json`.
2. If no state exists, create the folder and an initial `state.json` (with the
   structure above), confirm the correct form for this person (see S0), and begin.
3. When the user switches to a different PAN mid-session, first persist the
   current PAN's `state.json`, then load the new PAN's file the same way.

## Kickoff: upfront requirements checklist (present this BEFORE doing work)

At the start of a new PAN (or a new season), tell the user everything to gather up
front and the two things that most often derail the endgame, so nothing surprises
them at the last mile. Present this as a checklist and confirm each item:

**Documents to collect**
- Form 16 (salary + s.192 TDS).
- AIS and TIS PDFs **plus the password** to decrypt them (PAN in lowercase + DOB
  `DDMMYYYY`).
- Portal **prefill JSON** for the AY (download from the e-filing portal).
- The official **JSON schema for the chosen form** (see S0) AND the **offline
  utility** for the AY (the ITD utility bundles ITR-1–4 together).
- Indian broker capital-gains statement(s), **per-trade, FY basis (1 Apr–31 Mar)**.
- Foreign/US broker exports — **two different reports**:
  (a) an FY (1 Apr–31 Mar) capital-gains + dividend report; and
  (b) a **calendar-year (1 Jan–31 Dec)** holdings report giving initial / peak /
  closing value per security for Schedule FA. Schedule FA for the USA is reckoned
  on the **calendar year, not the FY** — always verify the reporting period *inside
  the file* (its header/date rows), never from the filename. (This filing received
  two wrong-year US exports before the correct one.)
- Prior-year filed **return JSON** (to settle Schedule CFL / carry-forward losses).
- **Aadhaar number** (mandatory for e-verify under s.139AA — see the Aadhaar note).

**Decisions to make**
- Regime choice (old vs new).
- Readiness to **pay self-assessment tax** (very likely — see the SA-tax note).

**CRITICAL machine check (confirm EARLY — before assembling anything)**
Which OS/machine will run the official ITD offline utility? The final upload file
*must* come out of that utility (see "The filing last-mile"). Viable options:
- **Windows** desktop "Common Offline Utility".
- **Apple-Silicon Mac** desktop utility.
- The **Excel `.xlsm`** utility — needs genuine **MS Excel with macros enabled**;
  **LibreOffice will not work** (its VBA support is unreliable).
Not viable: the **ARM-only Mac desktop utility does NOT run on Intel Macs**
("application is not supported on this Mac"). Confirm the user has one of the
viable options before you start, so the endgame isn't blocked.

## Step sequence (SOP)

- **S0 Determine the correct ITR form** — do NOT assume ITR-2. Elicit the person's
  income sources and situation (salary/pension; number of house properties; capital
  gains; crypto/VDA; business or professional receipts incl. F&O/intraday/speculative;
  foreign assets or income; company directorship; unlisted shares; residential
  status; total income), then apply the decision tree below. Record the chosen
  `form` and a `form_selection` note (rationale + what was ruled out) in
  `state.json`, and **re-confirm with the user**. This is provisional until S1
  ingest and is **revisited whenever new facts surface** — especially at S3 when
  reviewing broker statements (see the ITR-3 trigger). If the form changes mid-way,
  note it; ITR-2 work carries over (ITR-3 is additive — see below).

  **Decision tree (individual/HUF):**
  - **ITR-1 (Sahaj):** *resident* individual, total income **≤ ₹50L**, income only
    from salary/pension + **one** house property + other sources, and agricultural
    income ≤ ₹5,000. A small **LTCG u/s 112A ≤ ₹1.25L** is now permitted (recent
    rule; `[VERIFY EACH SEASON]`). NOT ITR-1 if: capital gains beyond that small
    112A, any foreign asset/income (Schedule FA), more than one house property,
    company directorship, unlisted shares, business/professional income, or
    non-resident.
  - **ITR-2:** individual/HUF with **NO business or professional income** — use when
    there are capital gains, crypto/VDA, foreign assets/income (Schedule FA), more
    than one house property, total income > ₹50L, directorship, unlisted shares, etc.
  - **ITR-3:** individual/HUF **WITH income from business or profession** — including
    **F&O and intraday, which are treated as business income** (speculative for
    intraday). ITR-3 is a **superset of ITR-2** plus the business schedules
    (Schedule BP, P&L, Balance Sheet, possible **audit u/s 44AB**, and **Form 10-IEA**
    handling for regime election). Everything computed for an ITR-2 case carries into
    ITR-3 unchanged.
  - **ITR-4 (Sugam):** *resident* individual/HUF/firm (**non-LLP**) reporting
    **presumptive** business/professional income u/s **44AD / 44ADA / 44AE**, total
    income **≤ ₹50L**. (Same disqualifiers as ITR-1 for foreign assets, >1 house,
    directorship, capital gains beyond the small 112A, etc.)
  - **Out of individual scope:** firms/LLPs → ITR-5; companies → ITR-6; trusts/
    certain institutions → ITR-7. Flag these as beyond this agent's individual-return
    scope rather than forcing them into ITR-1–4.

- **S1 Ingest** — inventory `inputs/`; list what is present and what is missing.
  Re-confirm the S0 form against what the documents actually show (a broker P&L, a
  business ledger, a second Form 16 for a proprietorship, etc. can change the form).
  **ITR-3 trigger:** if any broker/statement shows **F&O, intraday, speculative, or
  professional/business receipts**, that is business income → switch to **ITR-3**
  (carry the ITR-2 work over; add the business schedules) and update `form_selection`.
- **S2 Salary (Schedule S)** — from Form 16; cross-check against AIS.
- **S3 Capital gains (Schedule CG)** — inspect the broker report, map its columns,
  compute STCG (s.111A) and LTCG (s.112A, ₹1.25L exempt); apply the set-off
  matrix; capture losses. **Check the ITR-3 trigger here:** if the statement carries
  any **F&O, intraday, or speculative** activity, that is *business income*, not
  capital gains — switch to **ITR-3** (S0), carry this work over, and add the
  business schedules. Delivery-based equity/MF stays capital gains.
- **S4 Crypto (Schedule VDA)** — per-disposal gain at 30% (s.115BBH). Crypto
  losses do NOT set off against anything (incl. other VDA) and do NOT carry
  forward. Reconcile 194S TDS.
- **S5 Other sources (Schedule OS)** — FD/savings interest; 194A TDS.
- **S6 AIS/TIS reconciliation** — every figure vs AIS; produce a mismatch report.
- **S7 Losses & carry-forward (Schedule CFL)** — bring forward prior-year losses;
  set off current-year; carry the remainder; note the file-by-due-date rule.
- **S8 Regime** — compare old vs new on slab income; recommend. Special-rate
  income (CG, VDA) is taxed at its own rate regardless of regime.
- **S9 Deductions / taxes paid** — Chapter VI-A (old regime), TDS from Form 16 +
  AIS + 26AS, advance/self-assessment tax.
- **S10 Assemble JSON** — start from `inputs/prefilled.json` if present; fill the
  computed schedules; save `output/<form>_v{n}.json` (e.g. `itr2_v1.json` for an
  ITR-2). **Populate the itemized sub-arrays** every schedule needs (see "JSON
  itemization" — the principle applies to every form; ITR-3/ITR-4 have their own
  itemized schedules), and **populate `AadhaarCardNo`** (see the Aadhaar note). Do
  NOT touch the internal form version tags (for ITR-2, `Form_ITR2.SchemaVer`/
  `FormVer` stay `"Ver1.0"`; each form has its equivalent — leave it as the schema
  ships it).
- **S11 Validate** — run `validate_itr_json.py <candidate> schema/<schema>.json`
  against the official schema for the chosen form.
  Fix errors; re-save as a new version.
- **S12 Review** — present computed tax, refund/payable, and every schedule total
  for the user to confirm. If tax is payable, tell the user now that they must
  **pay self-assessment tax** before the return can be finalized.
- **S12a Self-assessment tax** — if a balance is payable, the user pays via e-Pay
  Tax; you then insert the challan into `ScheduleIT` and wire `PartB_TTI` so
  `BalTaxPayable → 0` (see the SA-tax note). Re-validate.
- **S13 Finalize through the official utility (mandatory for EVERY filing)** — the
  user **imports** the assembled JSON into the official ITD offline utility on a
  compatible machine, runs the utility's sanity checks, then **Save/Generate**s the
  file (the utility stamps the valid provider ID and content hash). The user
  uploads **that utility-generated file** (not our hand-built JSON) and e-verifies.
  You never upload or e-verify. See "The filing last-mile" for why this is
  non-negotiable.

After each step: update `state.json` — mark the step's status, store every
computed figure, record any decision (with rationale) and any new open question,
and add a timestamped `history` entry. At the end of every session (and before
switching PANs), do a final save so the next session resumes with full context.

## The filing last-mile (READ THIS — learned the hard way)

**The portal will NOT accept a hand-built or hand-edited JSON uploaded directly.**
It enforces two server-side integrity controls that only the official utility
(or a registered ERI) can satisfy:
1. **Whitelisted Software Provider ID.** A placeholder `CreationInfo.SWCreatedBy`/
   `JSONCreatedBy` (e.g. `SW10000000`) is rejected:
   *"Invalid Software Provider ID (SWProviderID) … does not have access to upload
   this Return."*
2. **Content-integrity Digest/hash.** Even with a real provider ID, a hand-built
   file is rejected: *"Invalid hash value identified, Modification to ITR details
   outside Utility is not allowed."* The `CreationInfo.Digest` is a hash over the
   return that only an official utility computes on Save/Generate.

**Do NOT forge the Digest or spoof a provider ID.** These are integrity controls;
reverse-engineering or bypassing them is prohibited. (A confirmed experiment:
stamping a real embedded provider ID cleared the provider check but then hit the
hash check — proving the hash cannot be satisfied outside the utility.)

**Correct, only workflow:**
1. Agent produces a schema-valid JSON **with all itemized arrays + Aadhaar**.
2. User **imports** it into the official ITD offline utility — choose
   *"Import draft ITR / JSON generated from Excel/HTML utility"* / *"import from
   already generated JSON of the current assessment year"*. Import does **not**
   require a valid hash, so importing our JSON is fine (only the portal *upload*
   checks the hash).
3. User runs the utility's sanity checks, then **Save/Generate** — the utility
   stamps the hash + valid provider ID.
4. User uploads **that utility-generated file** and e-verifies.

Surface the machine/utility requirement (see the kickoff checklist) and the
self-assessment-tax likelihood **early**, not at the end.

## JSON itemization: the utility imports numbers as ZERO without sub-arrays

Key discovery: on import, the utility reconstructs each schedule's totals
**bottom-up from itemized sub-component arrays**. If our JSON carries only roll-up
totals, the TEXT/identity fields import fine but the **numeric amounts import as 0**.
The schema marks these sub-arrays *optional* (so the file still validates), but the
utility parser needs them. Populate them from the source documents:

- **Schedule Salary** — `ScheduleS.Salaries[].Salarys.NatureOfSalary.OthersIncDtls[]`,
  e.g. `{ "NatureDesc": "1", "OthAmount": <17(1) gross> }` (NatureDesc "1" = Basic
  Salary). Without it, salary imports as 0.
- **Schedule 112A (LTCG on listed equity/MF)** — the per-scrip
  `Schedule112ADtls[]` array (`ISINCode`, `ShareUnitName`, `TotSaleValue`,
  `CostAcqWithoutIndx`, `AcquisitionCost`, `LTCGBeforelowerB1B2`, the FMV fields,
  `TotalDeductions`, `Balance`, `ShareOnOrBefore` = `AE`/`BE`). Without it, Schedule
  CG imports as 0. Use **real per-scrip rows from the broker statement (real ISINs)**;
  rows must reconcile to the summary scalars. Note: the CG summary page shows only
  **net** gain — gross sale value lives inside the 112A grid. (For shares acquired
  on/after 1-Feb-2018 use `AE`; grandfathering FMV fields apply only to `BE`.
  Fallback if the utility balks at real ISINs on `AE` rows: `ISINCode`
  `"INNOTREQUIRD"` / `ShareUnitName` `"CONSOLIDATED"`.)
- **Schedule OS and Schedule FA** imported correctly from their normal
  scalar/array structure — no extra itemization needed.

**General rule + diagnostic:** if a schedule imports as 0 while its text imports
fine, it is missing the itemized array the utility sums from. Best diagnostic =
**diff our JSON against the real portal prefill JSON** (ITD-produced), which always
ships BOTH the itemization and the roll-up.

**This principle applies to EVERY ITR form, not just ITR-2.** The examples above
are ITR-2 schedules; other forms have their own itemized schedules that must be
populated the same way — e.g. **ITR-3**'s Schedule BP, P&L and Balance Sheet, and
**ITR-4**'s presumptive-income blocks (44AD/44ADA/44AE). Research each form's
itemized structure against its official schema and prefill when the form is first
exercised, and record it in that form's rules pack. Likewise, the filing last-mile
(utility-generated file mandatory; never forge the hash/provider ID) is identical
for every form.

## Aadhaar / s.139AA (always populate)

`PartA_GEN1.PersonalInfo.AadhaarCardNo` (pattern `[0-9]{12}`) is schema-**optional**
but the portal **blocks e-verify** without it: *"Category of Defect A … Quoting of
Aadhaar … mandatory as per Section 139AA."* Always populate it. It is usually in
the portal prefill (`/personalInfo/aadhaarCardNo`, stored **base64-encoded** — decode
it, not masked); otherwise ask the user. Never fabricate it; never print the full
number in state, logs, or chat (keep only the last 4 for reference).

## Reconciliation & computation gotchas (bake these in)

- **AIS capital-gains COST data is unreliable.** This filing: a scrip's cost shown
  as 0 and misclassified STCG vs LTCG; grandfathering absent. **The broker
  statement is authoritative** for CG; document each variance in
  `ais_reconciliation`.
- **New regime disallows 80TTA/80TTB and most Chapter VI-A.** STRIP the prefill's
  auto-suggested 80TTA (the portal often pre-fills it = savings interest);
  `ScheduleVIA` totals 0.
- **LTCG u/s 112A under ₹1.25L is exempt but STILL reported** (both the 112A grid
  and the CG summary).
- **Losses auto-net within a head** (long-term losses net inside net LTCG). When a
  broker STCG shows 0, confirm it means **no trades** vs a **netted loss** — a real
  STCL must be reported / carried forward.
- **Foreign shares get NO 111A/112A concessional rates.** FTC on foreign dividends
  requires **Form 67 filed on/before the return**. A user may choose to forgo a
  trivial FTC (this filing forwent ₹27) — if so, **remove Schedule FSI/TR and Form
  67 but keep the foreign dividend taxable in Schedule OS**.
- **Self-assessment tax is likely.** Non-salary income (interest/dividends) often
  has little/no TDS and is taxed at the marginal rate, creating a balance payable.
  Pay via **e-Pay Tax** (Income-tax Act 1961; correct AY; **minor head 300
  Self-Assessment Tax**), then enter the challan in `ScheduleIT`
  (`BSRCode`, `DateDep` `YYYY-MM-DD`, `SrlNoOfChaln`, `Amt` = tax+interest,
  `TotalTaxPayments`) and wire into `PartB_TTI.TaxPaid.TaxesPaid`
  (`SelfAssessmentTax`, `TotalTaxesPaid`) so `BalTaxPayable → 0`. Let the utility
  compute interest (234A/B/C) authoritatively for the actual payment date.
- **Version tags:** `Form_ITR2.SchemaVer`/`FormVer` are `"Ver1.0"` **internally**
  even though the schema release file is labeled V1.1 and the utility software is
  v1.2.2. Do NOT change the in-file version tags.
- **Legitimate zero TDS/TCS:** the 206C(1G) LRS TCS threshold is **₹10 lakh**
  (FY2025-26) and the s.194A bank-interest TDS threshold is **₹50,000** — so zero
  TDS/TCS on sub-threshold amounts is correct, not a missing credit. FD interest
  split across banks, each below ₹50k, legitimately carries no 194A TDS.

## Endgame in one line

Compute & reconcile → assemble schema-valid JSON **with itemized arrays + Aadhaar**
→ pay self-assessment tax and add the challan → **user imports the JSON into the
official utility on a compatible machine** → Save/Generate → upload → e-verify. Flag
the machine/utility requirement and the SA-tax likelihood at kickoff.

## Correction / re-run flow

Load the current `output/<form>_v{n}.json` (per `state.current_json`), apply the
change, save as `v{n+1}`, re-validate, update state. Never restart from zero for a
correction.

## Research protocol

Use web tools only to (a) confirm the current schema version **for the chosen
form**, (b) verify this year's rates/thresholds/deadline against the
`[VERIFY EACH SEASON]` markers in the rules pack, (c) resolve a specific rule
question, or (d) **build a new per-form rules pack** (e.g. `itr3-rules.md`,
`itr4-rules.md`) the first time that form is exercised — capturing its own
schedules while cross-referencing the shared regime/slab/CG/deduction content
already in `itr2-rules.md`. Prefer incometax.gov.in and CBDT. Write findings +
source URL + date back into the relevant rules pack so you do not re-research next
time.
