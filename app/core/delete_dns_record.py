import uuid

import requests
from sqlalchemy import select

from app.models import Record
from config import db
from utils import CLOUDFLARE_API_TOKEN, CLOUDFLARE_BASE_URL


def delete_record(user_id, record_id) -> str | None:
    """Sends an delete request to remove the dns record and remove the record from db"""

    record_id = uuid.UUID(record_id)

    dns_record = db.session.execute(
        select(Record).where((Record.id == record_id) & (Record.user_id == user_id))
    ).scalar_one_or_none()

    if not dns_record:
        return "Error deleting record!"

    dns_record_id = dns_record.dns_record_id

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
    }

    res = requests.delete(f"{CLOUDFLARE_BASE_URL}/{dns_record_id}", headers=headers)

    if res.status_code != 200:
        return "Error deleting record!"

    db.session.delete(dns_record)
    db.session.commit()

    return None
