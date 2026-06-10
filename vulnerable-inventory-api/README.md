# Vulnerable Inventory API (Test Fixture)

A small Flask-based inventory management API with **intentionally outdated
dependencies**. Its purpose is to act as a test fixture for automated
dependency-remediation agents: scan it, score it, upgrade it, and validate
that the app still works afterwards.

> ⚠️ Do NOT deploy this anywhere. Every pinned version below has known CVEs.

## Layout

```
vulnerable-inventory-api/
├── app/
│   ├── main.py        # Flask API (flask, jinja2, requests, pyyaml, pillow, sqlalchemy)
│   └── tasks.py       # Celery workers (paramiko, lxml, cryptography, numpy, markdown)
├── tests/
│   └── test_app.py    # Smoke tests = your post-upgrade validation gate
├── requirements.txt   # The intentionally outdated pins
└── KNOWN_VULNERABILITIES.md  # Answer key for verifying your agent
```

## How to use it with your agent

1. Point the agent at `requirements.txt`.
2. Expected detection: 14 outdated packages, most with one or more CVEs
   (see `KNOWN_VULNERABILITIES.md` for the answer key).
3. After the agent upgrades pins, run the validation gate:
   ```bash
   pip install -r requirements.txt
   pytest -q
   ```
4. Edge cases baked in for the agent to handle:
   - **flask 0.12 → 2.x/3.x** is a *major* jump (werkzeug + jinja2 must move together).
   - **sqlalchemy 1.2 → 2.x** has breaking API changes (`declarative_base` import moved).
   - **pyyaml `safe_load`** is already used — agent shouldn't flag a code change there.
   - **celery 4.2 → 5.x** changes the CLI; the code itself mostly survives.
   - **numpy 1.16 → modern** is generally safe but tests confirm it.

## Quick scan commands (for baseline comparison)

```bash
pip install pip-audit safety
pip-audit -r requirements.txt
safety check -r requirements.txt
```
