from __future__ import annotations

from uuid import UUID

from app.services.chat.models import ChatResult, Citation
from app.services.chat.prompt_builder import PromptBuilder
from app.services.llm.llm_service import LLMService
from app.services.search.retrieval_service import RetrievalService


class ChatService:
    """
    Orchestrates the repository question-answering flow.

    Flow:
        Question
            ↓
        RetrievalService
            ↓
        PromptBuilder
            ↓
        LLMService
            ↓
        ChatResult
    """

    def __init__(
        self,
        retrieval_service: RetrievalService,
        llm_service: LLMService,
    ) -> None:
        self.retrieval_service = retrieval_service
        self.llm_service = llm_service

    async def ask(
        self,
        repository_id: UUID,
        question: str,
    ) -> ChatResult:
        """
        Answer a repository question using Retrieval-Augmented Generation (RAG).
        """

        search_results = await self.retrieval_service.retrieve(
            repository_id=repository_id,
            query=question,
            limit=10,
        )

        print("1. Retrieved chunks")

        messages = PromptBuilder.build(
            question=question,
            search_results=search_results,
        )

        print("2. Prompt built")

        answer = await self.llm_service.generate(
            messages,
        )

        print("3. LLM finished")

        citations = [
            Citation(
                file_path=result.chunk.repository_file.relative_path,
                start_line=result.chunk.start_line,
                end_line=result.chunk.end_line,
            )
            for result in search_results
        ]

        return ChatResult(
            answer=answer,
            citations=citations,
        )
