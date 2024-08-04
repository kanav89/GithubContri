from database import Base
from sqlalchemy import JSON, Column, Date, Integer, String
from sqlalchemy.ext.mutable import MutableDict


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    contributions = Column(JSON, default=[])


class Streak(Base):
    __tablename__ = "streaks"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    current_streak = Column(Integer, default=0)
    longest_streak_between_dates = Column(Integer, default=0)
    longest_streak_since_joining = Column(Integer, default=0)
    last_contribution_date = Column(Date)
    streak_history = Column(MutableDict.as_mutable(JSON), default={})
