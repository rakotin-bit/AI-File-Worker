from .model_storage import ModelStorage
from .model_stats import ModelStats


class ModelPerformance:
    """
    Слой управления производительностью AI моделей.

    Отвечает только за:
    - запись успешных запросов;
    - запись ошибок;
    - получение статистики моделей.

    Не отвечает за:
    - выбор модели;
    - ранжирование моделей;
    - вызов AI API.
    """

    def __init__(self):

        self.storage = ModelStorage()
        self.stats = ModelStats(
            self.storage
        )


    def record_success(
        self,
        model,
        response_time,
    ):
        """
        Записывает успешный запрос модели.
        """

        self.stats.record_success(
            model,
            response_time,
        )


    def record_failure(
        self,
        model,
    ):
        """
        Записывает ошибку модели.
        """

        self.stats.record_failure(
            model
        )


    def get_stats(
        self,
        model,
    ):
        """
        Возвращает статистику модели.
        """

        return self.stats.get(
            model
        )