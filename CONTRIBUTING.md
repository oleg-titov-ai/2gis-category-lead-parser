# Contributing

Thanks for your interest in improving 2GIS Category Lead Parser.

## Development Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
make install
```

## Run Tests

```bash
make test
```

All changes should keep the test suite green.

## Run Demo Mode

```bash
make demo
```

Demo mode must remain safe and must not require a real API key.

## Contribution Rules

- Do not commit `.env` files.
- Do not include real API keys or database credentials.
- Do not upload real lead exports or private contact data.
- Keep the live collection limit and request-delay safeguards.
- Do not add captcha bypassing, cookie theft, proxy rotation, or search-engine scraping.
- Add or update tests when changing parser behavior.
- Keep public examples based on placeholders and demo data.

## Pull Request Checklist

- [ ] The project runs locally.
- [ ] Unit tests pass.
- [ ] No secrets are included.
- [ ] Documentation is updated when behavior changes.
- [ ] Demo mode still works without external services.
- [ ] New dependencies are justified.

## Commit Style

Use clear commit messages, for example:

```text
feat: add CSV filtering
fix: handle malformed API response
test: cover duplicate company IDs
docs: explain PostgreSQL setup
```
