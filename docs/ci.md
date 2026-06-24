# Continuous Integration

The repository uses GitHub Actions to run automated tests on every push to `main` and on every pull request targeting `main`.

## Workflow

The CI pipeline performs these steps:

1. checks out the repository;
2. installs Python 3.12;
3. restores the pip cache when available;
4. installs dependencies from `requirements.txt`;
5. runs the unit test suite.

## Test Command

```bash
python -m unittest discover -s tests -v
```

## Why CI Matters

Continuous integration helps detect regressions before changes are merged. It also proves that the public portfolio version can be installed and tested in a clean environment without local secrets, PostgreSQL, or access to the real 2GIS API.

## Current Coverage

The workflow currently validates:

- demo-mode limits;
- company serialization;
- duplicate company ID handling;
- live-mode limit validation.

## Future Improvements

- PostgreSQL service container for integration tests;
- code coverage report;
- linting and formatting checks;
- dependency vulnerability scanning;
- test matrix for multiple Python versions.
