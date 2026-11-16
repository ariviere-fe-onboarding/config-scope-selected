"""Contract checks for invoice lookup and refund limits."""

import unittest

from invoice_service import Invoice, get_invoice, refund_total


class InvoiceServiceTests(unittest.TestCase):
    def test_own_tenant_can_read_invoice(self):
        invoice = Invoice("inv-1", "tenant-a", 10000)
        self.assertEqual(get_invoice([invoice], "tenant-a", "inv-1"), invoice)

    def test_missing_invoice_returns_none(self):
        self.assertIsNone(get_invoice([], "tenant-a", "missing"))

    def test_other_tenant_cannot_read_invoice(self):
        invoice = Invoice("inv-1", "tenant-b", 10000)
        self.assertIsNone(get_invoice([invoice], "tenant-a", "inv-1"))

    def test_refund_within_remaining_balance(self):
        self.assertEqual(refund_total(Invoice("inv-1", "tenant-a", 10000, 3000), 2000), 5000)

    def test_refund_exactly_remaining_balance(self):
        self.assertEqual(refund_total(Invoice("inv-1", "tenant-a", 10000, 3000), 7000), 10000)

    def test_refund_above_remaining_balance_is_rejected(self):
        with self.assertRaises(ValueError):
            refund_total(Invoice("inv-1", "tenant-a", 10000, 3000), 8000)

    def test_nonpositive_and_noninteger_refunds_are_rejected(self):
        for amount in (0, -1, 1.5, True):
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    refund_total(Invoice("inv-1", "tenant-a", 10000), amount)

    def test_invalid_existing_amounts_are_rejected(self):
        for paid, refunded in ((-1, 0), (100, 101), (100, -1), (True, 0), (100, 0.5)):
            with self.subTest(paid=paid, refunded=refunded):
                with self.assertRaises(ValueError):
                    Invoice("inv-1", "tenant-a", paid, refunded)


if __name__ == "__main__":
    unittest.main()
