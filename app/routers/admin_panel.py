@router.get("/admin/metrics")
def get_admin_kpis(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    require_superadmin(user)
    return {
        "total_empresas": db.query(Company).count(),
        "total_usuarios": db.query(User).count(),
        "tareas_creadas": db.query(Task).count(),
        "tareas_completadas": db.query(Task).filter(Task.status == "done").count()
    }
