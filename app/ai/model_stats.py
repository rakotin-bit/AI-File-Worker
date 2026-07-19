class ModelStats:
    def __init__(self, storage):
        self.storage = storage

    def get(self, model):
        self.storage.create_if_missing(model)
        return self.storage.get(model)

    def record_success(self, model, response_time):
        stats = self.get(model)

        success_count = stats["success_count"] + 1
        total_time = stats["total_response_time"] + response_time

        avg_time = total_time / success_count

        self.storage.update(
            model,
            {
                "success_count": success_count,
                "total_response_time": total_time,
                "avg_response_time": avg_time,
            },
        )

    def record_failure(self, model):
        stats = self.get(model)

        failure_count = stats["failure_count"] + 1

        self.storage.update(
            model,
            {
                "failure_count": failure_count,
            },
        )