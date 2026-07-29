from __future__ import annotations

from pathlib import Path

from app.db.models.file_chunk import FileChunk
from app.db.models.repository import Repository
from app.repositories.file_chunk import FileChunkRepository
from app.repositories.repository_file import RepositoryFileRepository
from app.services.chunking.chunk_factory import ChunkFactory


class ChunkService:
    """
    Responsible for generating and persisting chunks for every file
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
        """
        Generate chunks for every indexed file belonging to a repository.
        """

        if repository.local_path is None:
            raise ValueError("Repository has no local path.")

        repository_files = (
            await self.repository_file_repo.get_by_repository(
                repository.id
            )
        )

        for repository_file in repository_files:

            absolute_path = (
                Path(repository.local_path)
                / repository_file.relative_path
            )

            if not absolute_path.exists():
                continue
            print("Reading file:", absolute_path)
            try:
                text = absolute_path.read_text(
                    encoding="utf-8",
                )
            except UnicodeDecodeError:
                text = absolute_path.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )
            print("File read:", len(text))

            chunker = self.chunk_factory.get_chunker(
                repository_file.extension,
            )
            print("Chunking...")

            chunks = chunker.chunk(
                text,
            )
            print("Chunks generated:", len(chunks))

            if not chunks:
                continue

            await self.file_chunk_repo.delete_by_repository_file(
                repository_file.id
            )

            file_chunks = [
                FileChunk(
                    repository_file_id=repository_file.id,
                    chunk_index=chunk.chunk_index,
                    content=chunk.content,
                    start_line=chunk.start_line,
                    end_line=chunk.end_line,
                    token_count=chunk.token_count,
                    content_hash=chunk.content_hash,
                )
                for chunk in chunks
            ]

            await self.file_chunk_repo.bulk_create(
                file_chunks
            )