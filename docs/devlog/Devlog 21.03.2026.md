## Problem I ran into

I deleted and rewrote parts of `cli.py`, then got confused about why the `sitecheck` command stopped working.

## What caused it

The entry point in `pyproject.toml` points to `sitecheck.cli:main`, and my new file did not include a `main()` function.

## What I learned

The installed CLI command depends on the entry point chain staying valid:
`sitecheck -> sitecheck.cli -> main()`

## Rule for future me

If the command stops working, first check:
- `cli.py` exists
- `main()` exists
- `pyproject.toml` points to the right place