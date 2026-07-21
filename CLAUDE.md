# CLAUDE.md

This project prepares Indian income-tax returns, one PAN at a time. It
**determines the correct ITR form** (ITR-1, ITR-2, ITR-3, or ITR-4 — and flags
firm/company/trust cases as out of individual scope) from the person's income
sources, then prepares that form. ITR-2 is the most deeply validated path so far;
other forms follow the same SOP using that form's official schema and a per-form
rules pack built via the research protocol.

**Follow the operating guide in [`itr-agent-guide.md`](./itr-agent-guide.md).** It
is the source of truth for guardrails, the form-determination step (S0), the
per-PAN memory model (`pans/<alias>/state.json`), the step sequence (SOP), the
correction flow, and the research protocol. Read it before doing anything, and
follow it exactly.

Rules live in per-form packs. [`itr2-rules.md`](./itr2-rules.md) is the ITR-2 pack
(its regime/slab/capital-gains/deduction content is largely shared across forms);
packs for other forms (e.g. `itr3-rules.md`) are created when those forms are first
exercised. Validate every candidate JSON with `validate_itr_json.py` against the
official schema for the chosen form.

You can also invoke the dedicated agent as `@itr-agent`.
