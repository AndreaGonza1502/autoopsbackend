from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class CalendlyWebhook(Base):
    __tablename__ = "calendly_webhooks"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    url = Column(String, nullable=False)  # webhook URL registrado en Calendly
    secret = Column(String, nullable=True)  # opcional para verificar firma
