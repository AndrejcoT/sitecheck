# Devlog — 02.04.2026

## Session goal

Add an `xmlrpc.php` warning to strengthen the WordPress profile.

## What I worked on

- Added a new WordPress-specific check for `xmlrpc.php`
- Decided to treat its presence as a warning rather than a failure
- Kept the logic simple and easy to understand

## Why this feature makes sense

`xmlrpc.php` is one of those WordPress files that often comes up in production/security discussions.

Even though this is still an early version of the tool, adding a warning for it makes the WordPress profile more recognizable and useful.

## Result logic

Current idea:
- `WARN` if `xmlrpc.php` is found
- `PASS` if it is not found

## Why this is a good early feature

It is:
- easy to explain
- easy to implement
- clearly WordPress-specific
- relevant to deployment hygiene

## What I learned

- Not every useful check has to be technically complex
- Some of the best early features are simple but meaningful
- Clear result meaning matters more than trying to look overly advanced

## Current state

The WordPress profile now includes:
- `wp-config.php`
- `wp-content`
- `readme.html`
- `WP_DEBUG`
- `xmlrpc.php`

## Next step

Return to the generic side of the project and add a risky root files check for normal websites and WordPress projects alike.