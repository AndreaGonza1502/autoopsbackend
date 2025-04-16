from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.subscription import Subscription
from app.services.stripe_service import create_checkout_session
from app.models.user import User
from app.models.company import Company
import stripe, os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Endpoint para generar checkout URL
@router.post("/billing/subscribe")
def subscribe(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden suscribirse")

    url, customer_id = create_checkout_session(user.company.name, user.email)
    return {"checkout_url": url}

# Webhook de Stripe para suscripciones completadas
@router.post("/billing/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, secret)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook inválido: {str(e)}")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_id = session["customer"]
        subscription_id = session["subscription"]
        email = session.get("customer_email") or session["customer_details"]["email"]

        # Buscar el usuario admin por email
        user = db.query(User).filter(User.email == email, User.role == "admin").first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario administrador no encontrado")

        # Verificar si ya existe una suscripción para la empresa
        existing = db.query(Subscription).filter(
            Subscription.company_id == user.company_id
        ).first()

        if existing:
            existing.stripe_customer_id = customer_id
            existing.stripe_subscription_id = subscription_id
            existing.active = True
        else:
            new_sub = Subscription(
                company_id=user.company_id,
                stripe_customer_id=customer_id,
                stripe_subscription_id=subscription_id,
                active=True
            )
            db.add(new_sub)

        db.commit()

    return {"status": "success"}
