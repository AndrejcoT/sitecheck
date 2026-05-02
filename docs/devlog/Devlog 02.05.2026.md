# Devlog — 02.05.2026

## Session goal

Start implementing structured scan results so `sitecheck` can support both normal text output and future JSON output.

## What I worked on

Today I focused on changing the internal shape of the project instead of adding more checks.

The main goal was to move `sitecheck` away from directly printing scan results during the scan process and toward returning structured data that can later be rendered in different formats.

### Work completed

- Refactored the generic checks so each one returns a structured dictionary instead of a simple tuple
- Standardized generic check output around:
  - `check`
  - `status`
  - `message`
- Refactored the WordPress checks to return the same structured result shape
- Cleaned up and standardized the check names across WordPress checks
- Worked through multiple issues in the `WP_DEBUG` check, including naming consistency and result structure
- Updated `profiles.py` so profile detection stays simple and readable
- Started refactoring `scanner.py`
- Removed the old result-printing mindset from the scanner and began moving toward a result-collection mindset
- Replaced the old summary-printing logic with a summary builder that counts:
  - pass
  - warn
  - fail
- Refactored the scanner flow so it can return a full scan result dictionary instead of only printing output
- Began preparing `cli.py` for the new workflow where it receives scan data and later decides how to render it

## Main architectural shift

The biggest change today was mental, not just technical.

Before today, the project mostly worked like this:

- run checks
- print results immediately
- print summary immediately

Now the project is moving toward this model:

- checks return structured data
- scanner collects all results
- scanner returns one full scan result
- CLI decides how to display it

That is an important shift because it opens the door to:
- JSON output
- better testing
- exit codes
- cleaner architecture

## What I learned

- A scanner should not also be the renderer
- Checks should return data, not print directly
- Returning structured dictionaries makes the project much easier to extend
- The difference between:
  - scan logic
  - rendering logic
  - CLI command handling
  is becoming much clearer
- Building a feature like JSON output starts much earlier than the final output function — it starts with how the data is shaped internally

## Problems I ran into

- I got confused a few times about whether logic should stay in `scanner.py` or move into other files
- I needed to rethink old tuple-based logic because the project now uses dictionaries for results
- The `WP_DEBUG` check was the most overwhelming part because it involved more than simple file existence logic
- I had to slow down and think more carefully about responsibilities:
  - checks
  - scanner
  - CLI
  instead of just trying to make the code work quickly

## What improved today

The project now feels much more like a real CLI tool in progress rather than a script that happens to work.

The internal structure is stronger because:
- checks are more consistent
- scan results are becoming reusable
- the path toward text output + JSON output is much clearer

## Current state

By the end of today:

- generic checks return structured result dictionaries
- WordPress checks return structured result dictionaries
- profile detection is still simple and clean
- summary counting is being handled through returned data instead of printing
- the scanner is being transformed into a function that returns scan data
- the CLI is the next place to finish this feature

## Next step

Finish the CLI side of the new flow:

- capture the result returned by `scan(path)`
- render text output from the returned scan data
- add `--json` support afterward