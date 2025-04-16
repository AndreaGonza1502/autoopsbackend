# app/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Crear engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=settings.DEBUG)

# Crear sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

# Dependency para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Validación inmediata al importar el módulo
def test_connection():
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        print("✅ Conexión a la base de datos exitosa.")
    except OperationalError as e:
        print("❌ Error al conectar a la base de datos:")
        print(e)

# Ejecutar validación al cargar el módulo
test_connection()
