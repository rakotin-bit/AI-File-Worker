from .model_storage import ModelStorage
from .model_stats import ModelStats


class ModelPriorityManager:
    """
    Calculates model priority based on historical statistics.

    Responsibility:
        - Rank available models.
        - Calculate model score.
        - Record execution statistics.

    Does NOT:
        - Call AI providers.
        - Choose task type.
        - Execute requests.
    """

    # ------------------------------------------------------------------
    # Score weights
    # ------------------------------------------------------------------

    SUCCESS_WEIGHT = 10
    FAILURE_WEIGHT = 20
    LATENCY_WEIGHT = 1.0

    # ------------------------------------------------------------------

    def __init__(self):
        self.storage = ModelStorage()
        self.stats = ModelStats(self.storage)

    # ------------------------------------------------------------------

    def rank(self, models):

        ranked = sorted(
            models,
            key=self._calculate_score,
            reverse=True,
        )

        print("=" * 60)
        print("[Model Router] Model ranking:")

        for index, model in enumerate(ranked[:5], start=1):

            stat = self.stats.get(model)

            score = self._calculate_score(model)

            print(
                f"{index}. {model}"
            )

            print(
                f"   score={round(score, 2)} "
                f"success={stat['success_count']} "
                f"failure={stat['failure_count']} "
                f"time={round(stat['avg_response_time'], 2)}s"
            )

        print("=" * 60)

        return ranked

    # ------------------------------------------------------------------

    def explain_score(self, model):

        stat = self.stats.get(model)

        success_bonus = (
            stat["success_count"] * self.SUCCESS_WEIGHT
        )

        failure_penalty = (
            stat["failure_count"] * self.FAILURE_WEIGHT
        )

        latency_penalty = (
            stat["avg_response_time"] * self.LATENCY_WEIGHT
        )

        final_score = (
            success_bonus
            - failure_penalty
            - latency_penalty
        )

        return {
            "success_bonus": success_bonus,
            "failure_penalty": failure_penalty,
            "latency_penalty": latency_penalty,
            "score": final_score,
        }

    # ------------------------------------------------------------------

    def _calculate_score(self, model):

        score = self.explain_score(model)

        return score["score"]

    # ------------------------------------------------------------------

    def mark_success(
        self,
        model,
        response_time,
    ):

        self.stats.record_success(
            model,
            response_time,
        )

    # ------------------------------------------------------------------

    def mark_failure(
        self,
        model,
    ):

        self.stats.record_failure(model)