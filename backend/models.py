from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class Bounty(Base):
    __tablename__ = "bounties"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, index=True)
    title = Column(String)
    description = Column(Text)
    scope = Column(String)
    reward = Column(String)
    severity_rewards = Column(String)
    status = Column(String, default="ACTIVE")
    stellar_address = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    bounty_id = Column(Integer, index=True)
    researcher = Column(String)
    title = Column(String)
    description = Column(Text)
    severity = Column(String)
    evidence = Column(Text)
    hash = Column(String)
    stellar_tx_hash = Column(String, nullable=True)
    status = Column(String, default="SUBMITTED")
    created_at = Column(DateTime(timezone=True), server_default=func.now())