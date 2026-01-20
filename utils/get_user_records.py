from sqlalchemy import select

from app.models import Record
from config import db


def get_user_records(user_id):
    """Returns the all dns record created by the user"""

    record_data = (
        db.session.execute(select(Record).where(Record.user_id == user_id))
        .scalars()
        .all()
    )

    return record_data
