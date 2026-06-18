"""Open-source enrichment helpers.

This module does not bypass websites, captchas, sessions, or paywalls.
For companies without a website, it prepares public search URLs that can be
reviewed manually or passed to a permitted search API later.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

from parser_2gis import CompanyLead

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


@dataclass
class EnrichmentResult:
    company_name: str
    website: str | None
    email: str | None
    enriched: bool
    source_url: str | None
    search_query: str | None = None
    google_search_url: str | None = None
    yandex_search_url: str | None = None
    two_gis_url: str | None = None


def build_search_query(company: CompanyLead) -> str:
    parts = [company.name, company.city]
    if company.address:
        parts.append(company.address)
    parts.append("официальный сайт телефон")
    return " ".join(part for part in parts if part)


def build_google_search_url(query: str) -> str:
    return f"https://www.google.com/search?q={quote_plus(query)}"


def build_yandex_search_url(query: str) -> str:
    return f"https://yandex.ru/search/?text={quote_plus(query)}"


def build_2gis_url(company: CompanyLead) -> str | None:
    if company.source != "2gis" or not company.source_company_id:
        return None
    return f"https://2gis.ru/search/{quote_plus(company.name)}/firm/{company.source_company_id}"


def enrich_company(company: CompanyLead, timeout: int = 15) -> EnrichmentResult:
    """Enrich one company.

    If website exists, try to extract a public email from that website.
    If website is missing, prepare search URLs for manual/API-based enrichment.
    """
    search_query = build_search_query(company)
    google_url = build_google_search_url(search_query)
    yandex_url = build_yandex_search_url(search_query)
    two_gis_url = build_2gis_url(company)

    if not company.website:
        return EnrichmentResult(
            company_name=company.name,
            website=None,
            email=None,
            enriched=False,
            source_url=None,
            search_query=search_query,
            google_search_url=google_url,
            yandex_search_url=yandex_url,
            two_gis_url=two_gis_url,
        )

    try:
        response = requests.get(company.website, timeout=timeout, headers={"User-Agent": "LeadResearchDemo/1.0"})
        response.raise_for_status()
    except requests.RequestException:
        return EnrichmentResult(
            company_name=company.name,
            website=company.website,
            email=None,
            enriched=False,
            source_url=company.website,
            search_query=search_query,
            google_search_url=google_url,
            yandex_search_url=yandex_url,
            two_gis_url=two_gis_url,
        )

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True)
    emails = EMAIL_RE.findall(text)
    email = emails[0] if emails else None

    return EnrichmentResult(
        company_name=company.name,
        website=company.website,
        email=email,
        enriched=bool(email),
        source_url=company.website,
        search_query=search_query,
        google_search_url=google_url,
        yandex_search_url=yandex_url,
        two_gis_url=two_gis_url,
    )


def enrich_companies(companies: list[CompanyLead], enabled: bool = True, timeout: int = 15) -> list[EnrichmentResult]:
    if not enabled:
        return [
            EnrichmentResult(
                company_name=c.name,
                website=c.website,
                email=None,
                enriched=False,
                source_url=c.website,
                search_query=build_search_query(c),
                google_search_url=build_google_search_url(build_search_query(c)),
                yandex_search_url=build_yandex_search_url(build_search_query(c)),
                two_gis_url=build_2gis_url(c),
            )
            for c in companies
        ]

    return [enrich_company(company, timeout=timeout) for company in companies]
