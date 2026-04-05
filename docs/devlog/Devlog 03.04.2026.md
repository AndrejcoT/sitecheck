# Devlog — 03.04.2026

## Session goal

Improve generic website scanning by adding a risky root files check.

## What I worked on

- Added a generic check for risky or unnecessary files in the project root
- Focused on keeping the list of flagged files small and understandable
- Treated these findings as warnings instead of hard failures

## Why this feature matters

One of the goals of `sitecheck` is to support not only WordPress, but also more general website projects.

This feature helps with that because it checks for root-level files that might not belong in a production-ready project.

## Design decision

I did not want this feature to become a giant scanner for every possible risky file.

Instead, the idea is to start with a small, explicit set of checks that are easy to document and easy to reason about.

## What I learned

- Generic support needs to keep growing alongside the WordPress profile
- Scope control matters a lot
- A smaller clear feature is better than a huge vague one

## Current state

The scanner now feels more balanced:
- WordPress-specific checks are growing
- generic website checks are also getting stronger

## Next step

Clean up how results are represented and printed so the output becomes more standardized.