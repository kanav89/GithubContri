from sqlalchemy import JSON, Column, Integer, String

from githubapi.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    contributions = Column(JSON, default=[])
