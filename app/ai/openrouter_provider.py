import time

from openai import OpenAI

from app.config import settings
from app.ai.exceptions import AIProviderError
from app.ai.model_registry import ModelRegistry
from app.ai.model_router import ModelRouter
from app.ai.model_priority import ModelPriorityManager
from app.ai.model_performance import ModelPerformance


class OpenRouterProvider:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1",
        )

        self.registry = ModelRegistry()

        self.router = ModelRouter()

        self.priority = ModelPriorityManager()

        self.performance = ModelPerformance()


    def generate_summary(
        self,
        text: str,
    ) -> str:

        models = self.registry.get_free_models()

        if not models:
            raise AIProviderError(
                "Нет доступных моделей."
            )


        models = self.router.rank_models(
            models,
            self.priority,
        )


        last_error = None


        for model in models:

            try:

                print("=" * 60)
                print(
                    f"[OpenRouter] Trying model: {model}"
                )
                print("=" * 60)


                started = time.time()


                response = self.client.responses.create(
                    model=model,
                    input=(
                        "Сделай краткое содержание документа.\n\n"
                        f"{text}"
                    ),
                )


                elapsed = time.time() - started


                print("=" * 60)
                print(
                    f"[OpenRouter] Success: {model}"
                )

                print(
                    f"[Performance] "
                    f"Latency: {round(elapsed, 2)}s"
                )
                print("=" * 60)


                # Новый Performance Layer
                self.performance.record_success(
                    model,
                    elapsed,
                )


                stats = self.performance.get_stats(
                    model
                )


                print("=" * 60)
                print("[Model Stats]")
                print(
                    f"Success: "
                    f"{stats['success_count']}"
                )

                print(
                    f"Failures: "
                    f"{stats['failure_count']}"
                )

                print(
                    f"Average response time: "
                    f"{round(stats['avg_response_time'], 2)}s"
                )
                print("=" * 60)


                return response.output_text


            except Exception as error:

                last_error = error


                self.performance.record_failure(
                    model
                )


                print("=" * 60)
                print(
                    f"OPENROUTER ERROR ({model})"
                )
                print(error)
                print("=" * 60)


                if "free-models-per-day" in str(error):
                    break


        raise AIProviderError(
            f"Все модели недоступны.\n\n{last_error}"
        )