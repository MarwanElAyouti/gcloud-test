from datetime import datetime

import pytz
from sqlalchemy import Column, DateTime, inspect
from sqlalchemy.ext.declarative import as_declarative

from friendlyeats.settings import DEFAULT_TIMEZONE


def get_now_tz_aware():
    return datetime.now(tz=pytz.timezone(DEFAULT_TIMEZONE))


@as_declarative()
class Base:
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    created_at = Column(DateTime(timezone=True), default=get_now_tz_aware)
    updated_at = Column(DateTime(timezone=True), onupdate=get_now_tz_aware)
