# vulnerable-sample-app

A deliberately outdated Maven project for testing dependency/plugin remediation agents.
**Do not deploy.** Every version here is pinned to a known-vulnerable or stale release on purpose.

## Outdated / vulnerable dependencies

| Dependency | Current (bad) | Notable CVE(s) | Suggested fixed version |
|---|---|---|---|
| log4j-core / log4j-api | 2.14.1 | CVE-2021-44228 (Log4Shell), CVE-2021-45046 | 2.23.1+ |
| jackson-databind | 2.9.8 | Multiple RCE (CVE-2019-12384, etc.) | 2.17.x+ |
| snakeyaml | 1.30 | CVE-2022-1471 | 2.2+ |
| commons-collections | 3.2.1 | CVE-2015-7501 (deserialization) | 3.2.2 / migrate to 4.x |
| spring-core / spring-web | 5.3.16 | CVE-2022-22965 (Spring4Shell) | 5.3.39+ / 6.x |
| commons-text | 1.9 | CVE-2022-42889 (Text4Shell) | 1.10.0+ |
| guava | 24.1.1-jre | CVE-2020-8908, CVE-2023-2976 | 33.x |
| httpclient | 4.5.3 | several | 4.5.14 / migrate to 5.x |
| junit | 4.12 | stale | 4.13.2 / migrate to JUnit 5 |

## Outdated build plugins

| Plugin | Current (bad) | Suggested |
|---|---|---|
| maven-compiler-plugin | 3.1 | 3.13.0+ |
| maven-surefire-plugin | 2.18.1 | 3.2.5+ |
| maven-shade-plugin | 2.4.3 | 3.6.0+ |
| maven-jar-plugin | 2.4 | 3.4.1+ |

## Build

```bash
mvn -q -DskipTests package   # may require old plugin downloads
mvn test
```

## What a remediation agent should do

1. Detect each outdated dependency and plugin version.
2. Map to known CVEs and recommend the lowest safe upgrade.
3. Update `pom.xml` (ideally with breaking-change warnings for major bumps like guava 24→33, spring 5→6, junit 4→5).
4. Re-run tests / scan to confirm.
