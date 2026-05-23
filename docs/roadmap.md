# Roadmap

## Current Status

`sitecheck` is an active early-stage Python CLI tool for pre-deployment website checks.

The project already includes:

- Python package structure
- working CLI entry point
- `sitecheck scan <path>`
- generic website checks
- WordPress profile detection
- WordPress-specific checks
- structured scan results
- human-readable terminal output
- JSON output
- text output filtering with `--only`
- quick summary text output with `--summary`
- summary counts
- scan verdicts
- exit-code behavior
- optional deep WordPress checks with `--deep`
- `.sitecheck.toml` ignore support
- automated tests with `pytest`
- focused test files for CLI, scanner, profiles, generic checks, and WordPress checks
- GitHub Actions CI for push and pull requests

The project is no longer only in the foundation stage. The foundation is working, the test suite is broad, and the next focus is improving polish, documentation, and practical usefulness without making the CLI noisy.

---

## Now

### Project cleanup and documentation

- Keep README accurate with current features
- Add a basic `CONTRIBUTING.md`
- Improve docs and examples
- Keep weekly devlogs updated

### Test organization

- Keep focused test files easy to navigate
- Add regression tests for every new CLI flag and check
- Keep tests green after documentation and cleanup work

### Existing check improvements

- Review current generic checks for message consistency
- Review current WordPress checks for message consistency
- Make warning messages more helpful and actionable
- Avoid adding too many new checks before cleaning the current ones

---

## Next

### More useful generic website checks

- Improve detection of risky root files
- Add clearer handling for common deployment artifacts
- Improve Composer and npm-related checks
- Add more practical examples for generic projects

### More useful WordPress checks

- Improve WordPress hardening checks
- Add safer handling of `wp-config.php` parsing
- Consider optional WP-CLI detection
- Consider checks for common risky WordPress files or settings
- Keep WordPress checks practical and not overly aggressive

### Developer experience

- Keep CLI help text accurate as flags are added
- Improve output clarity without changing scan data
- Add more README examples
- Add example project folders for testing/demo purposes
- Keep CLI help and version output accurate

---

## Later

### Configuration support

- Expand optional config file support if a real need appears
- Keep ignore-check behavior documented and predictable
- Allow users to adjust warning behavior
- Keep default behavior simple

### More profiles

Possible future profiles:

- static site profile
- PHP project profile
- Node project profile

These should only be added when the generic and WordPress profiles feel stable.

### CI improvements

- Consider testing multiple Python versions
- Consider adding linting later
- Consider adding formatting checks later
- Consider coverage reporting later

Do not add these too early. The current priority is useful checks and clean structure.

### Release preparation

- Improve package metadata
- Add release notes
- Prepare for tagged releases
- Consider publishing later only if the tool becomes useful enough

---

## Future Possible Growth

Longer-term ideas:

- backend/environment checks
- database-related deployment checks
- CI-focused output improvements
- deployment checklist generation
- more advanced WordPress security checks
- integration with real deployment workflows

These are not immediate priorities.

---

## Rules for Roadmap Decisions

When adding features, follow these rules:

1. Keep the project small enough to ship.
2. Prefer useful over impressive.
3. Build one clear thing at a time.
4. Do not turn V1 into a giant platform.
5. Every feature should either:
   - improve the CLI foundation,
   - improve generic checks,
   - improve WordPress support,
   - improve test quality,
   - or improve usability and documentation.
6. Do not add complex features before the current structure is clean.
7. Green tests should remain the baseline after every change.
