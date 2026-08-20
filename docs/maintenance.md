# Maintenance

- 2026-08-19: Before sharing a portfolio CSV, verify its filename, row count, checksum, collection date, source commit, and provenance note all describe the same generated artifact.
- 2026-08-20: Keep a documented empty-result check so zero-match runs still produce a valid header-only CSV with the expected schema and no stale rows from prior exports.
- 2026-08-20: Keep portfolio export samples limited to documented public/demo source fields so private enrichment columns cannot appear accidentally in shared CSV files.
