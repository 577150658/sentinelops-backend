#!/usr/bin/env python3
"""
init_backend.py
生成 SentinelOps 后端基础项目
用法: python init_backend.py [目录名]
"""

import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "sentinelops-backend")

DIRS = [
    "app",
    "app/core",
    "app/db",
    "app/db/models",
    "app/schemas",
    "app/routers",
]

FILES = {}

# ================================================================
# requirements.txt
# ================================================================
FILES["requirements.txt"] = """fastapi==0.115.0
uvicorn[standard]==0.32.0
sqlalchemy==2.0.36
pydantic==2.9.2
pydantic-settings==2.6.1
python-dotenv==1.0.1
websockets==13.1
"""

FILES[".env"] = """APP_NAME=SentinelOps API
DEBUG=true
DATABASE_URL=sqlite:///./sentinelops.db
CORS_ORIGINS=http://localhost:5500,http://127.0.0.1:5500,http://localhost:8000,http://localhost:3000
"""

FILES[".gitignore"] = """__pycache__/
*.py[cod]
*.db
*.db-journal
.env
.venv/
venv/
.idea/
.vscode/
"""

FILES["run.py"] = """#!/usr/bin/env python3
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
    )
"""

# ================================================================
# app/__init__.py
# ================================================================
FILES["app/__init__.py"] = ""

# ================================================================
# app/core
# ================================================================
FILES["app/core/__init__.py"] = ""

FILES["app/core/config.py"] = '''from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "SentinelOps API"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./sentinelops.db"
    CORS_ORIGINS: str = "http://localhost:5500,http://127.0.0.1:5500"

    @property
    def cors_origin_list(self) -> list[str]:
        return [s.strip() for s in self.CORS_ORIGINS.split(",") if s.strip()]


settings = Settings()
'''

FILES["app/core/ws_manager.py"] = '''from fastapi import WebSocket
from typing import Any


class WSManager:
    """管理所有活跃的 WebSocket 连接，广播事件到前端"""

    def __init__(self) -> None:
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        self.active.append(ws)
        print(f"[WS] connected, total={len(self.active)}")

    def disconnect(self, ws: WebSocket) -> None:
        if ws in self.active:
            self.active.remove(ws)
        print(f"[WS] disconnected, total={len(self.active)}")

    async def broadcast(self, event_type: str, payload: dict[str, Any]) -> None:
        """向前端推送事件，格式与前端 WSMock.emit 对齐"""
        message = {"type": event_type, "payload": payload}
        dead: list[WebSocket] = []
        for ws in self.active:
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)


ws_manager = WSManager()
'''

# ================================================================
# app/db
# ================================================================
FILES["app/db/__init__.py"] = ""

FILES["app/db/base.py"] = '''from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
'''

FILES["app/db/session.py"] = '''from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.base import Base

# SQLite 需要 check_same_thread=False 允许跨线程访问
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """创建所有表并填充种子数据"""
    from app.db import models  # noqa: F401  确保模型已注册
    Base.metadata.create_all(bind=engine)

    from app.db.seed import seed_if_empty
    seed_if_empty()
'''

# ================================================================
# app/db/models
# ================================================================
FILES["app/db/models/__init__.py"] = '''from app.db.models.task import Task
from app.db.models.finding import Finding
from app.db.models.approval import Approval
from app.db.models.skill import Skill
from app.db.models.audit import AuditLog

__all__ = ["Task", "Finding", "Approval", "Skill", "AuditLog"]
'''

FILES["app/db/models/task.py"] = '''from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String(16), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    phase: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(32), default="queued")
    risk: Mapped[str] = mapped_column(String(16), default="low")
    agent: Mapped[str] = mapped_column(String(64), default="")
    progress: Mapped[int] = mapped_column(Integer, default=0)
    command: Mapped[str] = mapped_column(String(512), default="")
'''

FILES["app/db/models/finding.py"] = '''from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Finding(Base):
    __tablename__ = "findings"

    id: Mapped[str] = mapped_column(String(16), primary_key=True)
    severity: Mapped[str] = mapped_column(String(16))
    title: Mapped[str] = mapped_column(String(255))
    target: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(16), default="pending")
    cvss: Mapped[float] = mapped_column(Float, default=0.0)
    tool: Mapped[str] = mapped_column(String(64), default="")
'''

FILES["app/db/models/approval.py"] = '''from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Approval(Base):
    __tablename__ = "approvals"

    id: Mapped[str] = mapped_column(String(16), primary_key=True)
    task_id: Mapped[str] = mapped_column(String(16), index=True)
    title: Mapped[str] = mapped_column(String(255))
    desc: Mapped[str] = mapped_column(String(512))
    command: Mapped[str] = mapped_column(String(512))
    risk: Mapped[str] = mapped_column(String(16))
'''

FILES["app/db/models/skill.py"] = '''from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[str] = mapped_column(String(16), primary_key=True)
    icon: Mapped[str] = mapped_column(String(8), default="📦")
    name: Mapped[str] = mapped_column(String(64))
    version: Mapped[str] = mapped_column(String(16))
    author: Mapped[str] = mapped_column(String(64))
    desc: Mapped[str] = mapped_column(Text)
    tags: Mapped[str] = mapped_column(String(255), default="")  # 逗号分隔
    risk: Mapped[str] = mapped_column(String(16), default="low")
    tools: Mapped[int] = mapped_column(Integer, default=0)
    runs: Mapped[int] = mapped_column(Integer, default=0)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
'''

FILES["app/db/models/audit.py"] = '''from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    time: Mapped[str] = mapped_column(String(16))
    actor: Mapped[str] = mapped_column(String(32))
    action: Mapped[str] = mapped_column(String(16))
    target: Mapped[str] = mapped_column(String(255))
    risk: Mapped[str] = mapped_column(String(16), default="low")
    hash: Mapped[str] = mapped_column(String(32))
    prev_hash: Mapped[str] = mapped_column(String(32), default="")
'''

# ================================================================
# app/db/seed.py
# ================================================================
FILES["app/db/seed.py"] = '''"""种子数据：与前端 seed.js 对齐"""
from datetime import datetime

from app.db.session import SessionLocal
from app.db.models import Task, Finding, Approval, Skill, AuditLog


def seed_if_empty() -> None:
    db = SessionLocal()
    try:
        if db.query(Task).count() > 0:
            return
        print("[seed] 初始化种子数据...")

        tasks = [
            Task(id="0341", title="Nmap 全端口扫描 10.0.3.0/24", phase="扫描",
                 status="running", risk="low", agent="recon-02", progress=72),
            Task(id="0342", title="Redis 未授权访问验证", phase="利用",
                 status="blocked", risk="critical", agent="exploit-01", progress=0,
                 command="redis-cli -h 10.0.3.44 -p 6379 INFO keyspace"),
            Task(id="0343", title="SSH 弱口令爆破 10.0.5.12", phase="利用",
                 status="blocked", risk="high", agent="exploit-01", progress=0,
                 command="hydra -l admin -P /wordlists/top1k.txt 10.0.5.12 ssh"),
            Task(id="0344", title="Nuclei 模板扫描 api.acme.com", phase="扫描",
                 status="done", risk="low", agent="scan-03", progress=100),
            Task(id="0345", title="目录爆破 /admin 路径", phase="枚举",
                 status="done", risk="medium", agent="fuzz-01", progress=100),
            Task(id="0346", title="API 端点 SQL 注入验证", phase="利用",
                 status="done", risk="critical", agent="exploit-02", progress=100),
        ]
        db.add_all(tasks)

        findings = [
            Finding(id="F-01", severity="critical", title="API 端点 SQL 注入",
                    target="api.acme.com", status="verified", cvss=9.8, tool="Nuclei"),
            Finding(id="F-02", severity="critical", title="Redis 未授权访问",
                    target="10.0.3.44:6379", status="pending", cvss=9.1, tool="Nmap"),
            Finding(id="F-03", severity="high", title="任意文件读取（路径穿越）",
                    target="files.acme.com", status="verified", cvss=7.5, tool="Burp"),
            Finding(id="F-04", severity="high", title="SSH 弱口令",
                    target="10.0.5.12:22", status="pending", cvss=7.2, tool="Hydra"),
            Finding(id="F-05", severity="high", title="备份文件可公开访问",
                    target="files.acme.com", status="verified", cvss=7.0, tool="ffuf"),
            Finding(id="F-06", severity="med", title="TLS 证书过期",
                    target="mail.acme.com", status="verified", cvss=5.3, tool="Nuclei"),
            Finding(id="F-07", severity="med", title="缺少安全响应头",
                    target="api.acme.com", status="verified", cvss=4.3, tool="Nuclei"),
            Finding(id="F-08", severity="low", title="服务器版本信息泄露",
                    target="10.0.3.44", status="fp", cvss=2.1, tool="Nmap"),
            Finding(id="F-09", severity="low", title="目录列表启用",
                    target="files.acme.com", status="verified", cvss=3.1, tool="ffuf"),
        ]
        db.add_all(findings)

        approvals = [
            Approval(id="A-01", task_id="0342", title="Redis 未授权访问验证",
                     desc="将对 10.0.3.44:6379 发起未授权访问测试，读取 keyspace 信息。",
                     command="redis-cli -h 10.0.3.44 -p 6379 INFO keyspace",
                     risk="critical"),
            Approval(id="A-02", task_id="0343", title="SSH 弱口令爆破",
                     desc="将对 10.0.5.12:22 发起字典爆破，字典规模 1000 条。",
                     command="hydra -l admin -P /wordlists/top1k.txt 10.0.5.12 ssh",
                     risk="high"),
        ]
        db.add_all(approvals)

        skills = [
            Skill(id="S-01", icon="🎯", name="sql-injection-probe", version="v1.2.0",
                  author="security-team · 官方仓库",
                  desc="Web 应用 SQL 注入检测与验证，覆盖 OWASP A03，支持盲注与时间盲注确认。",
                  tags="web,sqli,T1190", risk="high", tools=3, runs=42, enabled=True),
            Skill(id="S-02", icon="🔍", name="subdomain-enum", version="v2.0.1",
                  author="recon-lab · 官方仓库",
                  desc="被动 + 主动子域枚举，整合证书透明度日志、DNS 字典与搜索引擎结果。",
                  tags="recon,dns,T1590", risk="low", tools=2, runs=128, enabled=True),
            Skill(id="S-03", icon="⚡", name="redis-unauth-check", version="v1.0.3",
                  author="community · 社区",
                  desc="Redis 未授权访问检测，读取 keyspace 信息并评估数据敏感度。",
                  tags="redis,exposure,T1190", risk="med", tools=1, runs=17, enabled=True),
            Skill(id="S-04", icon="🔑", name="ssh-brute", version="v1.4.0",
                  author="security-team · 官方仓库",
                  desc="SSH 弱口令检测，支持字典分级与速率限制，所有执行均需人工审批。",
                  tags="ssh,brute,T1110", risk="high", tools=1, runs=9, enabled=True),
            Skill(id="S-05", icon="🛡️", name="tls-audit", version="v1.1.2",
                  author="community · 社区",
                  desc="TLS/SSL 配置审计，检测协议版本、加密套件、证书链与常见配置缺陷。",
                  tags="tls,audit", risk="low", tools=2, runs=64, enabled=True),
            Skill(id="S-06", icon="📡", name="api-fuzz", version="v0.9.4",
                  author="local-import · 本地导入",
                  desc="REST/GraphQL API 参数模糊测试，自动识别参数类型并生成边界值载荷。",
                  tags="api,fuzz,graphql", risk="med", tools=2, runs=3, enabled=True),
            Skill(id="S-07", icon="⬆️", name="privesc-linux", version="v1.0.0",
                  author="local-import · 本地导入",
                  desc="Linux 本地提权路径检查，枚举 SUID、sudo 配置、计划任务与内核版本。",
                  tags="linux,privesc,T1068", risk="crit", tools=1, runs=0, enabled=False),
            Skill(id="S-08", icon="📦", name="smb-enum", version="v1.3.1",
                  author="community · 社区",
                  desc="SMB 共享枚举与会话信息收集，识别匿名访问与可写共享。",
                  tags="smb,enum,T1135", risk="low", tools=1, runs=21, enabled=True),
        ]
        db.add_all(skills)

        # 审计日志（初始几条，形成哈希链）
        seed_logs = [
            ("09:35:00", "operator", "停止", "sandbox · kali-02", "medium"),
            ("09:36:12", "admin", "配置", "model · deepseek-reasoner", "info"),
            ("09:38:44", "operator", "执行", "task-0345 · ffuf", "medium"),
            ("09:40:18", "system", "执行", "task-0344 · nuclei", "low"),
            ("09:41:30", "operator", "拒绝", "task-0339 · metasploit", "high"),
            ("09:42:55", "approver", "批准", "task-0342 · redis", "critical"),
            ("09:43:02", "operator", "执行", "task-0341 · nmap", "low"),
        ]
        prev = "genesis"
        for t, actor, action, target, risk in seed_logs:
            h = _compute_hash(prev, {"time": t, "actor": actor,
                                     "action": action, "target": target})
            db.add(AuditLog(time=t, actor=actor, action=action,
                            target=target, risk=risk, hash=h, prev_hash=prev))
            prev = h

        db.commit()
        print(f"[seed] 完成：{len(tasks)} 任务, {len(findings)} 发现, "
              f"{len(approvals)} 审批, {len(skills)} Skill")
    finally:
        db.close()


def _compute_hash(prev_hash: str, record: dict) -> str:
    import hashlib
    import json
    payload = json.dumps(record, sort_keys=True) + prev_hash
    return hashlib.sha256(payload.encode()).hexdigest()[:16]
'''

# ================================================================
# app/schemas
# ================================================================
FILES["app/schemas/__init__.py"] = ""

FILES["app/schemas/task.py"] = '''from pydantic import BaseModel, ConfigDict


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    phase: str
    status: str
    risk: str
    agent: str
    progress: int
    command: str = ""
'''

FILES["app/schemas/finding.py"] = '''from pydantic import BaseModel, ConfigDict


class FindingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    severity: str
    title: str
    target: str
    status: str
    cvss: float
    tool: str
'''

FILES["app/schemas/approval.py"] = '''from pydantic import BaseModel, ConfigDict


class ApprovalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    taskId: str
    title: str
    desc: str
    command: str
    risk: str
'''

FILES["app/schemas/skill.py"] = '''from pydantic import BaseModel


class SkillOut(BaseModel):
    id: str
    icon: str
    name: str
    version: str
    author: str
    desc: str
    tags: list[str]
    risk: str
    tools: int
    runs: int
    enabled: bool
'''

FILES["app/schemas/audit.py"] = '''from pydantic import BaseModel, ConfigDict


class AuditOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    time: str
    actor: str
    action: str
    target: str
    risk: str
    hash: str
'''

# ================================================================
# app/routers
# ================================================================
FILES["app/routers/__init__.py"] = '''from fastapi import APIRouter

from app.routers import tasks, findings, approvals, skills, audit, emergency

api_router = APIRouter()
api_router.include_router(tasks.router)
api_router.include_router(findings.router)
api_router.include_router(approvals.router)
api_router.include_router(skills.router)
api_router.include_router(audit.router)
api_router.include_router(emergency.router)
'''

FILES["app/routers/tasks.py"] = '''from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Task, Approval, AuditLog
from app.schemas.task import TaskOut
from app.core.ws_manager import ws_manager

router = APIRouter(tags=["tasks"])


def _hash(prev: str, record: dict) -> str:
    import hashlib, json
    return hashlib.sha256(
        (json.dumps(record, sort_keys=True) + prev).encode()
    ).hexdigest()[:16]


def _append_audit(db: Session, actor: str, action: str, target: str, risk: str) -> None:
    last = db.query(AuditLog).order_by(AuditLog.id.desc()).first()
    prev = last.hash if last else "genesis"
    record = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "actor": actor,
        "action": action,
        "target": target,
    }
    db.add(AuditLog(
        time=record["time"], actor=actor, action=action,
        target=target, risk=risk, hash=_hash(prev, record), prev_hash=prev,
    ))


@router.get("/engagements/{eid}/tasks", response_model=list[TaskOut])
def list_tasks(eid: str, db: Session = Depends(get_db)):
    return db.query(Task).all()


class ApproveBody(BaseModel):
    actor: str = "approver"


@router.post("/tasks/{task_id}/approve")
async def approve_task(task_id: str, body: ApproveBody | None = None,
                       db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(404, "task not found")
    if task.status != "blocked":
        raise HTTPException(400, f"task status={task.status}, cannot approve")

    task.status = "running"
    task.progress = 5
    db.query(Approval).filter(Approval.task_id == task_id).delete()
    _append_audit(db, (body.actor if body else "approver"),
                  "批准", f"task-{task_id}", task.risk)
    db.commit()

    await ws_manager.broadcast("task.progress",
                               {"taskId": task_id, "progress": 5})
    await ws_manager.broadcast("audit.log", {
        "time": datetime.now().strftime("%H:%M:%S"),
        "actor": "approver", "action": "批准",
        "target": f"task-{task_id}",
    })
    return {"ok": True, "taskId": task_id}


@router.post("/tasks/{task_id}/reject")
async def reject_task(task_id: str, body: ApproveBody | None = None,
                      db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(404, "task not found")

    task.status = "rejected"
    db.query(Approval).filter(Approval.task_id == task_id).delete()
    _append_audit(db, (body.actor if body else "approver"),
                  "拒绝", f"task-{task_id}", task.risk)
    db.commit()

    await ws_manager.broadcast("audit.log", {
        "time": datetime.now().strftime("%H:%M:%S"),
        "actor": "approver", "action": "拒绝",
        "target": f"task-{task_id}",
    })
    return {"ok": True, "taskId": task_id}


class VerifyBody(BaseModel):
    name: str


@router.post("/tasks/verify")
async def create_verify_task(body: VerifyBody, db: Session = Depends(get_db)):
    import time
    vid = "V-" + str(int(time.time()))[-4:]
    _append_audit(db, "operator", "执行", f"{vid} · {body.name}", "medium")
    db.commit()
    await ws_manager.broadcast("audit.log", {
        "time": datetime.now().strftime("%H:%M:%S"),
        "actor": "operator", "action": "执行",
        "target": f"{vid} · {body.name}",
    })
    return {"id": vid, "name": body.name, "status": "pending_approval"}
'''

FILES["app/routers/findings.py"] = '''from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Finding
from app.schemas.finding import FindingOut

router = APIRouter(tags=["findings"])


@router.get("/engagements/{eid}/findings", response_model=list[FindingOut])
def list_findings(eid: str, db: Session = Depends(get_db)):
    return db.query(Finding).all()
'''

FILES["app/routers/approvals.py"] = '''from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Approval
from app.schemas.approval import ApprovalOut

router = APIRouter(tags=["approvals"])


@router.get("/engagements/{eid}/approvals", response_model=list[ApprovalOut])
def list_approvals(eid: str, db: Session = Depends(get_db)):
    rows = db.query(Approval).all()
    return [
        ApprovalOut(
            id=r.id, taskId=r.task_id, title=r.title,
            desc=r.desc, command=r.command, risk=r.risk,
        )
        for r in rows
    ]
'''

FILES["app/routers/skills.py"] = '''from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Skill
from app.schemas.skill import SkillOut

router = APIRouter(tags=["skills"])


@router.get("/skills", response_model=list[SkillOut])
def list_skills(db: Session = Depends(get_db)):
    rows = db.query(Skill).all()
    return [
        SkillOut(
            id=r.id, icon=r.icon, name=r.name, version=r.version,
            author=r.author, desc=r.desc,
            tags=[t for t in (r.tags or "").split(",") if t],
            risk=r.risk, tools=r.tools, runs=r.runs, enabled=r.enabled,
        )
        for r in rows
    ]
'''

FILES["app/routers/audit.py"] = '''from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import AuditLog
from app.schemas.audit import AuditOut

router = APIRouter(tags=["audit"])


@router.get("/engagements/{eid}/audit", response_model=list[AuditOut])
def list_audit(eid: str, db: Session = Depends(get_db)):
    return db.query(AuditLog).order_by(AuditLog.id.desc()).all()
'''

FILES["app/routers/emergency.py"] = '''from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Task, AuditLog
from app.core.ws_manager import ws_manager

router = APIRouter(tags=["emergency"])


def _hash(prev: str, record: dict) -> str:
    import hashlib, json
    return hashlib.sha256(
        (json.dumps(record, sort_keys=True) + prev).encode()
    ).hexdigest()[:16]


@router.post("/emergency-stop")
async def emergency_stop(db: Session = Depends(get_db)):
    db.query(Task).filter(Task.status == "running").update({"status": "stopped"})

    last = db.query(AuditLog).order_by(AuditLog.id.desc()).first()
    prev = last.hash if last else "genesis"
    record = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "actor": "operator", "action": "停止",
        "target": "所有沙箱任务",
    }
    db.add(AuditLog(
        time=record["time"], actor="operator", action="停止",
        target="所有沙箱任务", risk="high",
        hash=_hash(prev, record), prev_hash=prev,
    ))
    db.commit()

    await ws_manager.broadcast("audit.log", {
        "time": record["time"], "actor": "operator",
        "action": "停止", "target": "所有沙箱任务",
    })
    return {"ok": True}
'''

FILES["app/routers/ws.py"] = '''import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.ws_manager import ws_manager

ws_router = APIRouter()


@ws_router.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        # 心跳：每 30 秒发一次 ping，保持连接
        while True:
            try:
                await asyncio.wait_for(websocket.receive_text(), timeout=30)
            except asyncio.TimeoutError:
                await websocket.send_json({"type": "ping", "payload": {}})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception:
        ws_manager.disconnect(websocket)
'''

# ================================================================
# app/main.py
# ================================================================
FILES["app/main.py"] = '''from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import init_db
from app.routers import api_router
from app.routers.ws import ws_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化数据库
    init_db()
    print(f"[startup] {settings.APP_NAME} 已就绪")
    yield
    print("[shutdown] 服务停止")


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
app.include_router(ws_router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.APP_NAME}


@app.get("/")
async def root():
    return {
        "service": settings.APP_NAME,
        "docs": "/docs",
        "health": "/health",
    }
'''

# ================================================================
# 主流程
# ================================================================
def main():
    print(f"▶ 创建后端项目: {ROOT}")
    ROOT.mkdir(parents=True, exist_ok=True)

    for d in DIRS:
        (ROOT / d).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {d}/")

    for rel, content in FILES.items():
        full = ROOT / rel
        full.parent.mkdir(parents=True, exist_ok=True)
        if full.exists():
            print(f"  · {rel} 已存在，跳过")
            continue
        full.write_text(content, encoding="utf-8")
        print(f"  + {rel}")

    print()
    print("✅ 完成！")
    print()
    print("下一步:")
    print(f"  cd {ROOT}")
    print("  python -m venv .venv")
    print("  .venv\\Scripts\\activate     # Windows")
    print("  source .venv/bin/activate    # macOS / Linux")
    print("  pip install -r requirements.txt")
    print("  python run.py")
    print()
    print("  访问 http://localhost:8080/docs 查看 API 文档")


if __name__ == "__main__":
    main()