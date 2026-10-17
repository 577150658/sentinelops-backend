from fastapi import APIRouter

from app.routers import (
    tasks, findings, approvals, skills, audit, emergency,
    tools, models, reports, replay, imports, targets,
)

api_router = APIRouter()
api_router.include_router(tasks.router)
api_router.include_router(findings.router)
api_router.include_router(approvals.router)
api_router.include_router(skills.router)
api_router.include_router(audit.router)
api_router.include_router(emergency.router)
api_router.include_router(tools.router)
api_router.include_router(models.router)
api_router.include_router(reports.router)
api_router.include_router(replay.router)
api_router.include_router(imports.router)
api_router.include_router(targets.router)
