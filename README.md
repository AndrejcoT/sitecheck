# sitecheck

`sitecheck` is a Python CLI pre-deployment checker for websites and WordPress projects.

It scans a project folder and reports common deployment risks before a site is shipped. Results are returned as `PASS`, `WARN`, and `FAIL`, with both human-readable output and JSON output available.

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

## Output Modes

The default output is readable terminal text. It includes the detected profile, each check result, a summary, and a verdict.

JSON output is also supported for automation:

```bash
sitecheck scan . --json
```

Exit-code behavior:

- exits with `0` when there are no failures
- exits with `1` when one or more failures are found

Verdicts:

- `ready`
- `ready_with_warnings`
- `not_ready`

## Usage

Install locally in editable mode:

```bash
python -m pip install -e .[dev]
```

Run a scan:

```bash
sitecheck scan .
```

Run a scan with JSON output:

```bash
sitecheck scan . --json
```

Run tests:

```bash
python -m pytest
```

In restricted local environments, use a workspace-local pytest temp directory:

```bash
python -m pytest --basetemp=.pytest_tmp
```

## Example Output

```text
Detected profile: generic
Verdict: ready_with_warnings

PASS: Path exists
PASS: Path is a directory
WARN: .gitignore file not found

Summary:
PASS: 2
WARN: 1
FAIL: 0
```

Short JSON example:

```json
{
  "path": ".",
  "profile": "generic",
  "results": [],
  "summary": {
    "pass": 0,
    "warn": 0,
    "fail": 0
  },
  "verdict": "ready"
}
```

## Project Status

`sitecheck` is an active early-stage tool. It already has real generic and WordPress checks, structured scan results, JSON output, exit-code behavior, and automated tests.

The next focus is making the checks more useful, keeping the CLI clear, and preparing the project for regular CI runs.

## Why This Exists

Website deployments often rely on memory and manual checklists. `sitecheck` is meant to make basic deployment hygiene repeatable by catching common issues such as debug settings, exposed development files, and risky project-root artifacts.

It is also a practical DevOps learning project that can grow gradually without turning into a large platform too early.

## Roadmap

Near-term directions:

- expand GitHub Actions coverage
- more useful generic website checks
- more WordPress hardening checks
- clearer docs and examples
- future backend or database-related checks

## Testing

Tests are written with `pytest` and cover:

- generic checks
- WordPress checks
- profile detection
- scanner summary and verdict flow
- text and JSON rendering
- exit-code behavior
