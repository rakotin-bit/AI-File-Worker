from datetime import datetime
from pathlib import Path

from fastapi import UploadFile

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def save_files(files: list[UploadFile]) -> int:
    count = 0

    for file in files:
        if not file.filename:
            continue

        destination = UPLOAD_DIR / file.filename

        with destination.open("wb") as buffer:
            buffer.write(file.file.read())

        count += 1

    return count


def _format_size(size: int) -> str:
    if size < 1024:
        return f"{size} B"

    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"

    return f"{size / (1024 * 1024):.1f} MB"


def list_documents() -> list[dict]:
    documents = []

    for path in sorted(UPLOAD_DIR.iterdir(), key=lambda p: p.name.lower()):
        if not path.is_file():
            continue

        stat = path.stat()

        documents.append(
            {
                "name": path.name,
                "size": _format_size(stat.st_size),
                "modified": datetime.fromtimestamp(
                    stat.st_mtime
                ).strftime("%d.%m.%Y %H:%M"),
                "type": path.suffix.replace(".", "").upper() or "FILE",
            }
        )

    return documents