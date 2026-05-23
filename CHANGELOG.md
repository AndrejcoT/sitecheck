# Changelog

All notable changes to this project will be documented in this file.

This project does not have official releases yet. Current changes are tracked under `Unreleased`.

## Unreleased

### Added

- Added Python package structure using `src/sitecheck`.
- Added CLI entry point for `sitecheck`.
- Added `sitecheck scan <path>` command.
- Added generic website checks.
- Added WordPress profile detection.
- Added WordPress-specific checks.
- Added structured scan results.
- Added human-readable terminal output.
- Added JSON output with `--json`.
- Added summary counts for `PASS`, `WARN`, and `FAIL`.
- Added scan verdicts:
  - `ready`
  - `ready_with_warnings`
  - `not_ready`
- Added exit-code behavior:
  - `0` when no failures are found
  - `1` when one or more failures are found
- Added automated tests with `pytest`.
- Added GitHub Actions workflow to run tests on push and pull requests.
- Added README documentation for usage, testing, and CI.
- Added database file checks.
- Added `.htaccess` external redirect checks.
- Added WordPress `wp-content/debug.log` check.
- Added WordPress uploads PHP file check.
- Added WordPress disguised plugin PHP file check.
- Added WordPress suspicious PHP pattern check.
- Added optional deep scan mode with `--deep`.
- Added deep WordPress checks for unexpected PHP files directly inside `wp-content`.
- Added deep WordPress checks for PHP files inside `wp-content/cache`.
- Added `.sitecheck.toml` support for ignoring check IDs.
- Added `--only <status>` text output filtering for `pass`, `warn`, and `fail` results.
- Added `--summary` text output mode for quick profile, verdict, summary counts, and verdict note output.
- Added CLI tests for `--only`, `--summary`, JSON interaction, deep scan interaction, and validation errors.

### Changed

- Improved scanner flow to return structured scan data.
- Improved CLI output clarity.
- Improved WordPress config parsing helpers.
- Improved generic check helper functions.
- Updated README to reflect current project status.
- Improved WordPress profile detection for partial WordPress projects.
- Improved text output details formatting for multi-item details.
- Improved text output with verdict guidance for warnings and failures.
- Improved CLI help examples to include output filtering and summary mode.
- Split automated tests into focused files for CLI, scanner, profiles, generic checks, and WordPress checks.

### Fixed

- Fixed local development setup by using editable installs with development dependencies.
- Fixed CI visibility by adding a GitHub Actions status badge.
