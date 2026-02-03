import requests

from app.models import Record
from config import db
from utils import CLOUDFLARE_API_TOKEN, CLOUDFLARE_BASE_URL
from utils.check_if_subdomain_available import check_if_subdomain_available

ALLOWED_TYPES: list[str] = ["A", "AAAA", "CNAME", "MX"]


def create_record(
    id, type: str, name: str, content: str, ttl: int = 3600
) -> str | None:
    """Sends an post request to set an dns record and adds record to the db"""

    # check if the sub-domain is taken

    is_taken = check_if_subdomain_available(name=name)

    if is_taken:
        return f"{name} is already taken!"

    if type not in ALLOWED_TYPES:
        return f"Error! Can't set record: {type}"

    if int(ttl) > 86400 or int(ttl) < 60:
        return "TTL must be between 60 to 86400"

    data = {
        "type": type,
        "name": name,
        "content": content,
        "ttl": int(ttl),
        "proxied": True,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
    }

    res = requests.post(CLOUDFLARE_BASE_URL, json=data, headers=headers)

    if res.status_code != 200:
        return "Error setting record!"

    data = res.json()
    dns_id = data["result"]["id"]

    # save the id to the related user and return sucess message
    record = Record(
        name=name,
        record_type=type,
        points_to=content,
        dns_record_id=dns_id,
        user_id=id,
    )

    db.session.add(record)
    db.session.commit()
    db.session.refresh(record)

    return None
