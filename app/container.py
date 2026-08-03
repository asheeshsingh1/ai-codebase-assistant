# app/container.py
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.chat_repository import ChatRepository
from app.repositories.file_chunk import FileChunkRepository
from app.repositories.repository import RepositoryRepository
from app.repositories.repository_file import RepositoryFileRepository
from app.services.chat.chat_history_service import ChatHistoryService
from app.services.chunking.chunk_factory import ChunkFactory
from app.services.chunking.chunk_service import ChunkService
from app.services.embeddings.models import EmbeddingProviderType
from app.services.file_indexer_service import FileIndexerService
from app.services.file_scanner import FileScanner
from app.services.git_service import GitService
from app.services.repository.repository_service import RepositoryService

from app.core.config import settings

from app.repositories.chunk_embedding_repository import ChunkEmbeddingRepository

from app.services.embeddings.config import EmbeddingProviderConfig
from app.services.embeddings.embedding_service import EmbeddingService
from app.services.embeddings.provider_factory import EmbeddingProviderFactory
from app.services.embeddings.base import EmbeddingProvider

from app.repositories.search import SearchRepository

from app.services.search.retrieval_service import RetrievalService

from app.services.llm.base import LLMProvider
from app.services.llm.config import LLMProviderConfig
from app.services.llm.provider_factory import LLMProviderFactory

from app.services.chat.chat_service import ChatService

from app.repositories.search import SearchRepository

from app.services.chat.chat_service import ChatService
from app.services.llm.config import LLMProviderConfig
from app.services.llm.llm_service import LLMService
from app.services.llm.provider_factory import LLMProviderFactory
from app.services.llm.base import LLMProvider
from app.services.search.retrieval_service import RetrievalService


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
        self._chunk_embedding_repo: ChunkEmbeddingRepository | None = None

        self._embedding_provider: EmbeddingProvider | None = None
        self._embedding_service: EmbeddingService | None = None
        self._search_repository: SearchRepository | None = None
        self._retrieval_service: RetrievalService | None = None
        self._llm_provider: LLMProvider | None = None
        self._chat_service: ChatService | None = None
        self._search_repository: SearchRepository | None = None

        self._llm_provider: LLMProvider | None = None
        self._llm_service: LLMService | None = None

        self._retrieval_service: RetrievalService | None = None
        self._chat_service: ChatService | None = None

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

    @property
    def chunk_embedding_repo(self) -> ChunkEmbeddingRepository:
        if self._chunk_embedding_repo is None:
            self._chunk_embedding_repo = ChunkEmbeddingRepository(
                self.db,
            )
        return self._chunk_embedding_repo

    @property
    def search_repository(self) -> SearchRepository:
        if self._search_repository is None:
            self._search_repository = SearchRepository(
                self.db,
            )

        return self._search_repository

    @property
    def search_repository(self) -> SearchRepository:

        if self._search_repository is None:
            self._search_repository = SearchRepository(
                self.db,
            )

        return self._search_repository

    @property
    def chat_repository(self) -> ChatRepository:
        return ChatRepository(
            self.db,
        )

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

    @property
    def embedding_provider(self) -> EmbeddingProvider:

        if self._embedding_provider is None:
            api_key = {
                EmbeddingProviderType.OPENAI: settings.openai_api_key,
                EmbeddingProviderType.OPENROUTER: settings.openrouter_api_key,
            }[settings.embedding_provider]

            config = EmbeddingProviderConfig(
                provider=settings.embedding_provider,
                api_key=api_key,
                model=settings.embedding_model,
            )

            self._embedding_provider = EmbeddingProviderFactory.create(config)

        return self._embedding_provider

    @property
    def llm_provider(self) -> LLMProvider:

        if self._llm_provider is None:

            config = LLMProviderConfig(
                provider=settings.llm_provider,
                api_key=settings.openrouter_api_key,
                model=settings.llm_model,
            )

            self._llm_provider = LLMProviderFactory.create(
                config,
            )

        return self._llm_provider

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
            embedding_service=self.embedding_service,
        )

    @property
    def embedding_service(self) -> EmbeddingService:

        if self._embedding_service is None:
            self._embedding_service = EmbeddingService(
                provider=self.embedding_provider,
                chunk_embedding_repo=self.chunk_embedding_repo,
            )

        return self._embedding_service

    @property
    def retrieval_service(self) -> RetrievalService:
        if self._retrieval_service is None:
            self._retrieval_service = RetrievalService(
                embedding_service=self.embedding_service,
                search_repository=self.search_repository,
            )

        return self._retrieval_service

    @property
    def chat_service(self) -> ChatService:
        return ChatService(
            retrieval_service=self.retrieval_service,
            llm_service=self.llm_service,
            chat_history_service=self.chat_history_service,
        )

    @property
    def llm_service(self) -> LLMService:

        if self._llm_service is None:
            self._llm_service = LLMService(
                provider=self.llm_provider,
            )

        return self._llm_service

    @property
    def retrieval_service(self) -> RetrievalService:

        if self._retrieval_service is None:
            self._retrieval_service = RetrievalService(
                embedding_service=self.embedding_service,
                search_repository=self.search_repository,
            )

        return self._retrieval_service

    @property
    def chat_history_service(self) -> ChatHistoryService:
        return ChatHistoryService(
            chat_repository=self.chat_repository,
        )
