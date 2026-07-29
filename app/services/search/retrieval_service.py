from __future__ import annotations

from uuid import UUID

from app.repositories.search import SearchRepository
from app.services.embeddings.embedding_service import EmbeddingService
from app.services.search.models import SearchResult


class RetrievalService:
    """
    Service responsible for retrieving the most relevant chunks
    for a user query.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        search_repository: SearchRepository,
    ) -> None:
        self.embedding_service = embedding_service
        self.search_repository = search_repository

    async def retrieve(
        self,
        repository_id: UUID,
        query: str,
        limit: int = 10,
    ) -> list[SearchResult]:
        """
        Retrieve the most semantically relevant chunks for a query.
        """

        query_embedding = await self.embedding_service.embed_query(
            query,
        )

        return await self.search_repository.similarity_search(
            repository_id=repository_id,
            embedding=query_embedding,
            limit=limit,
        )
