from datetime import datetime
from typing import Any

from sqlalchemy import BIGINT, TIMESTAMP, String, func
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseDB(DeclarativeBase):
    __abstract__ = True

    type_annotation_map = {
        int: BIGINT,
        datetime: TIMESTAMP(timezone=False),
        str: String(),
        dict[str, Any]: JSONB,
        list[UUID]: ARRAY(UUID()),
        list[str]: ARRAY(String()),
    }

    # create_date: Mapped[datetime] = mapped_column(server_default=func.now())
    # update_date: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
