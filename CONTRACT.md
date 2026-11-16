# Invoice helper contract

This module provides repository-local invoice lookup and refund calculation.

- Invoice lookup must return an invoice only when both its ID and tenant match.
  A missing invoice or a different tenant must return `None`.
- All amounts are integer cents. Paid and previously refunded values are non-negative.
  The refunded amount must never exceed the paid amount.
- Refund requests must be positive integer cents and cannot exceed the remaining
  paid balance. The helper returns the new cumulative refunded total without
  mutating the immutable invoice.
- Callers authenticate the user and supply the authenticated tenant ID.
- Run the contract checks with `python3 -m unittest -v`.
