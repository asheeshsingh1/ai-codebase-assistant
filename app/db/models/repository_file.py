from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.db.models.repository import Repository
    from app.db.models.file_chunk import FileChunk


class RepositoryFile(TimestampMixin, Base):
    __tablename__ = "repository_files"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    repository_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(
            "repositories.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    relative_path: Mapped[str] = mapped_column(
        String(1024),
        nullable=False,
    )

    extension: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    language: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )

    size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    checksum: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    repository: Mapped["Repository"] = relationship(
        "Repository",
        back_populates="files",
    )

    chunks: Mapped[list["FileChunk"]] = relationship(
        "FileChunk",
        back_populates="repository_file",
        cascade="all, delete-orphan",
    )
