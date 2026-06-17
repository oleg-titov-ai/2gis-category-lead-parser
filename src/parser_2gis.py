"""2GIS collector skeleton.

Public repository version uses demo data by default.
Connect an allowed data source or official API locally.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass
class CompanyLead:
    source: str
    source_company_id: str
    name: str
    category: str
    city: str
    address: str | None = None
    phone: str | None = None
    website: str | None = None
    rating: float | None = None
    reviews_count: int | None = None
    working_hours: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    description: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def collect_demo_leads(city: str, category: str, limit: int = 10) -> list[CompanyLead]:
    """Return safe fake leads for portfolio/demo mode."""
    demo = [
        CompanyLead(
            source="demo",
            source_company_id="DEMO_COMPANY_001",
            name="Demo Metal Works",
            category=category,
            city=city,
            address="DEMO_ADDRESS_001",
            phone="DEMO_PHONE_001",
            website="https://example.com",
            rating=4.8,
            reviews_count=42,
            working_hours="Mon-Fri 09:00-18:00",
            description="Demo metal processing company",
        ),
        CompanyLead(
            source="demo",
            source_company_id="DEMO_COMPANY_002",
            name="Demo Industrial Supply",
            category=category,
            city=city,
            address="DEMO_ADDRESS_002",
            phone="DEMO_PHONE_002",
            website="https://example.org",
            rating=4.5,
            reviews_count=21,
            working_hours="Mon-Sat 08:00-20:00",
            description="Demo B2B supplier",
        ),
        CompanyLead(
            source="demo",
            source_company_id="DEMO_COMPANY_003",
            name="Demo Warehouse Service",
            category=category,
            city=city,
            address="DEMO_ADDRESS_003",
            phone="DEMO_PHONE_003",
            website=None,
            rating=4.2,
            reviews_count=8,
            working_hours="Daily 10:00-19:00",
            description="Demo warehouse services",
        ),
    ]

    return demo[:limit]


def collect_2gis_leads(city: str, category: str, limit: int = 10, api_key: str | None = None) -> list[CompanyLead]:
    """Placeholder for a real allowed 2GIS/API integration.

    This public repo intentionally does not include scraping code that bypasses
    anti-bot systems. Implement locally using permitted data access.
    """
    if not api_key or api_key == "DEMO_DGIS_API_KEY":
        return collect_demo_leads(city=city, category=category, limit=limit)

    raise NotImplementedError(
        "Real 2GIS integration is intentionally not included in the public skeleton. "
        "Use an official or otherwise permitted data source locally."
    )
