from fastapi import APIRouter, Depends, Request
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.routers.auth import get_current_user
from app.models.google_credentials import GoogleCredentials
from app.models.user import User
import os
from google_auth_oauthlib.flow import Flow
import json

router = APIRouter()

@router.get("/google/connect")
def connect_google(user: User = Depends(get_current_user)):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "redirect_uris": [os.getenv("GOOGLE_REDIRECT_URI")],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=["https://www.googleapis.com/auth/calendar"]
    )
    flow.redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")

    auth_url, _ = flow.authorization_url(prompt="consent")
    return {"url": auth_url}


@router.get("/google/callback")
def oauth_callback(request: Request, db: Session = Depends(get_db)):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "redirect_uris": [os.getenv("GOOGLE_REDIRECT_URI")],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=["https://www.googleapis.com/auth/calendar"]
    )
    flow.redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")

    authorization_response = str(request.url)
    flow.fetch_token(authorization_response=authorization_response)

    creds = flow.credentials

    user_id = 1  # ← ⚠️ Reemplazá con método real para recuperar el usuario

    existing = db.query(GoogleCredentials).filter(GoogleCredentials.user_id == user_id).first()

    if existing:
        existing.access_token = creds.token
        existing.refresh_token = creds.refresh_token
        existing.token_uri = creds.token_uri
        existing.client_id = creds.client_id
        existing.client_secret = creds.client_secret
        existing.scopes = ",".join(creds.scopes)
    else:
        new = GoogleCredentials(
            user_id=user_id,
            access_token=creds.token,
            refresh_token=creds.refresh_token,
            token_uri=creds.token_uri,
            client_id=creds.client_id,
            client_secret=creds.client_secret,
            scopes=",".join(creds.scopes)
        )
        db.add(new)

    db.commit()
    return {"message": "Cuenta de Google Calendar conectada correctamente ✅"}

