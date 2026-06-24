# Release Checklist

Use this checklist before publishing a tagged version or portfolio update.

## Code Quality

- [ ] Unit tests pass with `make test`.
- [ ] Demo mode works with `make demo`.
- [ ] GitHub Actions is green.
- [ ] New behavior has tests.
- [ ] Error messages are understandable.

## Security and Privacy

- [ ] No `.env` file is committed.
- [ ] No real API keys or database credentials are present.
- [ ] No real lead exports or private contacts are included.
- [ ] Screenshots use demo data.
- [ ] Production webhook URLs are removed.

## Documentation

- [ ] README reflects current behavior.
- [ ] Setup instructions are still valid.
- [ ] Testing guide is current.
- [ ] Changelog includes the new release.
- [ ] Known limitations are documented.

## Data and Database

- [ ] SQL migrations are safe to run.
- [ ] Duplicate handling is verified.
- [ ] Demo data can be loaded independently.
- [ ] CSV output contains only expected columns.

## Release

- [ ] Version number is selected.
- [ ] Release notes are prepared.
- [ ] Final commit messages are clear.
- [ ] Repository status is clean.
- [ ] Public files contain placeholders only.
