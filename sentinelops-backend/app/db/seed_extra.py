"""补充种子数据：tools / models / reports"""
from app.db.session import SessionLocal
from app.db.models import Tool, AIModel, Report


def seed_extra_if_empty() -> None:
    db = SessionLocal()
    try:
        if db.query(Tool).count() == 0:
            tools = [
                Tool(id="T-01", endpoint="kali-mcp-server", tools="Nmap, Hydra",
                     permission="扫描", signature="已校验", last_call="09:42:11", enabled=True),
                Tool(id="T-02", endpoint="burp-mcp", tools="Burp Suite",
                     permission="利用", signature="已校验", last_call="09:38:44", enabled=True),
                Tool(id="T-03", endpoint="nuclei-mcp", tools="Nuclei",
                     permission="扫描", signature="已校验", last_call="09:41:02", enabled=True),
                Tool(id="T-04", endpoint="playwright-mcp", tools="Chromium",
                     permission="只读", signature="已校验", last_call="09:35:20", enabled=True),
                Tool(id="T-05", endpoint="ffuf-mcp", tools="ffuf, wfuzz",
                     permission="扫描", signature="已校验", last_call="09:40:18", enabled=True),
                Tool(id="T-06", endpoint="sqlmap-mcp", tools="SQLMap",
                     permission="利用", signature="待校验", last_call="—", enabled=False),
                Tool(id="T-07", endpoint="metasploit-mcp", tools="Metasploit",
                     permission="后渗透", signature="已校验", last_call="—", enabled=False),
                Tool(id="T-08", endpoint="unknown-mcp-server", tools="—",
                     permission="未知", signature="校验失败", last_call="—", enabled=False),
            ]
            db.add_all(tools)

        if db.query(AIModel).count() == 0:
            models = [
                AIModel(id="M-01", name="DeepSeek-Reasoner", kind="cloud",
                        endpoint="api.deepseek.com", latency=320, status="online", enabled=True),
                AIModel(id="M-02", name="Qwen2.5-14B-Instruct", kind="local",
                        endpoint="localhost:11434", latency=1400, status="busy", enabled=True),
                AIModel(id="M-03", name="Qwen2.5-7B-Instruct", kind="local",
                        endpoint="localhost:11434", latency=0, status="offline", enabled=True),
            ]
            db.add_all(models)

        if db.query(Report).count() == 0:
            reports = [
                Report(id="R-01", title="ENG-2041 中期报告", fmt="PDF",
                       created="2026-09-23", size="4.2 MB", status="ready",
                       content="# ENG-2041 中期报告\n\n9 发现 · 2 Critical · 3 High"),
                Report(id="R-02", title="ENG-2041 侦察阶段报告", fmt="JSON",
                       created="2026-09-23", size="820 KB", status="ready",
                       content='{"engagement": "ENG-2041", "assets": 12}'),
                Report(id="R-03", title="ENG-2041 最终报告", fmt="PDF",
                       created="—", size="—", status="generating", content=""),
            ]
            db.add_all(reports)

        db.commit()
        print("[seed_extra] tools / models / reports 已填充")
    finally:
        db.close()
