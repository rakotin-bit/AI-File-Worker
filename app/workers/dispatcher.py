from app.workers.summary_worker import SummaryWorker


class WorkerDispatcher:
    """Диспетчер AI Workers."""

    def __init__(self):
        self.summary_worker = SummaryWorker()

    def process(self, worker: str, filename: str) -> dict:
        if worker == "summary":
            return self.summary_worker.process(filename)

        return {
            "success": False,
            "worker": worker,
            "filename": filename,
            "result": "Неизвестный AI Worker.",
        }