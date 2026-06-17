"""CSV export utilities."""

from __future__ import annotations

import csv
from pathlib import Path

from enrich import EnrichmentResult
from parser_2gis import CompanyLead


def export_companies_to_csv(
    companies: list[CompanyLead],
    enrichment: list[EnrichmentResult],
    export_path: str,
) -> str:
    path = Path(export_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    enrichment_by_name = {item.company_name: item for item in enrichment}

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "name",
                "category",
                "city",
                "address",
                "phone",
                "website",
                "email",
                "rating",
                "reviews_count",
                "working_hours",
                "description",
            ],
        )
        writer.writeheader()

        for company in companies:
            enriched = enrichment_by_name.get(company.name)
            writer.writerow(
                {
                    "name": company.name,
                    "category": company.category,
                    "city": company.city,
                    "address": company.address,
                    "phone": company.phone,
                    "website": company.website,
                    "email": enriched.email if enriched else None,
                    "rating": company.rating,
                    "reviews_count": company.reviews_count,
                    "working_hours": company.working_hours,
                    "description": company.description,
                }
            )

    return str(path)
