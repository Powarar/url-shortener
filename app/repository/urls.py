# urls.py
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError

from app.engines.postgres_engine import db_engine
from app.models.links import Urls
from app.logic.shortener import generate_slug
from app.schemas.links import Link
from app.exceptions.errors import SlugAlreadyExistsError, NoLongUrlFoundError 


async def create_new_slug(long_url: Link) -> str:
    slug = generate_slug()
    url_str = str(long_url) 
    
    stmt = insert(Urls).values(slug=slug, url=url_str).returning(Urls.slug)
    
    try:
        result = await db_engine.execute(stmt)
        return result
        
    except IntegrityError as e:
        raise SlugAlreadyExistsError(f"Slug '{slug}' already exists in DB.")


async def get_link_by_slug(slug: str) -> str:
    stmt = select(Urls.url).where(Urls.slug == slug)
    long_url = await db_engine.execute(stmt)
    
    if not long_url:
        raise NoLongUrlFoundError(slug)
        
    return long_url