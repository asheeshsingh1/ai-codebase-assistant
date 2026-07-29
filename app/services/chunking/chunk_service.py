from __future__ import annotations

from pathlib import Path

from app.db.models.file_chunk import FileChunk
from app.db.models.repository import Repository
from app.repositories.file_chunk import FileChunkRepository
from app.repositories.repository_file import RepositoryFileRepository

from .chunk_factory import ChunkFactory


class ChunkService:
    """
    Service responsible for generating semantic chunks for all files
    in a repository.
    """

    def __init__(
        self,
        repository_file_repo: RepositoryFileRepository,
        file_chunk_repo: FileChunkRepository,
        chunk_factory: ChunkFactory,
    ) -> None:
        self.repository_file_repo = repository_file_repo
        self.file_chunk_repo = file_chunk_repo
        self.chunk_factory = chunk_factory

    async def chunk_repository(
        self,
        repository: Repository,
    ) -> None:
        repository_files = (
            await self.repository_file_repo.get_by_repository_id(
                repository.id,
            )
        )

        repository_root = Path(repository.local_path)

        for repository_file in repository_files:
            absolute_path = repository_root / repository_file.relative_path

            if not absolute_path.exists():
                continue

            try:
                text = absolute_path.read_text(
                    encoding="utf-8",
                )
            except UnicodeDecodeError:
                text = absolute_path.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )

            chunker = self.chunk_factory.get_chunker(
                repository_file.extension,
            )

            chunks = chunker.chunk(text)

            await self.file_chunk_repo.delete_by_repository_file_id(
                repository_file.id,
            )

            db_chunks = [
                FileChunk(
                    repository_file_id=repository_file.id,
                    chunk_index=chunk.chunk_index,
                    chunk_type=chunk.chunk_type.value,
                    symbol_name=chunk.symbol_name,
                    content=chunk.content,
                    start_line=chunk.start_line,
                    end_line=chunk.end_line,
                    token_count=chunk.token_count,
                    content_hash=chunk.content_hash,
                )
                for chunk in chunks
            ]

            await self.file_chunk_repo.bulk_create(
                db_chunks,
            )