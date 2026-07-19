from app.ai import AIService
from app.services.document_loader import DocumentLoader


class SummaryWorker:
    """
    Первый AI Worker.

    Загружает документ и передает его в AIService.
    """

    def __init__(self):
        self.loader = DocumentLoader()
        self.ai = AIService()

    def process(self, filename: str) -> dict:
        text = self.loader.load(filename)

        summary = self.ai.summarize(text)

        return {
            "success": True,
            "worker": "Summary Worker",
            "filename": filename,
            "result": summary,
        }