import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Настройки приложения.
    """

    # ---------- OpenAI ----------

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv(
        "OPENAI_MODEL",
        "gpt-4.1-mini",
    )

    # ---------- OpenRouter ----------

    OPENROUTER_API_KEY = os.getenv(
        "OPENROUTER_API_KEY"
    )

    # Для совместимости со старым кодом
    OPENROUTER_MODEL = os.getenv(
        "OPENROUTER_MODEL",
        "google/gemma-3-27b-it:free",
    )

    # Список моделей по умолчанию
    OPENROUTER_MODELS = [
        "google/gemma-3-27b-it:free",
        "meta-llama/llama-3.3-70b-instruct:free",
        "mistralai/mistral-small-3.2-24b-instruct:free",
        "qwen/qwen3-32b:free",
    ]

    # Совместимость с новым кодом
    @property
    def openrouter_api_key(self):
        return self.OPENROUTER_API_KEY

    @property
    def openrouter_model(self):
        return self.OPENROUTER_MODEL

    @property
    def openai_api_key(self):
        return self.OPENAI_API_KEY

    @property
    def openai_model(self):
        return self.OPENAI_MODEL


settings = Settings()