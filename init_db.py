from app.core.database import Base, engine
from app.models.user import User
from app.models.company import Company
from app.models.document import Document  # si estás usando documentos
# Podés agregar más modelos aquí...

print("🛠️ Creando las tablas...")
Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas con éxito.")
