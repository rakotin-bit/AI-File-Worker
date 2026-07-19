import random


class ModelRouter:
    """
    Stable Router.

    Выбирает порядок моделей на основе статистики,
    но периодически исследует новые модели.

    Выполнение запроса выполняет Provider.
    Router отвечает только за выбор порядка моделей.
    """

    def __init__(self):
        self.exploration_rate = 0.2


    def rank_models(
        self,
        models,
        priority_manager,
    ):

        if not models:
            return []


        ranked = priority_manager.rank(
            models
        )


        exploration = False


        if (
            len(ranked) > 1
            and random.random() < self.exploration_rate
        ):

            exploration = True

            print("=" * 60)
            print("[Model Router] Exploration mode")
            print("=" * 60)


            first = ranked.pop(0)

            random.shuffle(ranked)

            ranked.insert(1, first)


        else:

            print("=" * 60)
            print("[Model Router] Stable mode")
            print("=" * 60)


        self._log_decision(
            ranked,
            priority_manager,
            exploration,
        )


        return ranked



    def _log_decision(
        self,
        ranked,
        priority_manager,
        exploration,
    ):

        if not ranked:
            return


        selected = ranked[0]


        stats = priority_manager.stats.get(
            selected
        )


        print("=" * 60)
        print("[Model Router Decision]")

        print(
            f"Selected model: {selected}"
        )


        if exploration:

            print(
                "Mode: Exploration"
            )

            print(
                "Reason: Testing alternative model"
            )

        else:

            print(
                "Mode: Stable"
            )

            print(
                "Reason: Highest calculated score"
            )


        print("Statistics:")

        print(
            f"Success: {stats['success_count']}"
        )

        print(
            f"Failures: {stats['failure_count']}"
        )

        print(
            f"Average response time: "
            f"{round(stats['avg_response_time'], 2)}s"
        )

        print("=" * 60)