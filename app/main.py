from fastapi import Body, FastAPI, HTTPException, status
from contextlib import asynccontextmanager
from app.engines.postgres_engine import db_engine
from app.repository.urls import create_new_slug


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_engine.create_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.post("/short_url")
async def generate_slug(
    long_url: str = Body(embed=True)
):
    try:
        new_slug = await create_new_slug(long_url)
    except Exception as s:
        raise s
    return {"data": new_slug}