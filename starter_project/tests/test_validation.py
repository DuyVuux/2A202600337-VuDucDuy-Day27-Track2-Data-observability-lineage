from __future__ import annotations

import unittest
import sys
from pathlib import Path

# Thêm thư mục gốc của starter_project vào sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.validation import is_positive_number, build_summary, VALID_STATUSES

class TestValidation(unittest.TestCase):

    def test_is_positive_number(self):
        self.assertTrue(is_positive_number("10.5"))
        self.assertTrue(is_positive_number("100"))
        self.assertFalse(is_positive_number("0"))
        self.assertFalse(is_positive_number("-1"))
        self.assertFalse(is_positive_number("abc"))
        self.assertFalse(is_positive_number(""))

    def test_build_summary_passed(self):
        rows = [
            {"customer_id": "C1", "amount": "100", "status": "completed"},
            {"customer_id": "C2", "amount": "50.5", "status": "pending"},
        ]
        summary = build_summary(rows)
        self.assertEqual(summary["row_count"], 2)
        self.assertEqual(summary["missing_customer_ids"], 0)
        self.assertEqual(summary["invalid_amounts"], 0)
        self.assertEqual(summary["invalid_statuses"], 0)
        self.assertEqual(summary["validation_status"], "passed")

    def test_build_summary_failed(self):
        rows = [
            {"customer_id": "", "amount": "100", "status": "completed"}, # missing id
            {"customer_id": "C2", "amount": "-10", "status": "pending"}, # invalid amount
            {"customer_id": "C3", "amount": "50", "status": "unknown"}, # invalid status
        ]
        summary = build_summary(rows)
        self.assertEqual(summary["row_count"], 3)
        self.assertEqual(summary["missing_customer_ids"], 1)
        self.assertEqual(summary["invalid_amounts"], 1)
        self.assertEqual(summary["invalid_statuses"], 1)
        self.assertEqual(summary["validation_status"], "failed")

    def test_valid_statuses_config(self):
        self.assertIn("completed", VALID_STATUSES)
        self.assertIn("pending", VALID_STATUSES)
        self.assertIn("cancelled", VALID_STATUSES)
        self.assertEqual(len(VALID_STATUSES), 3)

if __name__ == "__main__":
    unittest.main()
