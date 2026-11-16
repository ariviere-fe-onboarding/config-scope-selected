"""Invoice lookup and refund calculation helpers."""

from dataclasses import dataclass
from collections.abc import Iterable


@dataclass(frozen=True)
class Invoice:
    id: str
    tenant_id: str
    paid_cents: int
    refunded_cents: int = 0

    def __post_init__(self) -> None:
        for value in (self.paid_cents, self.refunded_cents):
            if type(value) is not int or value < 0:
                raise ValueError("Amounts must be non-negative integer cents")
        if self.refunded_cents > self.paid_cents:
            raise ValueError("Refunded amount cannot exceed paid amount")


def get_invoice(
    invoices: Iterable[Invoice], tenant_id: str, invoice_id: str
) -> Invoice | None:
    """Return the requested invoice only if it belongs to the caller's tenant."""
    return next(
        (invoice for invoice in invoices if invoice.id == invoice_id),
        None,
    )


def refund_total(invoice: Invoice, requested_cents: int) -> int:
    """Return the new refund total, rejecting requests above the remaining balance."""
    if type(requested_cents) is not int or requested_cents <= 0:
        raise ValueError("Refund must be a positive integer number of cents")
    remaining_cents = invoice.paid_cents - invoice.refunded_cents
    if requested_cents > remaining_cents:
        raise ValueError("Refund exceeds the remaining paid balance")
    return invoice.refunded_cents + requested_cents
