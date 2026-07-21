# pans/ — per-PAN workspace

Each PAN being prepared gets its own folder here. **These folders are git-ignored and never
committed** — they hold real taxpayer PII and stay local to your machine.

```
pans/
├── dashboard.py          # shared tool (committed): progress board across all PANs
├── README.md             # this file (committed)
├── <alias>/              # one folder per PAN — GIT-IGNORED (local only)
│   ├── inputs/           # source docs (Form 16, AIS/TIS, prefill, broker CG, prior return, …)
│   ├── work/             # scratch / intermediate files
│   ├── output/           # assembled JSON + filed return artifacts
│   └── state.json        # the agent's per-PAN memory (progress, figures, decisions, open Qs)
└── DASHBOARD.md          # rendered board — git-ignored (may contain names/figures)
```

To start a PAN, create `pans/<alias>/inputs/` and drop the documents in. Run
`python3 pans/dashboard.py` for the board, or `python3 pans/dashboard.py <alias>` for one PAN.
See `../itr-agent-guide.md` for the per-PAN memory model and the step sequence.
