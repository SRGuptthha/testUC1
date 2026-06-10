# Known Vulnerabilities — Answer Key

Use this to verify your agent's scan output. CVE lists are representative,
not exhaustive (scanners may report more). "Safe target" = a reasonable
upgrade destination as of early 2026; your agent may legitimately choose newer.

| Package      | Pinned  | Representative CVEs / advisories                          | Safe target | Upgrade type |
|--------------|---------|-----------------------------------------------------------|-------------|--------------|
| flask        | 0.12.2  | CVE-2018-1000656, CVE-2019-1010083 (DoS via JSON)         | 3.x         | MAJOR        |
| werkzeug     | 0.14.1  | CVE-2019-14806 (debugger PIN), CVE-2023-25577             | 3.x         | MAJOR        |
| jinja2       | 2.10    | CVE-2019-10906 (sandbox escape), CVE-2020-28493           | 3.1.x       | MAJOR        |
| requests     | 2.19.1  | CVE-2018-18074 (credential leak on redirect)              | 2.32.x      | MINOR        |
| urllib3      | 1.24.1  | CVE-2019-11324, CVE-2019-11236, CVE-2020-26137            | 2.x         | MAJOR        |
| pyyaml       | 5.1     | CVE-2019-20477, CVE-2020-1747, CVE-2020-14343 (full_load) | 6.x         | MAJOR        |
| pillow       | 8.1.0   | CVE-2021-25287/88, CVE-2021-28675..78, CVE-2022-22817     | 10.x+       | MAJOR        |
| lxml         | 4.6.2   | CVE-2021-28957 (XSS), CVE-2021-43818                      | 5.x         | MAJOR        |
| cryptography | 2.8     | CVE-2020-25659 (Bleichenbacher), CVE-2023-23931           | 42.x+       | MAJOR        |
| paramiko     | 2.4.1   | CVE-2018-1000805 (auth bypass), CVE-2022-24302            | 3.x         | MAJOR        |
| sqlalchemy   | 1.2.0   | CVE-2019-7164, CVE-2019-7548 (SQL injection via order_by) | 2.x         | MAJOR (breaking) |
| celery       | 4.2.1   | CVE-2021-23727 (stored command injection via backend)     | 5.x         | MAJOR        |
| numpy        | 1.16.0  | CVE-2019-6446 (pickle load), CVE-2021-33430               | 1.26+/2.x   | MAJOR        |
| markdown     | 3.0.1   | Outdated (no major CVE — tests "outdated but not vulnerable" handling) | 3.x latest | MINOR |

## Expected agent behaviors worth asserting

1. **Detection completeness** — all 13 CVE-affected packages flagged; markdown
   flagged as outdated-only (or skipped, depending on your policy).
2. **Risk prioritization** — pillow, pyyaml, paramiko, and sqlalchemy should
   rank high (RCE / injection class issues).
3. **Coupled upgrades** — flask, werkzeug, and jinja2 must be upgraded
   together; upgrading flask alone breaks resolution.
4. **Breaking-change warnings** — sqlalchemy 2.x (`declarative_base` moved to
   `sqlalchemy.orm`), urllib3 2.x, celery 5.x should carry MAJOR warnings.
5. **Validation gate** — `pytest -q` passes before and (after minor code
   fixes, if your agent does them) after upgrade.
