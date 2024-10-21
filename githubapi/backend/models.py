from database import Base
from sqlalchemy import JSON, Column, Date, ForeignKey, Integer, String
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, ForeignKey("users.username"))
    goal_type = Column(String)  # "daily", "weekly", or "monthly"
    target = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)

    user = relationship("User", back_populates="goals")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    access_token = Column(String, unique=True, index=True)
    contributions = Column(JSON, default=[])
    goals = relationship("Goal", back_populates="user")
    oauth2_tokens = relationship("OAuth2Token", back_populates="user")


class Streak(Base):
    __tablename__ = "streaks"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    current_streak = Column(Integer, default=0)
    longest_streak_between_dates = Column(Integer, default=0)
    longest_streak_since_joining = Column(Integer, default=0)
    last_contribution_date = Column(Date)
    streak_history = Column(MutableDict.as_mutable(JSON), default={})


class OAuth2Token(Base):
    __tablename__ = "oauth2_tokens"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40))
    token_type = Column(String(40))
    access_token = Column(String(200))
    # refresh_token = Column(String(200))
    expires_at = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="oauth2_tokens")

    def to_token(self):
        return dict(
            access_token=self.access_token,
            token_type=self.token_type,
            # refresh_token=self.refresh_token,
            expires_at=self.expires_at,
        )