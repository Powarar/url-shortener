from fastapi import Body, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from contextlib import asynccontextmanager
from app.engines.postgres_engine import db_engine
from app.repository.urls import create_new_slug, get_link_by_slug
from app.schemas.links import Link
from exceptions.exceptions import ShortenerBaseError, SlugAlreadyExistsError, NoLongUrlFoundError

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_engine.create_tables()
    yield

app = FastAPI(lifespan=lifespan)


app.exception_handler(SlugAlreadyExistsError)
async def already_exists_handler(request: Request, exc: SlugAlreadyExistsError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Could not generate unique link. Try again.", "error_code": "SLUG_CONFLICT"}
    )

@app.exception_handler(NoLongUrlFoundError)
async def not_found_handler(request: Request, exc: NoLongUrlFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Link not found", "error_code": "NOT_FOUND"}
    )


@app.post("/short_url")
async def generate_slug(payload: Link):
    new_slug = await create_new_slug(payload)
    return {"data": new_slug}


@app.get("/{slug}")
async def get_link(slug: str):
    long_url = await get_link_by_slug(slug)
    return RedirectResponse(url=long_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)