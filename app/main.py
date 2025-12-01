from fastapi import Body, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from app.engines.postgres_engine import db_engine
from app.repository.urls import create_new_slug, get_link_by_slug


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
        
    except Exception as e:
        print(f"Database error while retrieving link: {e}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Could not generate a unique short link. Please try again.")
    return {"data": new_slug}

@app.get("/{slug}")
async def get_link(slug: str):
    try:
        long_url = await get_link_by_slug(slug)
    except Exception as e:
        print(f"Database error while retrieving link: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="link not found")
    return RedirectResponse(url=long_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)