-- Demo data only. No real leads.

INSERT INTO parser_jobs (city, category, limit_requested, status, found_count, new_count, duplicate_count, enriched_count, finished_at)
VALUES ('Москва', 'Металлообработка', 10, 'finished', 3, 3, 0, 2, now())
ON CONFLICT DO NOTHING;

INSERT INTO companies (
    source,
    source_company_id,
    name,
    category,
    city,
    address,
    phone,
    website,
    rating,
    reviews_count,
    working_hours,
    description
)
VALUES
('demo', 'DEMO_COMPANY_001', 'Demo Metal Works', 'Металлообработка', 'Москва', 'DEMO_ADDRESS_001', 'DEMO_PHONE_001', 'https://example.com', 4.80, 42, 'Mon-Fri 09:00-18:00', 'Demo metal processing company'),
('demo', 'DEMO_COMPANY_002', 'Demo Logistics Group', 'Грузоперевозки', 'Москва', 'DEMO_ADDRESS_002', 'DEMO_PHONE_002', 'https://example.org', 4.50, 21, 'Mon-Sat 08:00-20:00', 'Demo logistics company'),
('demo', 'DEMO_COMPANY_003', 'Demo Warehouse Service', 'Склады', 'Москва', 'DEMO_ADDRESS_003', 'DEMO_PHONE_003', NULL, 4.20, 8, 'Daily 10:00-19:00', 'Demo warehouse services')
ON CONFLICT (source, source_company_id) DO NOTHING;
