from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    auth, users, tasks, emails, rules, calendar,
    dashboard, notifications, templates, feedback, webhooks, admin, stats
)
from app.middleware.subscription_guard import SubscriptionMiddleware
from app.middleware.role_guard import RoleChecker
from apscheduler.schedulers.background import BackgroundScheduler
from app.tasks.email_cron import scan_emails_for_all_users

# ⬇️ NEW: DB Auto-init
from app.core.database import Base, engine

# ⬇️ NEW: Crear tablas si no existen
print("🛠️ Verificando/creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
print("✅ Base de datos inicializada correctamente.")

# ⬇️ FastAPI App
app = FastAPI(title="AutoOps Backend")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔒 Reemplazar por dominios específicos en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware personalizado
app.add_middleware(SubscriptionMiddleware)

# ⬇️ Background Cron Job
scheduler = BackgroundScheduler()
scheduler.add_job(scan_emails_for_all_users, "interval", minutes=10)
scheduler.start()

# Rutas organizadas por módulo
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(emails.router, tags=["Emails"])
app.include_router(rules.router, prefix="/rules", tags=["Rules"])
app.include_router(calendar.router, tags=["Calendar"])
app.include_router(dashboard.router, tags=["Dashboard"])
app.include_router(notifications.router, tags=["Notifications"])
app.include_router(templates.router, prefix="/templates", tags=["Templates"])
app.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(stats.router, prefix="/admin", tags=["Stats"])

# Ruta raíz de prueba
@app.get("/")
def root():
    return {"message": "🚀 AutoOps API is alive!"}

