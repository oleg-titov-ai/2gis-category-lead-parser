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
