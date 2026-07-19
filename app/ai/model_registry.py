import time
import requests

from app.config import settings


class ModelRegistry:
    """
    Получает список бесплатных моделей OpenRouter
    с TTL-кэшированием.
    """

    URL = "https://openrouter.ai/api/v1/models"

    CACHE_TTL = 300  # 5 минут

    _cache = None
    _cache_time = 0


    def get_free_models(self):

        # Проверяем кэш
        if self._cache_is_valid():
            print("=" * 60)
            print("MODEL REGISTRY CACHE HIT")
            print("=" * 60)

            return self._cache


        try:
            headers = {
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}"
            }


            response = requests.get(
                self.URL,
                headers=headers,
                timeout=20,
            )

            response.raise_for_status()

            data = response.json()

            models = []


            for model in data.get("data", []):

                model_id = model.get("id", "")

                if model_id.endswith(":free"):
                    models.append(model_id)


            # сохраняем в кэш
            self._cache = models
            self._cache_time = time.time()


            print("=" * 60)
            print(f"Found {len(models)} free models")
            print("MODEL REGISTRY CACHE UPDATED")
            print("=" * 60)


            return models


        except Exception as error:

            print("=" * 60)
            print("MODEL REGISTRY ERROR")
            print(error)
            print("=" * 60)

            return []


    def _cache_is_valid(self):

        if self._cache is None:
            return False


        elapsed = time.time() - self._cache_time

        return elapsed < self.CACHE_TTL