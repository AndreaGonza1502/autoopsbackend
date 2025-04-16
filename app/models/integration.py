from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class WebhookLog(Base):
    __tablename__ = "webhook_log"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String)  # calendly, gcalendar, etc.
    payload = Column(Text)
    company_id = Column(Integer, ForeignKey("company.id"), nullable=True)
    received_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="webhook_logs", lazy="joined")
