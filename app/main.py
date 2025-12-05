from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager

from app.engines.postgres_engine import db_engine
from app.repository.urls import create_new_slug, get_link_by_slug
from app.schemas.links import Link

# импортируем сами функции обработчиков
from app.exceptions.exceptions_handlers import (
    not_found_handler,
    conflict_handler,
    global_exception_handler
)

# импортируем кастомные ошибки
from app.exceptions.errors import NoLongUrlFoundError, SlugAlreadyExistsError


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_engine.create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.add_exception_handler(NoLongUrlFoundError, not_found_handler)
app.add_exception_handler(SlugAlreadyExistsError, conflict_handler)
app.add_exception_handler(Exception, global_exception_handler)


@app.post("/short_url")
async def generate_slug(payload: Link):
    new_slug = await create_new_slug(payload)
    return {"data": new_slug}


@app.get("/{slug}")
async def get_link(slug: str):
    long_url = await get_link_by_slug(slug)
    return RedirectResponse(url=long_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
