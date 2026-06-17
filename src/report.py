"""Report generation."""

from __future__ import annotations

from dataclasses import dataclass

from enrich import EnrichmentResult
from parser_2gis import CompanyLead


@dataclass
class ParseReport:
    city: str
    category: str
    limit_requested: int
    found: int
    new_count: int
    duplicate_count: int
    with_phone: int
    with_website: int
    with_email: int
    enriched: int
    export_path: str | None

    def to_text(self) -> str:
        return "\n".join(
            [
                "Parsing finished",
                f"City: {self.city}",
                f"Category: {self.category}",
                f"Requested limit: {self.limit_requested}",
                "",
                f"Found: {self.found}",
                f"New: {self.new_count}",
                f"Duplicates: {self.duplicate_count}",
                f"With phone: {self.with_phone}",
                f"With website: {self.with_website}",
                f"With email: {self.with_email}",
                f"Enriched: {self.enriched}",
                f"CSV exported: {self.export_path or 'disabled'}",
            ]
        )


def build_report(
    city: str,
    category: str,
    limit_requested: int,
    companies: list[CompanyLead],
    enrichment: list[EnrichmentResult],
    export_path: str | None,
) -> ParseReport:
    with_phone = sum(1 for c in companies if c.phone)
    with_website = sum(1 for c in companies if c.website)
    with_email = sum(1 for e in enrichment if e.email)
    enriched = sum(1 for e in enrichment if e.enriched)

    return ParseReport(
        city=city,
        category=category,
        limit_requested=limit_requested,
        found=len(companies),
        new_count=len(companies),
        duplicate_count=0,
        with_phone=with_phone,
        with_website=with_website,
        with_email=with_email,
        enriched=enriched,
        export_path=export_path,
    )
