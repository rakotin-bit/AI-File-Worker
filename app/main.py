from pathlib import Path

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.file_service import save_files, list_documents
from app.workers.dispatcher import WorkerDispatcher

app = FastAPI(title="AI File Worker")

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)

dispatcher = WorkerDispatcher()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "documents": list_documents(),
            "message": None,
        },
    )


@app.post("/", response_class=HTMLResponse)
async def upload_files(
    request: Request,
    files: list[UploadFile] = File(...)
):
    uploaded = save_files(files)

    if uploaded == 1:
        message = "Успешно загружен 1 файл."
    else:
        message = f"Успешно загружено {uploaded} файлов."

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "documents": list_documents(),
            "message": message,
        },
    )


@app.post("/documents/{filename}/process", response_class=HTMLResponse)
async def process_document(
    request: Request,
    filename: str,
):
    result = dispatcher.process(
        worker="summary",
        filename=filename,
    )

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "result": result,
        },
    )


@app.get("/health")
async def health():
    return {"status": "ok"}