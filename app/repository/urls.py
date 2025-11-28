from sqlalchemy.dialects.postgresql import insert

from app.engines.postgres_engine import db_engine
from app.models.links import Urls
from app.logic.shortener import generate_slug

async def create_new_slug(long_url: str):
    slug = generate_slug()
    stmt = insert(Urls).values(slug=slug, url=long_url).returning(Urls.slug)
    return await db_engine.execute(stmt)
