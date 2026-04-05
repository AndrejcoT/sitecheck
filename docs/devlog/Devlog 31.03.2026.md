# Devlog — 31.03.2026

## Session goal

Implement the first real WordPress configuration check by adding `WP_DEBUG` detection.

## What I worked on

- Added a new WordPress-specific check for `WP_DEBUG`
- Made the tool inspect `wp-config.php` instead of only checking whether the file exists
- Built the check so it can report whether `WP_DEBUG` appears to be:
  - enabled
  - disabled
  - unclear or not easily detected

## Why this was important

This is one of the first checks in the project that feels like real configuration analysis instead of only checking whether files or folders are present.

It makes `sitecheck` more useful because `WP_DEBUG` is one of the WordPress settings that matters for production readiness.

## Result logic

Current thinking for `WP_DEBUG`:
- `PASS` if it appears disabled
- `WARN` if it appears enabled
- `WARN` if it is not clearly detected

## What I learned

- Reading file contents in Python opens the door to much more useful checks
- Configuration-based checks are more valuable than surface-level existence checks
- Even simple checks become more useful when they reflect real deployment concerns

## Challenges

- `wp-config.php` can be written in different styles
- The check does not need to be perfect yet, but it should be clear and useful
- It is important not to overcomplicate the first version

## Current state

`sitecheck` now has one real WordPress logic check in addition to file/folder checks.

## Next step

Test and improve the `WP_DEBUG` detection logic so it behaves more reliably across slightly different config formats.