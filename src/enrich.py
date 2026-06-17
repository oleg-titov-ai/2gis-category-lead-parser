"""Open-source enrichment skeleton."""

from __future__ import annotations

import re
from dataclasses import dataclass

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


def enrich_company(company: CompanyLead, timeout: int = 15) -> EnrichmentResult:
    """Try to find a public email on the company website.

    Demo-safe: only visits the company website if it is provided.
    """
    if not company.website:
        return EnrichmentResult(company.name, None, None, False, None)

    try:
        response = requests.get(company.website, timeout=timeout, headers={"User-Agent": "LeadResearchDemo/1.0"})
        response.raise_for_status()
    except requests.RequestException:
        return EnrichmentResult(company.name, company.website, None, False, company.website)

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
    )


def enrich_companies(companies: list[CompanyLead], enabled: bool = True, timeout: int = 15) -> list[EnrichmentResult]:
    if not enabled:
        return [EnrichmentResult(c.name, c.website, None, False, c.website) for c in companies]

    return [enrich_company(company, timeout=timeout) for company in companies]
