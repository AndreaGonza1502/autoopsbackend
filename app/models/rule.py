from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    condition = Column(Text, nullable=False)  # JSON lógico como string
    company_id = Column(Integer, ForeignKey("companies.id"))

