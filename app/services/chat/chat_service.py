from __future__ import annotations

from uuid import UUID

from app.services.chat.chat_history_service import ChatHistoryService
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
        Save User Message
            ↓
        RetrievalService
            ↓
        PromptBuilder
            ↓
        LLMService
            ↓
        Save Assistant Message
            ↓
        ChatResult
    """

    def __init__(
        self,
        retrieval_service: RetrievalService,
        llm_service: LLMService,
        chat_history_service: ChatHistoryService,
    ) -> None:
        self.retrieval_service = retrieval_service
        self.llm_service = llm_service
        self.chat_history_service = chat_history_service

    async def ask(
        self,
        repository_id: UUID,
        question: str,
    ) -> ChatResult:
        """
        Answer a repository question using Retrieval-Augmented Generation (RAG).
        """

        # Save user message
        await self.chat_history_service.save_user_message(
            repository_id=repository_id,
            content=question,
        )

        # Retrieve relevant chunks
        search_results = await self.retrieval_service.retrieve(
            repository_id=repository_id,
            query=question,
            limit=10,
        )

        # Build prompt
        messages = PromptBuilder.build(
            question=question,
            search_results=search_results,
        )

        # Generate answer
        answer = await self.llm_service.generate(
            messages,
        )

        # Build citations
        citations = [
            Citation(
                repository_file_id=result.chunk.repository_file.id,
                file_path=result.chunk.repository_file.relative_path,
                start_line=result.chunk.start_line,
                end_line=result.chunk.end_line,
            )
            for result in search_results
        ]

        # Save assistant response
        await self.chat_history_service.save_assistant_message(
            repository_id=repository_id,
            content=answer,
            citations=[
                {
                    "repository_file_id": str(citation.repository_file_id),
                    "file_path": citation.file_path,
                    "start_line": citation.start_line,
                    "end_line": citation.end_line,
                }
                for citation in citations
            ],
        )

        return ChatResult(
            answer=answer,
            citations=citations,
        )
