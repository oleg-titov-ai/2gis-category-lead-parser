# Useful SQL Queries

## Latest Jobs

```sql
SELECT *
FROM parser_jobs
ORDER BY started_at DESC
LIMIT 20;
```

## Companies by City and Category

```sql
SELECT
    name,
    city,
    category,
    address,
    phone,
    website,
    rating,
    reviews_count
FROM companies
WHERE city = 'Москва'
  AND category = 'Металлообработка'
ORDER BY created_at DESC;
```

## Contacts

```sql
SELECT
    c.name,
    cc.contact_type,
    cc.value,
    cc.source_url,
    cc.is_verified
FROM company_contacts cc
JOIN companies c ON c.id = cc.company_id
ORDER BY cc.created_at DESC;
```

## Job Summary

```sql
SELECT
    city,
    category,
    limit_requested,
    status,
    found_count,
    new_count,
    duplicate_count,
    enriched_count,
    started_at,
    finished_at
FROM parser_jobs
ORDER BY started_at DESC
LIMIT 10;
```
