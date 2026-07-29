from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.repository_file import RepositoryFile

class FileChunk(TimestampMixin, Base):
    __tablename__ = "file_chunks"

    __table_args__ = (
        UniqueConstraint(
            "repository_file_id",
            "chunk_index",
            name="uq_repository_file_chunk",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    repository_file_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "repository_files.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    start_line: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    end_line: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    token_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    content_hash: Mapped[str] = mapped_column(
        nullable=False,
        index=True,
    )

    repository_file: Mapped["RepositoryFile"] = relationship(
        "RepositoryFile",
        back_populates="chunks",
    )