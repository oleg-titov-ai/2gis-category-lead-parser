# Maintenance checklist

Before publishing a demo export, confirm the CSV opens cleanly, row counts match the run summary, and no private lead data is included.

Record the parser version and category input used for any portfolio sample so the export can be reproduced later.

Use a small fixed test category after dependency updates to catch unexpected parsing or column-order changes.

Confirm empty search results produce a valid header-only export instead of a failed or malformed CSV.

Verify UTF-8 exports preserve non-Latin company names and addresses without replacement characters.

Compare export headers against the documented schema before release so downstream imports are not broken by silent column changes.
