from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin
from sqlalchemy import UniqueConstraint


if TYPE_CHECKING:
    from app.db.models.file_chunk import FileChunk


class ChunkEmbedding(TimestampMixin, Base):
    __tablename__ = "chunk_embeddings"

    __table_args__ = (
        UniqueConstraint(
            "chunk_id",
            "provider",
            "model",
            name="uq_chunk_provider_model",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    chunk_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(
            "file_chunks.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    provider: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    model: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )

    dimensions: Mapped[int] = mapped_column(
        nullable=False,
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(),
        nullable=False,
    )

    chunk: Mapped["FileChunk"] = relationship(
        "FileChunk",
        back_populates="embeddings",
    )