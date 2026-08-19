# Security Rules

## Never Commit

- `.env` files;
- real API keys;
- cookies;
- session files;
- private headers;
- production exports;
- real lead CSV files;
- database dumps;
- screenshots with private data.

## Safe Placeholders

```text
DEMO_DGIS_API_KEY
DEMO_COMPANY_ID
DEMO_PHONE
DEMO_EMAIL
CHANGE_ME_LOCALLY
```

## Local Check Before Push

```bash
git status
git diff --cached
```

Before publishing an export, open the CSV once and confirm it contains no unintended local paths, internal IDs, or private contact data.

Also confirm demo exports do not include hidden enrichment columns that are not documented for public use.

Confirm shared demo exports identify only the intended public/demo source and do not expose internal enrichment source metadata.

Record which demo command produced a published CSV so portfolio exports remain reproducible and clearly separate from production data.

Confirm any committed demo CSV uses a documented, stable column set so downstream portfolio examples remain reproducible.

Confirm published source URLs point only to intentionally public pages and do not expose private enrichment endpoints or query tokens.

Confirm each published demo export can be traced to a documented public/demo source without including private lookup metadata.

Use neutral export filenames that do not contain client names, account names, or local usernames.

## Secret Search

```bash
grep -RniE "token|secret|password|api_key|api_secret|cookie|session|authorization|bearer|chat_id|user_id|webhook" . \
  --exclude-dir=.git \
  --exclude=.env.example
```

## If a Secret Was Committed

1. Revoke or rotate it.
2. Remove it from code.
3. Review Git history before making the repository public.
