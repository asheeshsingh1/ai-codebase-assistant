from app.services.llm.models import ChatMessage


class LLMService:

    def __init__(self, provider):
        self.provider = provider

    async def generate(
        self,
        messages: list[ChatMessage],
    ):
        return await self.provider.generate(messages)
