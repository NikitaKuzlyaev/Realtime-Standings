from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy import text, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=False)
    secret = Column(String, nullable=False)
    contest_id = Column(Integer, nullable=False)

    request = relationship("UserRequest", back_populates="user", uselist=False, cascade="all, delete-orphan")


class UserRequest(Base):
    __tablename__ = "user_requests"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    last_request = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    user = relationship("User", back_populates="request")


class LastRequestByContestAndMethod(Base):
    __tablename__ = "last_request_by_contest_and_method"

    contest_id = Column(Integer, index=True)
    method = Column(String, index=True)
    last_request = Column(DateTime(timezone=True), server_default=text("(now() - interval '365 days')"), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('contest_id', 'method'),
    )
