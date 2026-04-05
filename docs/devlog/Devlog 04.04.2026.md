# Devlog — 04.04.2026

## Session goal

Standardize the scan results so the output is more consistent and easier to extend later.

## What I worked on

- Cleaned up the way results are represented internally
- Made the output feel more consistent across generic and WordPress checks
- Improved the structure so every check follows the same general pattern

## Why this matters

As the number of checks grows, inconsistent output quickly becomes annoying.

This session was less about adding visible features and more about improving the quality of the scanner engine so future work is easier.

## What improved

- more predictable result handling
- clearer scan output
- better consistency between checks
- a stronger foundation for future features like JSON output, config support, or better summaries

## What I learned

- internal consistency saves a lot of pain later
- even when users only see printed lines, the structure behind those lines matters
- it is worth pausing feature work to improve the foundation

## Current state

`sitecheck` is starting to feel less like a script and more like a real project with reusable patterns.

## Next step

Begin adding the first real tests so the project becomes safer to refactor.