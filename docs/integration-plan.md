# Integration Plan

## Goal

Turn the lead parser into a reusable lead-generation component that can send structured company data into automation workflows and CRM systems.

## Target Flow

```text
2GIS Category Lead Parser
        ↓
PostgreSQL
        ↓
n8n workflow
        ↓
lead scoring and enrichment
        ↓
CRM / Telegram / email outreach queue
```

## Integration Options

### 1. n8n Webhook

The parser can send each new company to an n8n webhook after it is saved in PostgreSQL.

Recommended payload:

```json
{
  "company_id": 101,
  "company_name": "Example Company",
  "city": "Moscow",
  "category": "Metalworking",
  "address": "Example address",
  "phone": null,
  "website": null,
  "source": "2gis",
  "status": "NEW"
}
```

### 2. PostgreSQL Polling

n8n can periodically query companies with status `NEW`, process them, and then change the status to `ENRICHING`, `VERIFIED`, or `CONTACTED`.

### 3. CSV Handoff

The current CSV export remains useful for manual review and import into third-party CRM systems.

## Suggested Lead Statuses

```text
NEW
ENRICHING
CONTACT_FOUND
VERIFIED
CONTACTED
INTERESTED
NOT_RELEVANT
```

## Recommended Database Extension

Add these fields to the company workflow layer:

- `lead_status`
- `score`
- `last_processed_at`
- `assigned_to`
- `next_action_at`
- `notes`

## Security Rules

- Store webhook URLs locally in `.env`.
- Never commit API keys or production credentials.
- Use demo placeholders in screenshots and documentation.
- Do not upload real lead exports to the repository.

## Next Implementation Step

The first practical integration should be:

1. add `lead_status` to PostgreSQL;
2. create a query that selects only `NEW` leads;
3. send those leads to an n8n webhook;
4. update the status after successful delivery;
5. log failed attempts for retry.
