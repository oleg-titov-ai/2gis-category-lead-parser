# Enrichment Strategy

The project separates lead collection from contact enrichment.

This is intentional: public company cards and verified contacts have different reliability levels.

## Current MVP Enrichment

The current repository version does not scrape search engine result pages.

Instead, it prepares an enrichment queue:

```text
company name + city + address
        ↓
search query
        ↓
Google search link
Yandex search link
2GIS company card link
        ↓
manual or API-based contact verification
        ↓
company_contacts
```

## Why This Design

The goal is to keep the public repository stable, clean, and portfolio-ready.

Search-engine HTML scraping is fragile because:

- result page markup changes;
- search engines may return JavaScript-only pages;
- anti-bot pages may appear;
- result quality differs by region and network;
- false positive contacts are common.

For a production system, enrichment should use permitted data sources.

## Contact Confidence Levels

### 1. API-provided contacts

Highest confidence if the data source contract allows these fields.

Example:

```text
2GIS API plan with contact field permissions
```

### 2. Company website contacts

Medium/high confidence when the source URL is the official company website.

### 3. Directory contacts

Medium/low confidence. These should be verified before outreach.

### 4. Search snippets or generic pages

Low confidence. Do not treat as verified contacts.

## Verification Model

Contacts are stored in `company_contacts` with:

```text
is_verified = true/false
```

Recommended approach:

```text
auto-discovered contact → is_verified=false
human-confirmed contact → is_verified=true
```

## Production Roadmap

Possible production enrichment providers:

- official search API;
- paid 2GIS contact access;
- company website crawler with rate limits;
- manual verification dashboard;
- email validation API;
- CRM integration.

## Local Experiments

Local scripts may be used for private experiments with public web pages, but they should not be part of the public portfolio repository unless they are stable, permitted, and documented.
