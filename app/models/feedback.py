from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("company.id"))
    message = Column(Text, nullable=False)
    response = Column(Text)
    rating = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="feedbacks")
