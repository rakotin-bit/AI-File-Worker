class DummyProvider:
    """
    Временный AI-провайдер.

    Используется, пока настоящая LLM не подключена.
    """

    def generate_summary(self, text: str) -> str:
        if not text.strip():
            return "Документ пуст."

        return (
            "=== Dummy AI ===\n\n"
            f"Получено символов: {len(text)}\n\n"
            + text[:1000]
        )