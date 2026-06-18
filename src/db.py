"""Database helpers.

The MVP can run without PostgreSQL. Use --save-db to write demo leads
to a local or remote PostgreSQL database configured in .env.
"""

from __future__ import annotations

from dataclasses import dataclass

import psycopg

from config import AppConfig, build_database_url
from parser_2gis import CompanyLead


@dataclass(frozen=True)
class DbSaveResult:
    job_id: int
    processed_count: int
    new_count: int
    duplicate_count: int


def get_connection(config: AppConfig):
    return psycopg.connect(build_database_url(config))


def create_parser_job(config: AppConfig, city: str, category: str, limit_requested: int) -> int:
    query = """
        INSERT INTO parser_jobs (city, category, limit_requested, status)
        VALUES (%s, %s, %s, 'running')
        RETURNING id;
    """

    with get_connection(config) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (city, category, limit_requested))
            job_id = cur.fetchone()[0]
        conn.commit()

    return int(job_id)


def finish_parser_job(
    config: AppConfig,
    job_id: int,
    found_count: int,
    new_count: int,
    duplicate_count: int,
    enriched_count: int,
    status: str = "finished",
    error_message: str | None = None,
) -> None:
    query = """
        UPDATE parser_jobs
        SET
            status = %s,
            found_count = %s,
            new_count = %s,
            duplicate_count = %s,
            enriched_count = %s,
            error_message = %s,
            finished_at = now()
        WHERE id = %s;
    """

    with get_connection(config) as conn:
        with conn.cursor() as cur:
            cur.execute(
                query,
                (status, found_count, new_count, duplicate_count, enriched_count, error_message, job_id),
            )
        conn.commit()


def save_companies_for_job(config: AppConfig, job_id: int, companies: list[CompanyLead]) -> DbSaveResult:
    """Insert or update companies and link them to a parser job."""
    upsert_company_query = """
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
            updated_at = now()
        RETURNING id, (xmax = 0) AS inserted;
    """

    link_job_query = """
        INSERT INTO job_companies (job_id, company_id, is_new)
        VALUES (%s, %s, %s)
        ON CONFLICT (job_id, company_id) DO NOTHING;
    """

    new_count = 0
    duplicate_count = 0

    with get_connection(config) as conn:
        with conn.cursor() as cur:
            for company in companies:
                cur.execute(upsert_company_query, company.to_dict())
                company_id, inserted = cur.fetchone()

                is_new = bool(inserted)
                if is_new:
                    new_count += 1
                else:
                    duplicate_count += 1

                cur.execute(link_job_query, (job_id, company_id, is_new))
        conn.commit()

    return DbSaveResult(
        job_id=job_id,
        processed_count=len(companies),
        new_count=new_count,
        duplicate_count=duplicate_count,
    )


def save_companies(config: AppConfig, companies: list[CompanyLead]) -> int:
    """Backward-compatible helper: insert companies without job tracking."""
    job_id = create_parser_job(
        config=config,
        city=companies[0].city if companies else "unknown",
        category=companies[0].category if companies else "unknown",
        limit_requested=len(companies),
    )
    result = save_companies_for_job(config=config, job_id=job_id, companies=companies)
    finish_parser_job(
        config=config,
        job_id=job_id,
        found_count=result.processed_count,
        new_count=result.new_count,
        duplicate_count=result.duplicate_count,
        enriched_count=0,
    )
    return result.processed_count
