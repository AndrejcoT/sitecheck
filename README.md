# sitecheck

![Tests](https://github.com/AndrejcoT/sitecheck/actions/workflows/tests.yml/badge.svg)

`sitecheck` is a Python CLI pre-deployment checker for websites and WordPress projects.

It scans a project folder and reports common deployment risks before a site is shipped. Results are returned as `PASS`, `WARN`, and `FAIL`, with both human-readable output and JSON output available.

## Why This Exists

Website deployments often rely on memory and manual checklists. `sitecheck` is meant to make basic deployment hygiene repeatable by catching common issues such as debug settings, exposed development files, missing project files, and risky project-root artifacts.

It is also a practical DevOps learning project that can grow gradually without turning into a large platform too early.

## What It Checks

Generic website checks:

- path exists
- path is a directory
- Git repository is present
- `.gitignore` is present
- `.env` is protected by `.gitignore` when present
- suspicious backup or dump files in the project root
- debug, log, or temporary files in the project root
- public development files such as `phpinfo.php`, `debug.php`, and `test.php`
- Composer and npm lockfile consistency
- system files such as `.DS_Store` and `Thumbs.db`
- `node_modules` in the project root
- editor directories such as `.idea` and `.vscode`
- specific error log files

WordPress checks:

- `wp-config.php`
- `wp-content`
- `readme.html`
- `WP_DEBUG`
- `WP_DEBUG_LOG`
- `WP_DEBUG_DISPLAY`
- `DISALLOW_FILE_EDIT`
- `xmlrpc.php`
- `wp-config-sample.php`
- `license.txt`
- possible install files
- `WP_ENVIRONMENT_TYPE`
- `SCRIPT_DEBUG`
- `display_errors`

## Usage

Install locally in editable mode with development dependencies:

## Severity Rules

`sitecheck` currently uses a conservative severity model:

- `PASS` means the check found no issue.
- `WARN` means a possible deployment risk was found, but deployment may still be possible.
- `FAIL` means a hard blocker was found, such as an invalid path or missing required project structure.

Future versions may promote high-risk warnings to failures, especially for exposed secrets, database dumps, public debug output, or production-dangerous WordPress settings.

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

Scan the current directory and output JSON:

```bash
sitecheck scan . --json
```

Run tests:

```bash
python -m pytest
```
