# Known Vulnerabilities — Answer Key (Ruby)

Use this to verify your agent's scan output. CVE lists are representative,
not exhaustive (bundler-audit may report more). "Safe target" = a reasonable
upgrade destination as of early 2026; your agent may legitimately choose newer.

| Gem          | Pinned  | Representative CVEs / advisories                              | Safe target | Upgrade type |
|--------------|---------|---------------------------------------------------------------|-------------|--------------|
| sinatra      | 2.0.5   | CVE-2022-29970 (path traversal), CVE-2022-45442 (XSS)         | 4.x         | MAJOR        |
| rack         | 2.0.6   | CVE-2019-16782 (session timing), CVE-2020-8184, CVE-2022-30122| 3.x         | MAJOR        |
| puma         | 3.12.0  | CVE-2019-16770, CVE-2020-5247/5249 (HTTP smuggling), CVE-2020-11076/77 | 6.x | MAJOR  |
| activerecord | 5.2.0   | CVE-2018-16476, CVE-2021-22880 (DoS), CVE-2022-32224 (RCE via YAML column) | 7.x | MAJOR (breaking) |
| nokogiri     | 1.10.4  | CVE-2020-26247 (XXE), CVE-2021-41098, bundled libxml2 CVEs    | 1.16+       | MINOR (native deps) |
| rest-client  | 1.8.0   | CVE-2015-3448 (logs Authorization header in plaintext)        | 2.1.x       | MAJOR        |
| loofah       | 2.2.2   | CVE-2018-16468 (XSS bypass), CVE-2019-15587                   | 2.19+       | MINOR        |
| json         | 2.1.0   | CVE-2020-10663 (unsafe object creation)                       | 2.7.x       | MINOR        |
| rake         | 12.3.2  | CVE-2020-8130 (command injection in FileList)                 | 13.x        | MAJOR        |
| sidekiq      | 5.2.5   | CVE-2021-30151 (Web UI XSS), CVE-2022-23837 (DoS)             | 7.x         | MAJOR        |
| tzinfo       | 1.2.5   | CVE-2022-31163 (path traversal in timezone lookup)            | 2.x         | MAJOR        |
| addressable  | 2.7.0   | CVE-2021-32740 (ReDoS in template parsing)                    | 2.8.x       | MINOR        |
| omniauth     | 1.9.0   | CVE-2015-9284 (CSRF in request phase — needs omniauth-rails_csrf_protection or 2.x) | 2.x | MAJOR |
| colorize     | 0.8.1   | None — outdated only (tests "stale vs vulnerable" handling)   | 1.x         | MAJOR (but trivial) |

## Expected agent behaviors worth asserting

1. **Lockfile awareness** — the agent should generate/refresh `Gemfile.lock`
   and scan it (bundler-audit ignores the Gemfile), then update both files.
2. **Detection completeness** — 13 CVE-affected gems flagged; colorize flagged
   as outdated-only (or skipped, depending on your policy).
3. **Risk prioritization** — activerecord (RCE class), rake (command
   injection), tzinfo (path traversal), and puma (request smuggling) should
   rank high.
4. **Coupled upgrades** — sinatra/rack/puma must move together; activerecord
   forces a sqlite3 bump. Upgrading sinatra alone fails resolution.
5. **Breaking-change warnings** — activerecord 7.x, tzinfo 2.x, rest-client
   2.x (exception class changes), and omniauth 2.x should carry MAJOR
   warnings; omniauth 2.x also changes the request phase to POST-only.
6. **Validation gate** — `bundle exec rake test` passes before and (after
   minor code fixes, if your agent does them) after upgrade.
