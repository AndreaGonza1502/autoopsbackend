from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class GoogleCredentials(Base):
    __tablename__ = "google_credentials"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    token_uri = Column(String)
    client_id = Column(String)
    client_secret = Column(String)
    scopes = Column(String)
