# Weekly Devlog — Sitecheck

## Note

I forgot to write devlogs on each individual day I worked on `sitecheck`, so this is one bigger weekly devlog to capture the progress from the whole week in one place.

## Main focus of the week

This week was mostly about making `sitecheck` feel more like a real tool instead of just a script that prints some checks.

A lot of the work was not only about adding new checks, but also about improving the internal structure so the tool is easier to grow, test, and use later.

## What I worked on

### 1. Structured scan results

One of the biggest shifts this week was moving away from loose scan output and toward structured data.

Instead of having checks return very small simple results and printing everything directly during the scan, I worked on making the project return more consistent structured scan results.

That meant:
- checks now return dictionaries with a consistent shape
- the scanner collects results
- the scanner returns a full scan result
- the CLI can then decide how to display that result

This was one of the most important improvements because it made later features like JSON output and exit codes much easier.

### 2. Scanner refactor

I refactored the scanner so it behaves more like a real scanner and less like a printer.

Before, the scanner was doing a bit too much:
- running checks
- printing results
- printing the summary

Now the scanner is much closer to this model:
- run checks
- collect results
- build summary
- return scan data

That change also helped separate responsibilities better between:
- checks
- scanner
- CLI output

### 3. JSON output and text output

I worked on making `sitecheck` support multiple output modes from the same scan data.

That means the same scan result can now be shown as:
- human-readable text
- JSON

This made the project feel much more DevOps-oriented because it is no longer only about terminal output for a human. It can now also produce output that machines and automation could use later.

### 4. Exit-code handling

I added exit-code logic so the project can return a proper code depending on the scan result.

This is important because it makes `sitecheck` more useful in automation and CI-style flows.

This also pushed me to understand a bit more clearly how the CLI should behave:
- run the scan
- show output
- return the proper exit code

### 5. First real tests

This week was also the point where testing became a real part of the project.

I added the first real tests and got pytest running inside the virtual environment.

At first the project only had manual checking, but now there is actual automated test coverage.

That already makes the project feel much more serious.

### 6. Expanded test coverage

After the initial tests were working, I kept expanding the test coverage.

Tests now cover:
- exit code behavior
- generic checks
- WordPress checks
- profile detection
- summary counting
- scanner flow
- text rendering
- JSON rendering

This helped confirm that the core structure of the project still works even as features are added.

### 7. `.env` handling check

A big practical improvement this week was the `.env` handling logic.

I initially thought about warning if `.env` existed, but that turned out not to be a good idea because many projects legitimately need `.env`.

The more useful logic became:
- `.env` missing is fine
- `.env` existing is also fine
- the real concern is whether `.env` is safely handled through `.gitignore`

So the final direction became much better:
- `.env` present but not protected by `.gitignore` should warn
- `.env` handled safely should pass

That made the tool feel more realistic and less noisy.

### 8. Suspicious files check

I also added a new generic check for suspicious files in the project root.

The idea was to look for things like:
- `.sql`
- `.dump`
- `.bak`
- `.backup`
- archive-like files

This check is meant to catch obvious backup or dump artifacts that should probably not be sitting in the root of a deployment-ready project.

I also kept the logic root-only to avoid scanning the entire project recursively and causing unnecessary noise.

### 9. More tests for new checks

After adding the new `.env` logic and suspicious files logic, I also upgraded the tests again.

That included:
- dedicated tests for `.env` handling
- tests for suspicious file detection
- scanner-level checks proving the scan actually includes those new checks

This was useful because it confirmed not only that the functions worked alone, but also that the full scan flow was really using them.

## What I learned

This week taught me a lot, especially around structure and responsibility.

Some of the biggest lessons were:

- checks should return data, not print directly
- scanner logic and output rendering should not be mixed together
- structured data makes future features much easier
- tests become much more valuable once the project has enough moving parts
- a practical check is often better than a noisy one
- not every useful improvement is a flashy feature — a lot of value comes from better internal structure

## What was difficult

A few parts were more overwhelming than I expected:
- refactoring from simple results into structured scan data
- figuring out which logic belongs in checks, scanner, and CLI
- making the `.env` check useful without making it noisy
- keeping the suspicious files check practical without overcomplicating it
- staying consistent while the project kept growing

There were also moments where I felt a bit lost because the code was no longer just “small script” territory and started needing more intentional design.

## Current state of the project

At the end of this week, `sitecheck` now has:

- a working Python CLI
- structured scan results
- text and JSON output
- exit-code handling
- generic checks
- WordPress checks
- profile detection
- `.env` handling logic
- suspicious file detection
- broad test coverage
- a much stronger internal structure than before

## What is next

The next stage is to keep making the tool more practically useful by adding more real-world checks while keeping the structure clean.

Likely next directions:
- improve suspicious file logic further if needed
- add more useful generic checks
- keep expanding test coverage as features are added
- later move toward GitHub Actions once the feature set feels a bit more mature

## Weekly summary

This week was less about one giant flashy feature and more about leveling up `sitecheck` as a real project.

I improved the architecture, added more useful checks, introduced stronger testing, and made the tool feel more like something that could realistically keep growing instead of just being a small script.