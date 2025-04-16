from pydantic import BaseModel

class SubscriptionOut(BaseModel):
    stripe_customer_id: str
    stripe_subscription_id: str
    active: bool

    class Config:
        from_attributes = True
