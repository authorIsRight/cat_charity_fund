from datetime import datetime

from app.core.db import Base
from sqlalchemy import Boolean, Column, DateTime, Integer


class Abstract(Base):
    """
    Предназначен для наследования CharityProject и Donation.
    """
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
