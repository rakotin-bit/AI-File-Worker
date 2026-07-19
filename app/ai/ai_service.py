from app.config import settings

from app.ai.exceptions import AIProviderError
from app.ai.providers import DummyProvider
from app.ai.openai_provider import OpenAIProvider
from app.ai.openrouter_provider import OpenRouterProvider


class AIService:
    """
    Универсальный сервис работы с AI.

    Порядок работы:
    1. OpenRouter
    2. OpenAI
    3. DummyProvider
    """

    def __init__(self):
        self.providers = []

        if settings.OPENROUTER_API_KEY:
            self.providers.append(OpenRouterProvider())

        if settings.OPENAI_API_KEY:
            self.providers.append(OpenAIProvider())

        # Dummy всегда последний
        self.providers.append(DummyProvider())

    def summarize(self, text: str) -> str:
        last_error = None

        for provider in self.providers:
            try:
                return provider.generate_summary(text)

            except AIProviderError as error:
                print(f"Provider {provider.__class__.__name__} failed:")
                print(error)
                last_error = error
                continue

        return (
            "❌ Все AI-провайдеры недоступны.\n\n"
            "Проверьте API-ключи или подключение к интернету.\n\n"
            f"Последняя ошибка:\n{last_error}"
        )