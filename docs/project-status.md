# Project Status

_Last updated: 2026-06-22_

## Current State

The MVP is functional and portfolio-ready.

Implemented:

- company collection by city and category;
- safe demo mode and live 2GIS API mode;
- PostgreSQL persistence;
- parser job history;
- duplicate detection;
- enrichment source queue;
- manually verified contacts;
- CSV export;
- terminal reports;
- setup, security, architecture, and demo documentation.

## What Is Working

The current pipeline is:

```text
city + category
      ↓
2GIS API / demo dataset
      ↓
normalization and duplicate checks
      ↓
PostgreSQL
      ↓
enrichment queue
      ↓
manual contact verification
      ↓
CSV export
```

## Current Limitation

Phone, website, and email fields may be unavailable when the connected 2GIS API plan does not include contact data.

The project handles this by preparing enrichment links and supporting manual verification instead of attempting aggressive scraping or bypass techniques.

## Next Practical Milestone

The next useful release should focus on improving the existing project instead of creating a separate duplicate CRM backend.

Priority:

1. add lead status management;
2. add notes for each company;
3. improve CSV import/export flow;
4. add a lightweight dashboard;
5. prepare integration with n8n and external CRM systems;
6. add automated tests for duplicate handling and database writes.

## Portfolio Positioning

This project demonstrates:

- Python application structure;
- PostgreSQL schema design;
- API integration;
- data normalization;
- duplicate prevention;
- enrichment workflow design;
- secure configuration practices;
- business-oriented documentation.
