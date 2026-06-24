# Testing Guide

## Scope

The current automated tests focus on parser behavior that can be verified without calling the real 2GIS API and without connecting to PostgreSQL.

Covered scenarios:

- demo mode respects the requested limit;
- generated `CompanyLead` objects serialize into dictionaries correctly;
- duplicate company IDs are removed during live collection;
- the live MVP rejects limits above 30 companies per run.

## Run Tests

From the repository root:

```bash
python3 -m unittest discover -s tests -v
```

Expected result:

```text
test_company_lead_to_dict_contains_expected_fields ... ok
test_demo_mode_respects_limit ... ok
test_live_collection_removes_duplicate_company_ids ... ok
test_live_mode_rejects_limit_above_mvp_cap ... ok
```

## Why the Tests Are Offline

The tests mock external API calls so that they are:

- reproducible;
- fast;
- safe for CI;
- independent of API keys;
- independent of network availability;
- free from rate-limit side effects.

## Future Test Coverage

Recommended next tests:

1. PostgreSQL integration test for inserting a new company;
2. PostgreSQL integration test for detecting an existing company;
3. enrichment-source persistence tests;
4. CSV export tests;
5. CLI argument validation;
6. malformed API response handling;
7. retry and timeout behavior.

## Security

Tests must never contain real API keys, real company exports, private contact data, or production database credentials.
