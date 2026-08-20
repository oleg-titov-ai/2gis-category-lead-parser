# Maintenance

- 2026-08-19: Before sharing a portfolio CSV, verify its filename, row count, checksum, collection date, source commit, and provenance note all describe the same generated artifact.
- 2026-08-20: Keep a documented empty-result check so zero-match runs still produce a valid header-only CSV with the expected schema and no stale rows from prior exports.
