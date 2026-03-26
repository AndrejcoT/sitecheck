# Roadmap

## Now

### Foundation
- Create repository structure
- Set up Python package layout
- Add `pyproject.toml`
- Create initial docs
- Create GitHub issue/project workflow

### CLI foundation
- Create `sitecheck` package
- Add `cli.py`
- Add `main()` function
- Make `sitecheck --help` work
- Make `sitecheck scan <path>` work with placeholder output

## Next

### Generic website support
- Add more generic checks
- Add simple structure validation
- Add debug/dev artifact warnings
- Add backup-related warning logic
- Improve CLI help and output clarity

### WordPress support
- Detect WordPress root
- Check for `wp-config.php`
- Check for `wp-content`
- Add `WP_DEBUG` warning
- Add `readme.html` warning
- Add optional WP-CLI detection

### Project quality
- Add tests
- Improve docs
- Add examples folder content
- Keep devlog updated
- Start collecting reusable post ideas from progress

## Later

### Static site profile
- Detect static site structure
- Check for `index.html`
- Check for assets/build output
- Warn on obvious deployment mistakes

### Better developer experience
- Add config file support
- Add JSON output
- Add ignore rules
- Improve result formatting

### GitHub integration
- Add GitHub Actions for linting and tests
- Add release workflow later
- Prepare the project for open-source contributions

### Future possible growth
- PHP profile
- Node profile
- CI-focused output improvements
- more advanced deployment guidance

## Rules for roadmap decisions

When adding features, follow these rules:

1. Keep the project small enough to ship.
2. Prefer useful over impressive.
3. Build one clear thing at a time.
4. Do not turn V1 into a giant platform.
5. Every feature should either:
   - improve the CLI foundation,
   - improve generic checks,
   - improve WordPress support,
   - or improve usability and documentation.