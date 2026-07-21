# ITR-2 Rules Pack — AY 2026-27 (FY 2025-26)

This is the **ITR-2 pack** within a per-form rules model. Other forms have their
own packs (e.g. `itr3-rules.md`, `itr4-rules.md`), created via the research
protocol when first exercised. The shared content here — regime/slabs, capital
gains, deductions, deadlines — is **largely reused across forms**; a new pack
mostly adds that form's own schedules and cross-references this one. The
form-selection decision tree below is common to all individual returns.

Assessment year governed by the Income-tax Act, 1961 (the last AY before the
Income-tax Act, 2025 takes over from FY 2026-27 — re-check the governing Act for
AY 2027-28 onward).

Lines marked `[VERIFY EACH SEASON]` are my best current knowledge but MUST be
confirmed against incometax.gov.in / CBDT before filing. When you verify one,
append the source URL and the date you checked.

## Deadline & filing
- Due date — ITR-1 / ITR-2, non-audit individuals: **31 July 2026**.
  `[VERIFY EACH SEASON — watch for any official extension]`
- Carry-forward of capital losses requires filing on or before the due date
  (s.139(1) / s.139(3)). A belated return (s.139(4)) **forfeits** carry-forward of
  capital losses. So on-time filing is the whole point of a loss claim.
- Belated / revised returns: up to **31 March 2027**. `[VERIFY]`

## Form selection (common to all individual/HUF returns — see guide S0)
Do not assume ITR-2. Choose from the income profile:
- **ITR-1 (Sahaj)**: *resident* individual, total income ≤ ₹50L, income only from
  salary/pension + **one** house property + other sources (+ agricultural income
  ≤ ₹5,000). A small **LTCG u/s 112A ≤ ₹1.25L** is now permitted.
  `[VERIFY current-year ITR-1 eligibility, incl. the 112A allowance]` NOT ITR-1 if:
  capital gains beyond that small 112A, any foreign asset/income, >1 house property,
  company directorship, unlisted shares, business/professional income, or
  non-resident.
- **ITR-2**: individual/HUF **without** business or professional income — capital
  gains, crypto (VDA), foreign assets/income (Schedule FA), >1 property, income
  > ₹50L, directorship, unlisted shares, etc.
- **ITR-3**: individual/HUF **with** business or professional income — including
  **F&O and intraday** (business/speculative income), professional receipts. It is a
  **superset of ITR-2** plus Schedule BP, P&L, Balance Sheet, possible audit u/s
  44AB, and Form 10-IEA for regime election. ITR-2 work carries over unchanged.
  `[Build itr3-rules.md when first exercised]`
- **ITR-4 (Sugam)**: *resident* individual/HUF/firm (**non-LLP**) with
  **presumptive** business/professional income u/s 44AD/44ADA/44AE, total income
  ≤ ₹50L. `[Build itr4-rules.md when first exercised]`
- **Out of individual scope**: firms/LLPs → ITR-5; companies → ITR-6; trusts/
  institutions → ITR-7. Flag rather than force into ITR-1–4.

## Capital gains — listed equity / equity mutual funds
- **STCG** (holding ≤ 12 months), s.111A: **20%**. `[VERIFY rate]`
- **LTCG** (holding > 12 months), s.112A: **12.5%** on gains above **₹1.25L** per
  year. `[VERIFY rate & exemption threshold]`
- Set-off matrix: **STCL** → against STCG or LTCG; **LTCL** → against LTCG only.
- Unabsorbed capital losses carry forward **8 years** (subject to on-time filing).

## Crypto / Virtual Digital Assets — Schedule VDA
- Gains taxed at a flat **30%** (s.115BBH) + surcharge/cess. Only **cost of
  acquisition** is deductible — no other expenses, no indexation.
- Crypto losses: **not** set off against any income (including other VDA gains)
  and **not** carried forward.
- **1% TDS** u/s 194S — reconcile against AIS.

## Other sources
- FD / savings interest taxed at slab. TDS u/s 194A. 80TTA (savings interest,
  ≤ ₹10k) available under the old regime. `[VERIFY]`

## Regime (applies to slab income only; CG & VDA taxed at special rates regardless)
- New regime is the default. Revised slabs; standard deduction ₹75,000; the s.87A
  rebate makes income up to ₹12L effectively nil — but the rebate does **not**
  apply to special-rate income (111A / 112A / 115BBH).
  `[VERIFY slabs, standard deduction, and the 87A threshold for the year]`
- Old regime: Chapter VI-A deductions (80C, 80D, HRA, 80TTA, etc.) available.
  Compare total tax both ways, per person.

## JSON output
- Use the official ITR-2 JSON schema in `schema/`, current version.
  `[VERIFY schema version against the portal]`
- Prefer starting from the portal's pre-filled JSON. Validate every candidate
  against the schema before upload. Schema-valid ≠ numbers correct.
