# urls.py
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError

from app.engines.postgres_engine import db_engine
from app.models.links import Urls
from app.logic.shortener import generate_slug
from app.schemas.links import Link
from app.exceptions import SlugAlreadyExistsError, NoLongUrlFoundError 


async def create_new_slug(long_url: Link) -> str:
    slug = generate_slug()
    url_str = str(long_url) 
    
    stmt = insert(Urls).values(slug=slug, url=url_str).returning(Urls.slug)
    
    try:
        result = await db_engine.execute(stmt)
        return result.scalar_one() 
        
    except IntegrityError as e:
        raise SlugAlreadyExistsError(f"Slug '{slug}' already exists in DB.")


async def get_link_by_slug(slug: str) -> str:
    stmt = select(Urls.url).where(Urls.slug == slug)
    result = await db_engine.execute(stmt)
    
    long_url = result.scalar_one_or_none()
    
    if not long_url:
        raise NoLongUrlFoundError(f"No link found for slug: {slug}")
        
    return long_url