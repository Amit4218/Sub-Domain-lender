import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from config import db


class User(db.Model):  # ty:ignore[unsupported-base]
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),  # ty:ignore[no-matching-overload]
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        unique=True,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    password: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now,
        nullable=False,
    )

    records: Mapped[list["Record"]] = relationship(
        "Record",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def hash_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)


class Record(db.Model):  # ty:ignore[unsupported-base]
    __tablename__ = "records"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),  # ty:ignore[no-matching-overload]
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        unique=True,
        index=True,
    )

    record_type: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    points_to: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),  # ty:ignore[no-matching-overload]
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="records",
    )
