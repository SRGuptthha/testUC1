# vulnerable-py-app

A deliberately outdated Python project for testing dependency remediation agents.
**Do not deploy.** Every pin is a known-vulnerable or stale release on purpose.

Two manifests are included so you can test either path:
- `requirements.txt` (pip-style)
- `pyproject.toml` (PEP 621 dependencies + optional dev group)

## Outdated / vulnerable dependencies

| Package | Current (bad) | Notable CVE(s) | Suggested fixed version |
|---|---|---|---|
| requests | 2.25.0 | CVE-2023-32681 (proxy auth leak) | 2.32.x+ |
| urllib3 | 1.26.5 | CVE-2023-43804, CVE-2024-37891 | 2.2.x+ (or 1.26.19+) |
| jinja2 | 2.11.2 | CVE-2020-28493 (ReDoS), CVE-2024-22195 | 3.1.4+ |
| flask | 1.1.2 | stale; pairs w/ vuln Werkzeug | 3.0.x+ |
| werkzeug | 1.0.1 | CVE-2023-25577, CVE-2023-46136 | 3.0.x+ |
| setuptools | 58.0.0 | CVE-2022-40897 (ReDoS), CVE-2024-6345 | 70.0.0+ |
| certifi | 2021.5.30 | CVE-2023-37920 (bad root CA) | 2024.7.4+ |
| PyYAML | 5.3.1 | CVE-2020-14343 (RCE via full_load) | 6.0.1+ |
| cryptography | 3.3.2 | CVE-2023-0286, CVE-2023-50782, others | 43.x+ |
| pandas | 1.1.5 | stale, major behind | 2.2.x+ |
| numpy | 1.19.5 | stale, major behind | 1.26.x / 2.x |
| ipython (dev) | 7.16.1 | CVE-2022-21699 (arbitrary code exec) | 8.x+ |
| pytest (dev) | 5.4.3 | stale | 8.x+ |

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt        # installs the vulnerable set
pip install -e ".[dev]"                # alt path via pyproject
pytest
```

## What a remediation agent should do

1. Parse `requirements.txt` and/or `pyproject.toml`.
2. Detect each outdated package and map to known CVEs (e.g. via `pip-audit` / OSV).
3. Recommend the lowest safe upgrade, flagging major bumps (numpy 1→2, pandas 1→2, flask/werkzeug 1→3, urllib3 1→2, jinja2 2→3) as potential breaking changes needing review.
4. Update the manifest and re-run tests to confirm nothing broke.

The split between safe minor bumps and risky major bumps is intentional — good for testing whether your agent routes breaking changes to a human approval gate instead of auto-applying them.
