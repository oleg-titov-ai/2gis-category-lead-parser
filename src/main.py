"""CLI entry point for 2GIS Category Lead Parser MVP."""

from __future__ import annotations

import argparse

from categories import list_categories, validate_category
from config import load_config
from db import create_parser_job, finish_parser_job, save_companies_for_job
from enrich import enrich_companies
from exporter import export_companies_to_csv
from parser_2gis import collect_2gis_leads, collect_demo_leads
from report import build_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Collect and enrich demo B2B leads by city and category.")
    parser.add_argument("--city", default=None, help="City name, for example: Москва")
    parser.add_argument("--category", default=None, help="Category name")
    parser.add_argument("--limit", type=int, default=None, help="Company limit, default 10")
    parser.add_argument("--demo", action="store_true", help="Use demo data instead of live collector")
    parser.add_argument("--save-db", action="store_true", help="Save parsed companies to PostgreSQL")
    parser.add_argument("--list-categories", action="store_true", help="Print allowed categories and exit")
    return parser


def main() -> None:
    config = load_config()
    parser = build_parser()
    args = parser.parse_args()

    if args.list_categories:
        print("Available categories:")
        for category in list_categories():
            print(f"- {category}")
        return

    city = args.city or config.default_city
    category = validate_category(args.category or "Металлообработка")
    limit = args.limit or config.default_limit

    if limit > 10:
        raise ValueError("MVP limit is 10 companies per run.")

    if args.demo or config.dgis_api_key == "DEMO_DGIS_API_KEY":
        companies = collect_demo_leads(city=city, category=category, limit=limit)
    else:
        companies = collect_2gis_leads(city=city, category=category, limit=limit, api_key=config.dgis_api_key)

    enrichment = enrich_companies(
        companies,
        enabled=config.enrichment_enabled,
        timeout=config.request_timeout_seconds,
    )

    db_new_count = len(companies)
    db_duplicate_count = 0
    db_job_id = None

    if args.save_db:
        db_job_id = create_parser_job(config=config, city=city, category=category, limit_requested=limit)
        save_result = save_companies_for_job(config=config, job_id=db_job_id, companies=companies)
        db_new_count = save_result.new_count
        db_duplicate_count = save_result.duplicate_count
        finish_parser_job(
            config=config,
            job_id=db_job_id,
            found_count=len(companies),
            new_count=db_new_count,
            duplicate_count=db_duplicate_count,
            enriched_count=sum(1 for item in enrichment if item.enriched),
        )

    export_path = None
    if config.export_csv:
        export_path = export_companies_to_csv(companies, enrichment, config.export_path)

    report = build_report(
        city=city,
        category=category,
        limit_requested=limit,
        companies=companies,
        enrichment=enrichment,
        export_path=export_path,
    )

    print(report.to_text())

    if args.save_db:
        print("")
        print("Database save:")
        print(f"Job ID: {db_job_id}")
        print(f"DB new: {db_new_count}")
        print(f"DB duplicates: {db_duplicate_count}")


if __name__ == "__main__":
    main()
