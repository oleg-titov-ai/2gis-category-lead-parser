# Roadmap

## Current MVP

- 2GIS category collection
- demo mode
- PostgreSQL persistence
- parser job history
- deduplication
- enrichment queue
- manually verified contacts
- CSV export
- terminal report

## Next Improvements

### 1. Contact Enrichment Provider Interface

Add a clean provider interface:

```text
SearchProvider
WebsiteContactExtractor
ContactVerifier
```

This would allow connecting permitted search/data APIs without changing the core pipeline.

Use only providers and data sources whose terms permit the intended enrichment workflow.

### 2. Deduplication for Enrichment Sources

Add a uniqueness rule for enrichment sources:

```text
company_id + source_type + source_url + raw_text
```

This prevents duplicate enrichment links after repeated parser runs.

### 3. Export Improvements

Add additional export formats:

- CSV;
- JSON;
- Excel;
- CRM-ready import file;
- automated validation of required columns before export;
- explicit UTF-8 encoding checks for exported text fields;
- a small regression fixture for verifying column order and headers.

### 4. Verification Dashboard

Build a small web interface for reviewing contacts:

```text
pending contact → approve/reject → verified contact
```

### 5. CRM Integration

Possible integrations:

- HubSpot;
- Airtable;
- Google Sheets;
- Telegram notifications;
- n8n workflow.

### 6. Testing

Add tests for:

- category validation;
- company normalization;
- database upsert logic;
- enrichment source generation;
- CSV export.

### 7. Deployment

Possible deployment options:

- local CLI only;
- Docker Compose with PostgreSQL;
- scheduled n8n workflow;
- small admin dashboard.

## Product Direction

The long-term direction is a lightweight B2B lead research pipeline:

```text
Data source API
    ↓
Company database
    ↓
Enrichment queue
    ↓
Verified contacts
    ↓
CRM / outreach workflow
```
