from typing import Annotated

from fastapi import FastAPI, File, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from src.parsing import Parser

app = FastAPI()

MAX_SIZE = 150_000
MAX_SIZE_L = 15_000
COUNT = 50

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=Path(BASE_DIR, 'static')), name="static")

templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))


@app.get("/files/", response_class=HTMLResponse)
async def load_file(request: Request):
    items = {'Без коэффициента точности': '', 'Коэффициент точности 1': 0, 'Коэффициент точности 2': 1}
    return templates.TemplateResponse(
        "form.html", {"request": request, 'items': items}
    )


@app.post("/files/idf")
async def create_file(request: Request, file: Annotated[bytes, File()], lev: Annotated[int | None, Form()] = None):
    current_max_size = MAX_SIZE if lev is None else MAX_SIZE_L
    if len(file) < current_max_size:
        if lev is None:
            parser = Parser(file)
            parser.tf_idf_f()
            return templates.TemplateResponse(
                "result.html", {"request": request,
                                'names': ('ID', 'Слово', 'TF', 'TF-IDF'),
                                'items': parser.get_res_for_table(COUNT)})
        else:
            parser = Parser(file, lev)
            parser.union_tf_by_lev()
            parser.tf_idf_f()
            return templates.TemplateResponse(
                "result.html", {"request": request,
                                'names': ('ID', 'Слово', 'TF', 'TF-IDF'),
                                'items': parser.get_res_for_table(COUNT)})
    else:
        raise HTTPException(
            status_code=403,
            detail=f"Слишком большой размер файла. Максимальный размер без коэффициента точности: {MAX_SIZE}."
            if lev is None else f"Слишком большой размер файла. Максимальный размер с коэффициентом точности{MAX_SIZE_L}")


def get_html():
    with open('src/templates/form.html', 'r', encoding='utf-8') as f:
        return f.read()
