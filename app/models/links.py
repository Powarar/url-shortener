from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseDB

class Urls(BaseDB):
    __tablename__ = "Urls"

    slug: Mapped[str] = mapped_column(primary_key=True, unique=True)
    url: Mapped[str]