from pathlib import Path

from pypdf import PdfReader
from docx import Document

UPLOAD_DIR = Path("uploads")


class DocumentLoader:
    """
    Загружает текст документа.

    Поддерживаемые форматы:
    - TXT
    - PDF
    - DOCX
    """

    def load(self, filename: str) -> str:
        path = UPLOAD_DIR / filename

        if not path.exists():
            raise FileNotFoundError(f"Файл не найден: {filename}")

        extension = path.suffix.lower()

        if extension == ".txt":
            return self._load_txt(path)

        if extension == ".pdf":
            return self._load_pdf(path)

        if extension == ".docx":
            return self._load_docx(path)

        return f"Формат {extension} пока не поддерживается."

    def _load_txt(self, path: Path) -> str:
        text = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        return self._normalize(text)

    def _load_pdf(self, path: Path) -> str:
        reader = PdfReader(path)

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        if not pages:
            return "PDF не содержит извлекаемого текста."

        return self._normalize("\n\n".join(pages))

    def _load_docx(self, path: Path) -> str:
        document = Document(path)

        paragraphs = []

        for paragraph in document.paragraphs:
            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        if not paragraphs:
            return "DOCX не содержит текста."

        return self._normalize("\n".join(paragraphs))

    def _normalize(self, text: str) -> str:
        return (
            text.replace("\r\n", "\n")
                .replace("\r", "\n")
                .strip()
        )