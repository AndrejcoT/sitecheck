# Devlog — 30.03.2026

## Session goal

Plan the next stage of `sitecheck` and decide how to move from an early working prototype into a cleaner and more scalable structure.

## What I worked on

- Reviewed the current state of the project
- Confirmed that the CLI, generic checks, profile detection, and first WordPress checks were already working
- Planned the next set of features to build:
  - `WP_DEBUG` detection
  - `xmlrpc.php` warning
  - risky root files check
  - standardized result structure/output
  - first tests

## Why this session mattered

Until now, most of the project had been about getting the foundation working:
- package structure
- CLI command
- editable install
- first generic checks
- first WordPress checks

This session was about deciding what comes next so the project stays focused and grows in a useful direction.

## What I decided

The next features should not be random.

The best next path is:
1. add a real WordPress configuration check
2. add another simple but useful WordPress warning
3. improve generic website scanning
4. clean up how scan results are represented
5. start adding tests

## What I learned

- Planning the next few features ahead of time makes the project feel much less chaotic
- It is easier to build when the order of features makes sense
- At this stage, I need to balance:
  - useful checks
  - code quality
  - maintainability

## Current state

`sitecheck` is now beyond the “toy script” stage and has enough structure that future features should be added with more intention.

## Next step

Start with `WP_DEBUG` detection as the first real configuration-based WordPress check.