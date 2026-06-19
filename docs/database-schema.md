# Database Schema

This project uses PostgreSQL as a small lead-research database.

## Tables

### `parser_jobs`

Stores each parser run.

| Column | Purpose |
|---|---|
| `id` | Job ID |
| `city` | Selected city |
| `category` | Selected business category |
| `limit_requested` | Requested company limit |
| `status` | Job status |
| `found_count` | Number of companies returned by the collector |
| `new_count` | New companies inserted into the database |
| `duplicate_count` | Existing companies detected by deduplication |
| `enriched_count` | Number of saved enrichment source records |
| `started_at` / `finished_at` | Run timestamps |

### `companies`

Stores normalized company cards collected from 2GIS.

Deduplication is based on:

```text
source + source_company_id
```

Important fields:

| Column | Purpose |
|---|---|
| `source` | Data source, e.g. `2gis` |
| `source_company_id` | External company ID from the source |
| `name` | Company name |
| `category` | Requested category |
| `city` | City |
| `address` | Address |
| `phone` | Phone if available from API permissions |
| `website` | Website if available from API permissions |
| `rating` | Public rating |
| `reviews_count` | Number of public reviews |
| `latitude` / `longitude` | Geo coordinates |

### `company_contacts`

Stores manually or externally verified contacts.

| Column | Purpose |
|---|---|
| `company_id` | Link to company |
| `contact_type` | `phone`, `website`, or `email` |
| `value` | Contact value |
| `source_url` | Where the contact was found |
| `is_verified` | Whether a human confirmed the contact |

Unique constraint:

```text
company_id + contact_type + value
```

### `enrichment_sources`

Stores enrichment hints and source links for manual or API-based research.

Examples:

```text
google_search
yandex_search
2gis_card
company_website
search_query
```

### `job_companies`

Many-to-many link between parser jobs and companies.

This allows seeing which companies were returned in each run.

## Useful Checks

```bash
psql -d lead_parser_demo_db \
  -c "SELECT 'companies' AS table_name, COUNT(*) FROM companies
      UNION ALL
      SELECT 'parser_jobs', COUNT(*) FROM parser_jobs
      UNION ALL
      SELECT 'enrichment_sources', COUNT(*) FROM enrichment_sources
      UNION ALL
      SELECT 'company_contacts', COUNT(*) FROM company_contacts
      UNION ALL
      SELECT 'job_companies', COUNT(*) FROM job_companies;"
```

```bash
psql -d lead_parser_demo_db \
  -c "SELECT c.id, c.name, cc.contact_type, cc.value, cc.source_url, cc.is_verified
      FROM company_contacts cc
      JOIN companies c ON c.id = cc.company_id
      ORDER BY cc.id DESC;"
```
