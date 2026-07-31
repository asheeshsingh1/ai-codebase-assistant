from __future__ import annotations

from app.services.llm.models import ChatMessage, ChatRole
from app.services.search.models import SearchResult


class PromptBuilder:
    """
    Builds prompts for repository question answering.
    """

    SYSTEM_PROMPT = """
You are an expert software engineer helping developers understand a codebase.

Answer ONLY using the repository context provided.

Rules:
- Never invent code, APIs, classes or functions.
- If the answer is not present in the context, clearly say so.
- Prefer explaining code over guessing intent.
- Mention filenames when referring to code.
- Keep answers concise but complete.
- If multiple files are involved, explain how they relate.
""".strip()

    @classmethod
    def build(
        cls,
        question: str,
        search_results: list[SearchResult],
    ) -> list[ChatMessage]:

        context = cls._build_context(search_results)

        return [
            ChatMessage(
                role=ChatRole.SYSTEM,
                content=cls.SYSTEM_PROMPT,
            ),
            ChatMessage(
                role=ChatRole.USER,
                content=f"""
Repository Context

{context}

----------------------------------------

Question

{question}
""".strip(),
            ),
        ]

    @staticmethod
    def _build_context(
        search_results: list[SearchResult],
    ) -> str:

        sections: list[str] = []

        for index, result in enumerate(search_results, start=1):

            chunk = result.chunk

            section = "\n".join(
                [
                    f"Context #{index}",
                    f"Similarity : {result.similarity:.3f}",
                    f"File       : {chunk.repository_file.relative_path}",
                    f"Type       : {chunk.chunk_type}",
                    f"Symbol     : {chunk.symbol_name or '-'}",
                    f"Lines      : {chunk.start_line}-{chunk.end_line}",
                    "",
                    "Code:",
                    "```",
                    chunk.content,
                    "```",
                ]
            )

            sections.append(section)

        return "\n\n".join(sections)
