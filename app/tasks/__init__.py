from apscheduler.schedulers.background import BackgroundScheduler
from app.tasks.email_cron import scan_emails_for_all_users

scheduler = BackgroundScheduler()
scheduler.add_job(scan_emails_for_all_users, "interval", minutes=10)
scheduler.start()

print("✅ Scheduler de AutoOps iniciado (cada 10 min)")
