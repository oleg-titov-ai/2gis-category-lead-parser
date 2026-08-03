# Maintenance Checks

Use this short checklist before sharing a demo export:

- Confirm the export timestamp is current and plausible.
- Verify the CSV row count matches the run summary.
- Spot-check that demo data contains no credentials, private contacts, or local paths.
- Reopen the file as UTF-8 and confirm headers match the documented schema.
- Confirm empty-result runs still produce a clear summary without a misleading CSV.
