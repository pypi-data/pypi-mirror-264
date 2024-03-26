"""Base models for corvic RDBMS backed orm tables."""

from __future__ import annotations

from datetime import datetime
from typing import Any, ClassVar

import sqlalchemy as sa
import sqlalchemy.orm as sa_orm

from corvic.orm.func import gen_uuid, utc_now
from corvic.orm.keys import ForeignKey, MappedPrimaryKey, primary_key_column


class Base(sa_orm.MappedAsDataclass, sa_orm.DeclarativeBase):
    """Base class for all DB mapped classes."""

    created_at: sa_orm.Mapped[datetime] = sa_orm.mapped_column(
        sa.DateTime, server_default=utc_now(), init=False
    )
    updated_at: sa_orm.Mapped[datetime] = sa_orm.mapped_column(
        sa.DateTime, onupdate=utc_now(), nullable=True, init=False
    )

    @classmethod
    def foreign_key(cls):
        return ForeignKey(cls=cls)


class OrgBase(Base):
    """An organization it a top level grouping of resources."""

    __tablename__ = "org"

    # overriding table_args is the recommending way of defining these base model types
    __table_args__: ClassVar[Any] = (
        sa.UniqueConstraint("name"),
        {"extend_existing": True},
    )

    id: MappedPrimaryKey = primary_key_column()
    name: sa_orm.Mapped[str] = sa_orm.mapped_column(
        sa.Text, server_default=gen_uuid(), default=None
    )
