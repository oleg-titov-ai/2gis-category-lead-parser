-- 2GIS Category Lead Parser
-- PostgreSQL schema

CREATE TABLE IF NOT EXISTS parser_jobs (
    id BIGSERIAL PRIMARY KEY,
    city TEXT NOT NULL,
    category TEXT NOT NULL,
    limit_requested INTEGER NOT NULL DEFAULT 10,
    status TEXT NOT NULL DEFAULT 'created',
    found_count INTEGER NOT NULL DEFAULT 0,
    new_count INTEGER NOT NULL DEFAULT 0,
    duplicate_count INTEGER NOT NULL DEFAULT 0,
    enriched_count INTEGER NOT NULL DEFAULT 0,
    error_message TEXT,
    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    finished_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS companies (
    id BIGSERIAL PRIMARY KEY,
    source TEXT NOT NULL DEFAULT '2gis',
    source_company_id TEXT,
    name TEXT NOT NULL,
    category TEXT,
    city TEXT,
    address TEXT,
    phone TEXT,
    website TEXT,
    rating NUMERIC(3,2),
    reviews_count INTEGER,
    working_hours TEXT,
    latitude NUMERIC(10,7),
    longitude NUMERIC(10,7),
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (source, source_company_id)
);

CREATE TABLE IF NOT EXISTS company_contacts (
    id BIGSERIAL PRIMARY KEY,
    company_id BIGINT NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    contact_type TEXT NOT NULL,
    value TEXT NOT NULL,
    source_url TEXT,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (company_id, contact_type, value)
);

CREATE TABLE IF NOT EXISTS enrichment_sources (
    id BIGSERIAL PRIMARY KEY,
    company_id BIGINT NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    source_type TEXT NOT NULL,
    source_url TEXT,
    raw_text TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS job_companies (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT NOT NULL REFERENCES parser_jobs(id) ON DELETE CASCADE,
    company_id BIGINT NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    is_new BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (job_id, company_id)
);

CREATE INDEX IF NOT EXISTS idx_companies_city_category ON companies(city, category);
CREATE INDEX IF NOT EXISTS idx_companies_name ON companies(name);
CREATE INDEX IF NOT EXISTS idx_contacts_company ON company_contacts(company_id);
CREATE INDEX IF NOT EXISTS idx_parser_jobs_started ON parser_jobs(started_at DESC);
