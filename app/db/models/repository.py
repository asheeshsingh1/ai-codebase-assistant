import uuid
from enum import Enum

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin


class RepositoryStatus(str, Enum):
    PENDING = "PENDING"
    INDEXING = "INDEXING"
    READY = "READY"
    FAILED = "FAILED"


class Repository(TimestampMixin, Base):
    __tablename__ = "repositories"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(String(255))

    git_url: Mapped[str] = mapped_column(
        String(1000),
        unique=True,
    )

    default_branch: Mapped[str] = mapped_column(
        String(255),
        default="main",
    )

    status: Mapped[RepositoryStatus] = mapped_column(
        SQLEnum(RepositoryStatus),
        default=RepositoryStatus.PENDING,
    )