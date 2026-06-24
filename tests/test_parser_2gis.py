"""Unit tests for the 2GIS parser helpers.

These tests do not call the real 2GIS API and do not require PostgreSQL.
"""

from __future__ import annotations

from pathlib import Path
import sys
import unittest
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import parser_2gis
from parser_2gis import CompanyLead, collect_2gis_leads, collect_demo_leads


class FakeResponse:
    def __init__(self, payload: dict):
        self._payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return self._payload


class Parser2GisTests(unittest.TestCase):
    def test_demo_mode_respects_limit(self) -> None:
        leads = collect_demo_leads(
            city="Москва",
            category="Металлообработка",
            limit=2,
        )

        self.assertEqual(2, len(leads))
        self.assertTrue(all(lead.city == "Москва" for lead in leads))
        self.assertTrue(all(lead.category == "Металлообработка" for lead in leads))

    def test_company_lead_to_dict_contains_expected_fields(self) -> None:
        lead = CompanyLead(
            source="demo",
            source_company_id="COMPANY_001",
            name="Example Company",
            category="Industrial Supply",
            city="Moscow",
        )

        payload = lead.to_dict()

        self.assertEqual("COMPANY_001", payload["source_company_id"])
        self.assertEqual("Example Company", payload["name"])
        self.assertIn("phone", payload)
        self.assertIsNone(payload["phone"])

    @patch("parser_2gis._fetch_company_details", side_effect=lambda company, api_key: company)
    @patch("parser_2gis.requests.get")
    def test_live_collection_removes_duplicate_company_ids(
        self,
        mock_get,
        _mock_details,
    ) -> None:
        mock_get.side_effect = [
            FakeResponse(
                {
                    "result": {
                        "items": [
                            {"id": "100", "name": "Company A"},
                            {"id": "100", "name": "Company A duplicate"},
                            {"id": "200", "name": "Company B"},
                        ]
                    }
                }
            )
        ]

        leads = collect_2gis_leads(
            city="Москва",
            category="Металлообработка",
            limit=2,
            api_key="TEST_API_KEY",
            request_delay_seconds=0,
        )

        self.assertEqual(2, len(leads))
        self.assertEqual(["100", "200"], [lead.source_company_id for lead in leads])
        self.assertEqual(["Company A", "Company B"], [lead.name for lead in leads])
        self.assertEqual(1, mock_get.call_count)

    def test_live_mode_rejects_limit_above_mvp_cap(self) -> None:
        with self.assertRaisesRegex(ValueError, "limit is 30"):
            collect_2gis_leads(
                city="Москва",
                category="Металлообработка",
                limit=31,
                api_key="TEST_API_KEY",
                request_delay_seconds=0,
            )


if __name__ == "__main__":
    unittest.main()
