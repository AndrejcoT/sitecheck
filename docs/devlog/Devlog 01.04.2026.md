# Devlog — 01.04.2026

## Session goal

Refine the `WP_DEBUG` check and make sure it fits naturally into the WordPress scan flow.

## What I worked on

- Improved the `WP_DEBUG` detection logic
- Reviewed how the result is displayed during a WordPress scan
- Made sure the check follows the same style as the rest of the scanner:
  - status
  - message
- Thought through how to handle cases where the setting is present but not obvious

## Why this session mattered

Adding a new check is one thing.
Making sure it fits the structure of the project is another.

This session was useful because it pushed me to think more about consistency instead of only adding features quickly.

## What I improved

- Better fit between WordPress checks and the scan flow
- Clearer thinking around when to use `PASS` vs `WARN`
- More confidence that `WP_DEBUG` belongs as a real first WordPress config check

## What I learned

- A feature is not really done when the code exists
- It is done when:
  - it fits the architecture
  - its output is understandable
  - it behaves consistently with the rest of the tool

## Current state

The WordPress profile now feels more real:
- file checks
- folder checks
- `readme.html`
- `WP_DEBUG`

## Next step

Add another simple but useful WordPress check: `xmlrpc.php`.