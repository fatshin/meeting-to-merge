import unittest

import product
from runtime.server import page, result_markup


class ProductTests(unittest.TestCase):
    def test_fixed_acceptance(self):
        result = product.analyze({field.name: field.value for field in product.PRODUCT.fields})
        passed, checks = product.acceptance(result)
        self.assertTrue(passed, checks)

    def test_page_is_product_specific_and_escapes_output(self):
        self.assertIn(product.PRODUCT.name, page())
        self.assertNotIn("<script>", result_markup({"status": "<script>", "headline": "safe", "metrics": {}, "items": [], "evidence": [], "artifact": {}}))

    def test_browser_crlf_submission_still_builds_patch(self):
        payload = {field.name: field.value.replace("\n", "\r\n") for field in product.PRODUCT.fields}
        result = product.analyze(payload)
        self.assertEqual(result["status"], "READY_FOR_HUMAN_APPLY")
        self.assertIn("idempotency_key", result["artifact"]["patch"])


if __name__ == "__main__":
    unittest.main()
