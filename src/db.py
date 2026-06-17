"""Database helpers placeholder.

The MVP demo can run without PostgreSQL. Use these helpers when connecting
real local storage.
"""

from __future__ import annotations

import psycopg

from config import AppConfig, build_database_url
from parser_2gis import CompanyLead


def get_connection(config: AppConfig):
    return psycopg.connect(build_database_url(config))


def save_companies(config: AppConfig, companies: list[CompanyLead]) -> int:
    """Insert companies into PostgreSQL.

    Returns number of processed companies.
    """
    query = """
        INSERT INTO companies (
            source, source_company_id, name, category, city, address, phone,
            website, rating, reviews_count, working_hours, latitude, longitude, description
        )
        VALUES (
            %(source)s, %(source_company_id)s, %(name)s, %(category)s, %(city)s,
            %(address)s, %(phone)s, %(website)s, %(rating)s, %(reviews_count)s,
            %(working_hours)s, %(latitude)s, %(longitude)s, %(description)s
        )
        ON CONFLICT (source, source_company_id) DO UPDATE
        SET
            name = EXCLUDED.name,
            category = EXCLUDED.category,
            city = EXCLUDED.city,
            address = EXCLUDED.address,
            phone = EXCLUDED.phone,
            website = EXCLUDED.website,
            rating = EXCLUDED.rating,
            reviews_count = EXCLUDED.reviews_count,
            working_hours = EXCLUDED.working_hours,
            description = EXCLUDED.description,
            updated_at = now();
    """

    with get_connection(config) as conn:
        with conn.cursor() as cur:
            for company in companies:
                cur.execute(query, company.to_dict())
        conn.commit()

    return len(companies)
