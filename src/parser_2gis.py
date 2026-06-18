"""2GIS collector.

Public repository version uses demo data by default.
Live mode uses a 2GIS API key from a local .env file.
Do not commit real API keys to GitHub.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, asdict
from typing import Any

import requests

CATALOG_ITEMS_URL = "https://catalog.api.2gis.com/3.0/items"
CATALOG_ITEM_BY_ID_URL = "https://catalog.api.2gis.com/3.0/items/byid"
DEFAULT_FIELDS = ",".join(
    [
        "items.point",
        "items.address_name",
        "items.contact_groups",
        "items.schedule",
        "items.reviews",
        "items.rubrics",
    ]
)
DETAIL_FIELDS = ",".join(
    [
        "items.point",
        "items.address_name",
        "items.contact_groups",
        "items.schedule",
        "items.reviews",
        "items.rubrics",
        "items.description",
    ]
)

# City center coordinates for small portfolio/demo runs.
# 2GIS API search is location-oriented, so we need a center point.
CITY_CENTERS = {
    "москва": "37.6173,55.7558",
    "санкт-петербург": "30.3159,59.9391",
    "спб": "30.3159,59.9391",
    "ростов-на-дону": "39.7203,47.2221",
    "краснодар": "38.9747,45.0355",
    "екатеринбург": "60.6057,56.8389",
    "новосибирск": "82.9204,55.0302",
    "казань": "49.1064,55.7961",
}


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


def _safe_sleep(seconds: float) -> None:
    if seconds > 0:
        time.sleep(seconds)


def _first_contact_value(item: dict[str, Any], contact_type: str) -> str | None:
    for group in item.get("contact_groups", []) or []:
        for contact in group.get("contacts", []) or []:
            if contact.get("type") == contact_type:
                value = contact.get("value") or contact.get("text")
                if value:
                    return str(value)
                values = contact.get("values")
                if isinstance(values, list) and values:
                    first = values[0]
                    if isinstance(first, dict):
                        nested_value = first.get("value") or first.get("text")
                        if nested_value:
                            return str(nested_value)
                    return str(first)
    return None


def _rating(item: dict[str, Any]) -> float | None:
    reviews = item.get("reviews") or {}
    value = reviews.get("general_rating") or reviews.get("rating")
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _reviews_count(item: dict[str, Any]) -> int | None:
    reviews = item.get("reviews") or {}
    value = reviews.get("general_review_count") or reviews.get("review_count")
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _working_hours(item: dict[str, Any]) -> str | None:
    schedule = item.get("schedule")
    if not schedule:
        return None
    if isinstance(schedule, dict):
        if schedule.get("text"):
            return str(schedule["text"])
        return str(schedule)
    return str(schedule)


def _point(item: dict[str, Any]) -> tuple[float | None, float | None]:
    point = item.get("point") or {}
    try:
        lon = float(point["lon"]) if point.get("lon") is not None else None
        lat = float(point["lat"]) if point.get("lat") is not None else None
        return lat, lon
    except (TypeError, ValueError):
        return None, None


def _city_location(city: str) -> str:
    key = city.strip().lower()
    if key not in CITY_CENTERS:
        raise ValueError(
            f"No default coordinates for city '{city}'. "
            "Add it to CITY_CENTERS in src/parser_2gis.py or use a supported city."
        )
    return CITY_CENTERS[key]


def _to_company(item: dict[str, Any], city: str, category: str) -> CompanyLead:
    latitude, longitude = _point(item)
    return CompanyLead(
        source="2gis",
        source_company_id=str(item.get("id") or item.get("hash") or item.get("name")),
        name=str(item.get("name") or "Unknown company"),
        category=category,
        city=city,
        address=item.get("address_name") or item.get("full_name"),
        phone=_first_contact_value(item, "phone"),
        website=_first_contact_value(item, "website"),
        rating=_rating(item),
        reviews_count=_reviews_count(item),
        working_hours=_working_hours(item),
        latitude=latitude,
        longitude=longitude,
        description=item.get("description") or item.get("purpose_name") or item.get("type"),
    )


def _merge_company(base: CompanyLead, detail: CompanyLead) -> CompanyLead:
    return CompanyLead(
        source=base.source,
        source_company_id=base.source_company_id,
        name=detail.name or base.name,
        category=base.category,
        city=base.city,
        address=detail.address or base.address,
        phone=detail.phone or base.phone,
        website=detail.website or base.website,
        rating=detail.rating if detail.rating is not None else base.rating,
        reviews_count=detail.reviews_count if detail.reviews_count is not None else base.reviews_count,
        working_hours=detail.working_hours or base.working_hours,
        latitude=detail.latitude if detail.latitude is not None else base.latitude,
        longitude=detail.longitude if detail.longitude is not None else base.longitude,
        description=detail.description or base.description,
    )


def _fetch_company_details(company: CompanyLead, api_key: str) -> CompanyLead:
    params = {
        "id": company.source_company_id,
        "fields": DETAIL_FIELDS,
        "key": api_key,
    }
    response = requests.get(CATALOG_ITEM_BY_ID_URL, params=params, timeout=20)
    response.raise_for_status()
    payload = response.json()
    items = payload.get("result", {}).get("items", [])
    if not items:
        return company
    detail = _to_company(item=items[0], city=company.city, category=company.category)
    return _merge_company(base=company, detail=detail)


def collect_2gis_leads(
    city: str,
    category: str,
    limit: int = 10,
    api_key: str | None = None,
    request_delay_seconds: float = 1.0,
) -> list[CompanyLead]:
    """Collect companies from 2GIS Catalog API using a local API key.

    This function uses normal API requests only. It does not scrape pages,
    bypass anti-bot systems, use cookies, or solve captchas.
    """
    if not api_key or api_key == "DEMO_DGIS_API_KEY":
        return collect_demo_leads(city=city, category=category, limit=limit)

    if limit > 30:
        raise ValueError("Live MVP limit is 30 companies per run.")

    location = _city_location(city)
    page_size = min(limit, 10)
    companies: list[CompanyLead] = []
    seen_ids: set[str] = set()
    page = 1

    while len(companies) < limit:
        params = {
            "q": category,
            "location": location,
            "radius": 50000,
            "page": page,
            "page_size": page_size,
            "fields": DEFAULT_FIELDS,
            "key": api_key,
        }

        response = requests.get(CATALOG_ITEMS_URL, params=params, timeout=20)
        response.raise_for_status()
        payload = response.json()

        items = payload.get("result", {}).get("items", [])
        if not items:
            break

        for item in items:
            company = _to_company(item=item, city=city, category=category)
            if company.source_company_id in seen_ids:
                continue
            seen_ids.add(company.source_company_id)
            companies.append(company)
            if len(companies) >= limit:
                break

        page += 1
        _safe_sleep(request_delay_seconds)

    detailed_companies: list[CompanyLead] = []
    for company in companies:
        try:
            detailed_companies.append(_fetch_company_details(company=company, api_key=api_key))
        except requests.HTTPError as exc:
            print(f"Warning: details request failed for {company.source_company_id}: {exc}")
            detailed_companies.append(company)
        _safe_sleep(request_delay_seconds)

    return detailed_companies
