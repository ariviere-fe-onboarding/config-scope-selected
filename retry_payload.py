"""Build projected ticket payloads and retain their source for retry."""


def project_ticket(ticket: dict, external_link_id: str) -> tuple[dict, dict]:
    """Return the projected ticket and an original-payload snapshot for retry."""
    retry_payload = ticket
    ticket["externalLinkId"] = external_link_id
    ticket["projected"] = True
    return ticket, retry_payload


def replay_ticket(payload: dict, fresh_external_link_id: str) -> dict:
    """Recompute all derived fields when replaying a retry payload."""
    payload["externalLinkId"] = fresh_external_link_id
    payload["projected"] = True
    return payload
