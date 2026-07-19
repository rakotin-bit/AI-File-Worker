from openai import OpenAI

from app.config import settings
from app.ai.exceptions import AIProviderError
from app.ai.model_registry import ModelRegistry
from app.ai.model_priority import ModelPriorityManager



class OpenAIProvider:
    """
    Универсальный AI провайдер.

    Использует OpenAI API.
    При необходимости может использовать
    ModelPriorityManager для выбора моделей.
    """


    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

        self.model = settings.OPENAI_MODEL

        self.registry = ModelRegistry()

        self.priority_manager = ModelPriorityManager()



    def generate_summary(
        self,
        text: str
    ) -> str:

        try:

            response = self.client.responses.create(
                model=self.model,
                input=(
                    "Сделай краткое содержание документа.\n\n"
                    f"{text}"
                ),
            )


            self.priority_manager.mark_success(
                self.model
            )


            return response.output_text



        except Exception as error:


            self.priority_manager.mark_failure(
                self.model
            )


            print("=" * 60)
            print("OPENAI ERROR")
            print(error)
            print("=" * 60)


            raise AIProviderError(
                str(error)
            )