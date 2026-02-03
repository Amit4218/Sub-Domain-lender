from sqlalchemy import select

from app.models import Record
from config import db


def check_if_subdomain_available(name) -> bool:
    result = db.session.execute(
        select(Record).where(Record.name == name)
    ).scalar_one_or_none()

    if not result:
        return False

    return True
