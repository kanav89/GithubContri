from database import Base, SessionLocal
from sqlalchemy import JSON, Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    contributions = Column(JSON, default=[])
