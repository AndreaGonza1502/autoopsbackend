from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.core.database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    stripe_customer_id = Column(String, nullable=False)
    stripe_subscription_id = Column(String, nullable=False)
    active = Column(Boolean, default=True)
