import stripe
import os
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_API_KEY")

def create_checkout_session(company_name: str, user_email: str):
    customer = stripe.Customer.create(
        name=company_name,
        email=user_email
    )

    checkout = stripe.checkout.Session.create(
        customer=customer.id,
        payment_method_types=["card"],
        line_items=[{
            "price": os.getenv("STRIPE_PRICE_ID"),
            "quantity": 1,
        }],
        mode="subscription",
        success_url="http://localhost:3000/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://localhost:3000/cancel",
    )

    return checkout.url, customer.id

