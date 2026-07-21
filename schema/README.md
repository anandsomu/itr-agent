# schema/ — official ITR JSON schema & offline utility

These are **assessment-year-specific public downloads** from the Income-Tax e-filing portal that
change every year, so they are **git-ignored** (not committed). Fetch the current ones and drop them
here.

From <https://www.incometax.gov.in/iec/foportal/downloads/income-tax-returns> → your Assessment Year
→ ITR-2:

1. **Schema JSON** (e.g. `ITR-2_<year>_Main_V*.json`) — `validate_itr_json.py` validates candidate
   returns against this.
2. **Offline utility** — the Common Offline Utility (Windows / Apple-Silicon macOS) **or** the Excel
   `.xlsm` (needs MS Excel with macros). This is what stamps the integrity hash on the final file —
   see the "filing last-mile" section of `../itr-agent-guide.md`.

> The macOS desktop utility is Apple-Silicon-only and will **not** run on an Intel Mac. Use Windows,
> an Apple-Silicon Mac, or the Excel `.xlsm` (not LibreOffice). The agent points you to the exact
> current-year links when you reach that step.
