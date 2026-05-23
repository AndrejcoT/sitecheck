# Devlog 23.05.2026 - Sitecheck

## Main focus

Today the work was mostly about improving the CLI experience without changing the scanner itself.

The important design idea was that scan data should stay complete, and output flags should only decide how much of that data gets printed for a human.

## What changed

### `--only`

I added support for filtering text output by status:

- `sitecheck scan . --only pass`
- `sitecheck scan . --only warn`
- `sitecheck scan . --only fail`

This does not change the scan result, summary counts, verdict, or exit code. It only changes which individual result lines are shown in text output.

### `--summary`

I added a quick summary output mode:

- `sitecheck scan . --summary`

This prints the detected profile, verdict, summary counts, and verdict note, but hides the individual check result lines.

This is useful when I only want a quick overview instead of a full detailed report.

### Flag interactions

I also clarified and tested how the new output flags behave with existing flags:

- `--json --summary` still returns full JSON data
- `--deep --summary` still runs deep checks
- `--only warn --summary` shows summary output, so `--only` has no visible effect

That keeps the behavior simple: JSON is for automation, and `--only` / `--summary` are text display controls.

## Tests

The CLI tests now cover:

- `--only` filtering
- invalid and missing `--only` values
- summary mode hiding individual result lines
- summary mode preserving summary counts and verdict notes
- JSON ignoring summary mode
- deep scans still running when summary mode is enabled

The full test suite passed after the changes.

## Documentation

I updated the project docs so they match the current behavior:

- README usage examples
- output mode documentation
- changelog
- roadmap
- this devlog

## What I learned

The useful pattern here is separation of responsibility:

- scanner runs checks and returns complete data
- CLI parses user options
- renderer decides what to print

That makes it much easier to add output modes without accidentally changing scan behavior.
