from sqlalchemy import Column, String, Integer, Float, ForeignKey, TIMESTAMP, text
from database import Base
from sqlalchemy.sql import func
from sqlalchemy import DateTime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    amount = Column(Float)
    category = Column(String)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))
    