# Vulnerable Inventory API — Ruby (Test Fixture)

A small Sinatra + ActiveRecord inventory API with **intentionally outdated
gems**. Its purpose is to act as a test fixture for automated dependency-
remediation agents: scan it, score it, upgrade it, and validate that the app
still works afterwards.

> ⚠️ Do NOT deploy this anywhere. Nearly every pinned gem below has known CVEs.

## Layout

```
vulnerable-inventory-rb/
├── app/
│   ├── api.rb         # Sinatra API (sinatra, activerecord, nokogiri, rest-client, loofah, addressable, json)
│   └── workers.rb     # Sidekiq workers (sidekiq, tzinfo, rest-client, nokogiri)
├── test/
│   └── api_test.rb    # Minitest smoke tests = your post-upgrade validation gate
├── config.ru          # Rack + OmniAuth middleware stack
├── Rakefile           # `rake test` (exercises the pinned rake itself)
├── Gemfile            # The intentionally outdated pins
└── KNOWN_VULNERABILITIES.md  # Answer key for verifying your agent
```

## How to use it with your agent

1. Run `bundle install` (or `bundle lock`) once to produce a `Gemfile.lock` —
   most Ruby scanners (bundler-audit) read the lockfile, not the Gemfile.
2. Point the agent at the project. Expected detection: 14 outdated gems,
   13 with one or more CVEs (see `KNOWN_VULNERABILITIES.md`).
3. After the agent upgrades pins, run the validation gate:
   ```bash
   bundle install
   bundle exec rake test
   ```
4. Edge cases baked in for the agent to handle:
   - **sinatra 2.0 → 4.x** drags **rack 2 → 3** and **puma 3 → 6** with it —
     coupled major upgrades.
   - **activerecord 5.2 → 7.x** also forces **sqlite3 ~>1.3 → >=1.6** and
     changes `ActiveRecord::Base.establish_connection` defaults — breaking.
   - **tzinfo 1.x → 2.x** changes the API (`tz.to_local` exists in 2.x but
     `utc_to_local` semantics changed) — the worker code is written to survive.
   - **rest-client 1.8 → 2.x** changes exception classes.
   - **colorize 0.8.1** is outdated but has no CVE — tests whether your agent
     distinguishes "vulnerable" from merely "stale".

## Quick scan commands (for baseline comparison)

```bash
gem install bundler-audit
bundle lock          # generate Gemfile.lock without installing
bundle-audit check --update
```
