# sitecheck

![Tests](https://github.com/AndrejcoT/sitecheck/actions/workflows/tests.yml/badge.svg)

`sitecheck` is a Python CLI pre-deployment checker for websites and WordPress projects.

It scans a project folder and reports common deployment risks before a site is shipped. Results are returned as `PASS`, `WARN`, and `FAIL`, with both human-readable output and JSON output available. Text output can also be narrowed with `--only` or shortened with `--summary` when a quick terminal view is enough.

## Why This Exists

Website deployments often rely on memory and manual checklists. `sitecheck` makes basic deployment hygiene repeatable by catching common issues such as debug settings, exposed development files, missing project files, and risky project-root artifacts.

It is also a practical DevOps learning project that can grow gradually without turning into a large platform too early.

## What It Checks

### Generic Checks

| Check area | What it reviews |
| --- | --- |
| Path validation | Path exists and is a directory |
| Git hygiene | Git repository, `.gitignore`, and `.env` handling |
| Root risky files | Backup/archive files, public development files, database files, and `.htaccess` external redirects |
| Dependency files | Composer and npm lockfile consistency |
| Local artifacts | `node_modules`, editor directories, system files, debug/temp files, and error logs |

### WordPress Checks

| Check area | What it reviews |
| --- | --- |
| WordPress structure | `wp-config.php`, `wp-content`, and partial WordPress detection |
| Public WordPress files | `readme.html`, `xmlrpc.php`, `wp-config-sample.php`, `license.txt`, and install files |
| Debug settings | `WP_DEBUG`, `WP_DEBUG_LOG`, `WP_DEBUG_DISPLAY`, `SCRIPT_DEBUG`, and `display_errors` |
| Hardening settings | `DISALLOW_FILE_EDIT` and `WP_ENVIRONMENT_TYPE` |
| Suspicious indicators | `wp-content/debug.log`, PHP files inside uploads, disguised PHP files in plugins, and suspicious PHP patterns in uploads |
| Deep scan only | Unexpected PHP files directly inside `wp-content` and PHP files inside `wp-content/cache` |

## Severity Rules

`sitecheck` uses a conservative severity model:

| Status | Meaning |
| --- | --- |
| `PASS` | The check found no issue. |
| `WARN` | A possible deployment risk was found, but deployment may still be possible. |
| `FAIL` | A hard blocker was found, such as an invalid path or missing required project structure. |

Sitecheck reports indicators, not proof of compromise. It avoids wording such as "malware detected" because filenames and code patterns can have legitimate explanations.

## Usage

Install locally in editable mode with development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Show help:

```bash
sitecheck --help
```

Check the installed version:

```bash
sitecheck --version
```

Scan the current directory:

```bash
sitecheck scan .
```

Run deeper, noisier WordPress checks:

```bash
sitecheck scan . --deep
```

Show only one status in text output:

```bash
sitecheck scan . --only warn
```

Show only the profile, verdict, summary counts, and verdict note:

```bash
sitecheck scan . --summary
```

## Output Modes

Human-readable output is the default:

```text
Detected profile: wordpress
Verdict: ready_with_warnings

WARN: PHP files found inside wp-content/uploads; review them before production deployment
  Details:
    - wp-content/uploads/2026/05/logo.png.php
    - wp-content/uploads/2026/05/shell.php

Summary:
PASS: 27
WARN: 6
FAIL: 0

Review WARN items before deployment.
```

Filter human-readable output by status:

```bash
sitecheck scan . --only fail
```

`--only` does not change the scan result, summary counts, verdict, or exit code. It only hides non-matching individual result lines in text output.

Use summary mode for a quick overview:

```bash
sitecheck scan . --summary
```

Example summary output:

```text
Detected profile: generic
Verdict: ready

Summary:
PASS: 16
WARN: 0
FAIL: 0
```

`--summary` changes text output only. The full scan still runs, summary counts are unchanged, and the exit code still depends on whether any `FAIL` results exist.

JSON output is available for automation:

```bash
sitecheck scan . --json
```

JSON output always returns the full scan data. Output display flags such as `--only` and `--summary` do not filter JSON results.

Example JSON shape:

```json
{
  "path": ".",
  "profile": "wordpress",
  "results": [],
  "summary": {
    "pass": 0,
    "warn": 0,
    "fail": 0
  },
  "verdict": "ready"
}
```

## Configuration

Ignore checks with `.sitecheck.toml` in the scanned project root:

```toml
[ignore]
checks = ["xmlrpc", "node_modules"]
```

Ignored checks are omitted from results and summary counts.

## Testing

Run tests:

```bash
python -m pytest
```

On Windows/OneDrive setups where pytest temp folders can be locked, use a fresh local base temp directory:

```powershell
$stamp = Get-Date -Format 'yyyyMMddHHmmssfff'
python -m pytest --basetemp ".pytest_tmp_$stamp"
```

## Continuous Integration

GitHub Actions runs the test suite on push and pull request events.

## Project Status

This project is pre-release and intentionally small. The current focus is fast, low-noise deployment checks with optional deeper WordPress checks behind `--deep`. Recent work has focused on keeping scan data complete while making terminal output easier to control with `--only` and `--summary`.

## Roadmap

- Improve WordPress profile detection further as real projects expose edge cases.
- Expand configuration only where it reduces noise without hiding important failures.
- Keep default scans fast and conservative.
- Keep deeper or noisier checks behind explicit flags.
- Keep text output useful for both detailed review and quick summaries.
