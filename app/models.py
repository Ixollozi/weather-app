from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from datetime import datetime
from .database import Base
from sqlalchemy.sql import func


class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    city_name = Column(String)
    country = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    search_count = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

