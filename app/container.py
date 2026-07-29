from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.file_chunk import FileChunkRepository
from app.repositories.repository import RepositoryRepository
from app.repositories.repository_file import RepositoryFileRepository
from app.services.chunking.chunk_factory import ChunkFactory
from app.services.chunking.chunk_service import ChunkService
from app.services.file_indexer_service import FileIndexerService
from app.services.file_scanner import FileScanner
from app.services.git_service import GitService
from app.services.repository_service import RepositoryService


class AppContainer:
    """
    Application composition root.

    Creates and wires repositories and services.
    Every dependency is lazily instantiated and shared
    within the lifetime of this container.
    """

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self.db = db

        self._repository_repo: RepositoryRepository | None = None
        self._repository_file_repo: RepositoryFileRepository | None = None
        self._file_chunk_repo: FileChunkRepository | None = None

        self._git_service: GitService | None = None
        self._file_scanner: FileScanner | None = None

        self._chunk_factory: ChunkFactory | None = None
        self._chunk_service: ChunkService | None = None
        self._file_indexer_service: FileIndexerService | None = None

    # ------------------------------------------------------------------
    # Repositories
    # ------------------------------------------------------------------

    @property
    def repository_repo(self) -> RepositoryRepository:
        if self._repository_repo is None:
            self._repository_repo = RepositoryRepository(self.db)
        return self._repository_repo

    @property
    def repository_file_repo(self) -> RepositoryFileRepository:
        if self._repository_file_repo is None:
            self._repository_file_repo = RepositoryFileRepository(self.db)
        return self._repository_file_repo

    @property
    def file_chunk_repo(self) -> FileChunkRepository:
        if self._file_chunk_repo is None:
            self._file_chunk_repo = FileChunkRepository(self.db)
        return self._file_chunk_repo

    # ------------------------------------------------------------------
    # Infrastructure
    # ------------------------------------------------------------------

    @property
    def git_service(self) -> GitService:
        if self._git_service is None:
            self._git_service = GitService()
        return self._git_service

    @property
    def file_scanner(self) -> FileScanner:
        if self._file_scanner is None:
            self._file_scanner = FileScanner()
        return self._file_scanner

    # ------------------------------------------------------------------
    # Chunking
    # ------------------------------------------------------------------

    @property
    def chunk_factory(self) -> ChunkFactory:
        if self._chunk_factory is None:
            self._chunk_factory = ChunkFactory()
        return self._chunk_factory

    @property
    def chunk_service(self) -> ChunkService:
        if self._chunk_service is None:
            self._chunk_service = ChunkService(
                repository_file_repo=self.repository_file_repo,
                file_chunk_repo=self.file_chunk_repo,
                chunk_factory=self.chunk_factory,
            )
        return self._chunk_service

    # ------------------------------------------------------------------
    # File Indexing
    # ------------------------------------------------------------------

    @property
    def file_indexer_service(self) -> FileIndexerService:
        if self._file_indexer_service is None:
            self._file_indexer_service = FileIndexerService(
                scanner=self.file_scanner,
                repository_file_repo=self.repository_file_repo,
            )
        return self._file_indexer_service

    # ------------------------------------------------------------------
    # Top-level Services
    # ------------------------------------------------------------------

    @property
    def repository_service(self) -> RepositoryService:
        return RepositoryService(
            repository_repo=self.repository_repo,
            git_service=self.git_service,
            file_indexer=self.file_indexer_service,
            chunk_service=self.chunk_service,
        )
