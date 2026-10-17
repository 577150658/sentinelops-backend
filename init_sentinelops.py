#!/usr/bin/env python3
"""
init_sentinelops.py
生成完整可运行的 SentinelOps 前端项目（补全版）
用法: python init_sentinelops.py [目录名]
"""

import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "sentinelops")
DIRS = ["styles", "js", "js/core", "js/data", "js/render", "js/bindings", ".vscode"]

# ================================================================
# HTML 片段
# ================================================================

TOPBAR = r"""<header class="topbar">
  <div class="brand">
    <div class="brand-mark">DS</div>
    <div>
      <div class="brand-name">SentinelOps</div>
      <div class="brand-sub">AI Pentest Console</div>
    </div>
  </div>
  <div class="eng-switch">
    <span class="eng-id">ENG-2041</span>
    <span class="eng-title">ACME Corp · Q4 外部评估</span>
    <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="color:var(--muted)"><path d="M6 9l6 6 6-6"/></svg>
  </div>
  <span class="badge badge--lock">
    <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
      <rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
    </svg>
    范围已锁定
  </span>
  <div class="spacer"></div>
  <div class="model-chips">
    <div class="chip">
      <span class="dot dot--on"></span>
      <div><div class="chip-label">DeepSeek</div><div class="chip-meta">reasoner · 320ms</div></div>
    </div>
    <div class="chip">
      <span class="dot dot--busy"></span>
      <div><div class="chip-label">本地 Qwen2.5-14B</div><div class="chip-meta">GPU 68% · 队列 3</div></div>
    </div>
  </div>
  <button class="btn-stop" onclick="openStop()">
    <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="6" width="12" height="12" rx="2"/></svg>
    紧急停止
  </button>
</header>
"""

# 导航图标
ICON_GRID = '<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="9"/><rect x="14" y="3" width="7" height="5"/><rect x="14" y="12" width="7" height="9"/><rect x="3" y="16" width="7" height="5"/></svg>'
ICON_TARGET = '<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/></svg>'
ICON_LIST = '<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h12M3 18h6"/></svg>'
ICON_TERM = '<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 17l6-6-6-6"/><path d="M12 19h8"/></svg>'
ICON_SHIELD = '<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l9 4v6c0 5-3.8 9.4-9 10-5.2-.6-9-5-9-10V6z"/></svg>'
ICON_JS = '<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M10 12l-2 2 2 2M14 12l2 2-2 2"/></svg>'
ICON_MINI = '<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="5" y="2" width="14" height="20" rx="2"/><path d="M12 18h.01"/></svg>'
ICON_APP = '<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="6" y="2" width="12" height="20" rx="2"/><circle cx="12" cy="18" r="1"/></svg>'
ICON_TRAFFIC = '<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12h4l3-9 4 18 3-9h4"/></svg>'
ICON_MODEL = '<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9L17 7M7 17l-2.1 2.1"/></svg>'
ICON_TOOL = '<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a4 4 0 0 0 5 5l-9 9a2.1 2.1 0 0 1-3-3z"/></svg>'
ICON_SKILL = '<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l2.4 7.4H22l-6 4.4 2.3 7.2-6.3-4.6L5.7 21 8 13.8l-6-4.4h7.6z"/></svg>'
ICON_AUDIT = '<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></svg>'
ICON_REPORT = '<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3v18h18"/><path d="M7 14l4-4 3 3 5-6"/></svg>'

SIDEBAR = f"""<nav class="sidebar">
  <div>
    <div class="nav-group-title">作战</div>
    <div class="nav">
      <div class="nav-item active" data-page="dashboard">{ICON_GRID}仪表盘</div>
      <div class="nav-item" data-page="engagement">{ICON_TARGET}目标范围 <span class="nav-count">12</span></div>
      <div class="nav-item" data-page="orchestration">{ICON_LIST}任务编排 <span class="nav-count">34</span></div>
      <div class="nav-item" data-page="execution">{ICON_TERM}实时执行 <span class="nav-count nav-count--alert">5</span></div>
      <div class="nav-item" data-page="findings">{ICON_SHIELD}漏洞发现 <span class="nav-count">9</span></div>
    </div>
  </div>
  <div>
    <div class="nav-group-title">逆向分析</div>
    <div class="nav">
      <div class="nav-item" data-page="js-analysis">{ICON_JS}JS 分析 <span class="nav-count">6</span></div>
      <div class="nav-item" data-page="miniapp-analysis">{ICON_MINI}小程序分析 <span class="nav-count">3</span></div>
      <div class="nav-item" data-page="app-analysis">{ICON_APP}App 分析 <span class="nav-count">2</span></div>
      <div class="nav-item" data-page="traffic-analysis">{ICON_TRAFFIC}抓包分析 <span class="nav-count nav-count--alert">248</span></div>
    </div>
  </div>
  <div>
    <div class="nav-group-title">配置</div>
    <div class="nav">
      <div class="nav-item" data-page="models">{ICON_MODEL}模型管理</div>
      <div class="nav-item" data-page="tools">{ICON_TOOL}工具管理 <span class="nav-count">8</span></div>
      <div class="nav-item" data-page="skills">{ICON_SKILL}Skill 管理 <span class="nav-count">14</span></div>
      <div class="nav-item" data-page="audit">{ICON_AUDIT}审计日志</div>
      <div class="nav-item" data-page="reports">{ICON_REPORT}报告</div>
    </div>
  </div>
</nav>
"""

PAGE_DASHBOARD = r"""<div class="page" id="page-dashboard">
  <div class="page-head">
    <div>
      <h1 class="page-title">作战仪表盘</h1>
      <p class="page-desc">ENG-2041 · 授权窗口 09:00 → 18:00 · 已运行 02:14:37</p>
    </div>
  </div>
  <div class="kpis">
    <div class="kpi"><div class="kpi-label">目标资产</div><div class="kpi-value">12</div><div class="kpi-foot">3 域名 · 9 IP 段</div></div>
    <div class="kpi"><div class="kpi-label">执行任务</div><div class="kpi-value">34</div><div class="kpi-foot">5 运行中 · 29 完成</div></div>
    <div class="kpi"><div class="kpi-label">有效发现</div><div class="kpi-value" style="color:var(--high)">9</div><div class="kpi-foot">2 Critical · 3 High</div></div>
    <div class="kpi"><div class="kpi-label">风险评分</div><div class="kpi-value" style="color:var(--crit)">7.8</div>
      <div class="kpi-foot"><div class="bar" style="flex:1;margin-top:0"><div class="bar-fill bar-fill--warn" style="width:78%"></div></div></div>
    </div>
  </div>
  <section class="section">
    <div class="section-head"><span class="section-title">攻击路径</span><span class="section-sub">Planner · DeepSeek-Reasoner 驱动</span><div class="spacer"></div><span class="badge badge--lock" style="height:22px;font-size:10px">阶段 4 / 6</span></div>
    <div class="section-body">
      <div class="flow">
        <div class="flow-node done"><div class="flow-circle">01</div><div class="flow-label">侦察</div><div class="flow-meta">4m 12s</div></div>
        <div class="flow-link done"></div>
        <div class="flow-node done"><div class="flow-circle">02</div><div class="flow-label">扫描</div><div class="flow-meta">11m 03s</div></div>
        <div class="flow-link done"></div>
        <div class="flow-node done"><div class="flow-circle">03</div><div class="flow-label">枚举</div><div class="flow-meta">18m 47s</div></div>
        <div class="flow-link active"></div>
        <div class="flow-node active"><div class="flow-circle">04</div><div class="flow-label">利用</div><div class="flow-meta">进行中</div></div>
        <div class="flow-link"></div>
        <div class="flow-node"><div class="flow-circle">05</div><div class="flow-label">后渗透</div><div class="flow-meta">待执行</div></div>
        <div class="flow-link"></div>
        <div class="flow-node"><div class="flow-circle">06</div><div class="flow-label">报告</div><div class="flow-meta">待执行</div></div>
      </div>
    </div>
  </section>
  <section class="section">
    <div class="section-head"><span class="section-title">最新发现</span><span class="section-sub">Validator 已验证</span><div class="spacer"></div><button class="btn" style="height:26px;font-size:11px" onclick="go('findings')">查看全部</button></div>
    <table class="table">
      <thead><tr><th style="width:90px">严重性</th><th>标题</th><th style="width:180px">目标</th><th style="width:110px">状态</th><th style="width:70px">CVSS</th></tr></thead>
      <tbody>
        <tr><td><span class="sev sev--crit">Critical</span></td><td>API 端点 SQL 注入</td><td class="mono">api.acme.com</td><td><span class="tag tag--verified">已验证</span></td><td class="mono">9.8</td></tr>
        <tr><td><span class="sev sev--crit">Critical</span></td><td>Redis 未授权访问</td><td class="mono">10.0.3.44:6379</td><td><span class="tag tag--pending">待验证</span></td><td class="mono">9.1</td></tr>
        <tr><td><span class="sev sev--high">High</span></td><td>任意文件读取（路径穿越）</td><td class="mono">files.acme.com</td><td><span class="tag tag--verified">已验证</span></td><td class="mono">7.5</td></tr>
        <tr><td><span class="sev sev--high">High</span></td><td>SSH 弱口令</td><td class="mono">10.0.5.12:22</td><td><span class="tag tag--pending">待验证</span></td><td class="mono">7.2</td></tr>
        <tr><td><span class="sev sev--med">Medium</span></td><td>TLS 证书过期</td><td class="mono">mail.acme.com</td><td><span class="tag tag--verified">已验证</span></td><td class="mono">5.3</td></tr>
      </tbody>
    </table>
  </section>
  <section class="section">
    <div class="section-head"><span class="dot dot--busy"></span><span class="section-title">实时执行流</span><span class="section-sub">Recon 子代理 · Qwen2.5-14B (local)</span></div>
    <div style="padding:12px">
      <div class="term" id="live-terminal">
        <div class="term-line t-dim">[09:42:11] 调度器 → 分配任务 task-0341 至 recon-agent-02</div>
        <div class="term-line t-cmd">$ nmap -sV -T4 --top-ports 1000 10.0.3.0/24 -oX /tmp/scan.xml</div>
        <div class="term-line t-ok">[+] 10.0.3.44  22/tcp   open  ssh      OpenSSH 8.2p1</div>
        <div class="term-line t-ok">[+] 10.0.3.44  6379/tcp open  redis    Redis 6.0.9</div>
        <div class="term-line t-warn">[!] 10.0.3.44  6379/tcp 未授权访问 — 疑似配置缺陷</div>
        <div class="term-line t-info">[i] 本地模型摘要：2 个服务，1 个高危候选，已上报 Validator</div>
        <div class="term-line t-ok">[+] Validator 确认：Redis 未授权访问可利用，已生成 Finding</div>
        <div class="term-line t-cmd">$ <span class="t-cursor"></span></div>
      </div>
    </div>
  </section>
</div>
"""

PAGE_ENGAGEMENT = r"""<div class="page" id="page-engagement" hidden>
  <div class="page-head">
    <div><h1 class="page-title">目标范围</h1><p class="page-desc">所有目标均在书面授权范围内，启动后范围锁定。</p></div>
    <div class="page-actions"><button class="btn">导入授权文件</button><button class="btn btn--primary">+ 添加目标</button></div>
  </div>
  <div class="grid-2">
    <section class="section" style="margin:0">
      <div class="section-head"><span class="section-title">授权信息</span><div class="spacer"></div><span class="tag tag--verified">有效</span></div>
      <div class="section-body">
        <div class="kv"><span class="kv-key">授权编号</span><span class="kv-val">AUTH-2026-0912</span></div>
        <div class="kv"><span class="kv-key">委托方</span><span class="kv-val">ACME Corp</span></div>
        <div class="kv"><span class="kv-key">测试类型</span><span class="kv-val">外部黑盒 + 灰盒</span></div>
        <div class="kv"><span class="kv-key">有效期</span><span class="kv-val">2026-09-23 → 2026-09-27</span></div>
        <div class="kv"><span class="kv-key">授权文件</span><span class="kv-val" style="color:var(--accent)">authorization.pdf</span></div>
      </div>
    </section>
    <section class="section" style="margin:0">
      <div class="section-head"><span class="section-title">时间窗口与限制</span></div>
      <div class="section-body">
        <div class="form-row"><div><div class="form-label">允许时间窗口</div><div class="form-hint">超出窗口自动停止所有任务</div></div><span class="mono">09:00 – 18:00</span></div>
        <div class="form-row"><div><div class="form-label">请求速率限制</div><div class="form-hint">每个目标 IP 的并发连接上限</div></div><span class="mono">10 req/s</span></div>
        <div class="form-row"><div><div class="form-label">破坏性操作</div><div class="form-hint">利用类动作需人工审批</div></div><span class="tag tag--blocked">强制审批</span></div>
        <div class="form-row"><div><div class="form-label">范围锁定</div><div class="form-hint">启动后禁止修改目标列表</div></div><div class="toggle on" onclick="this.classList.toggle('on')"></div></div>
      </div>
    </section>
  </div>
  <section class="section">
    <div class="section-head"><span class="section-title">目标资产</span><span class="section-sub">共 12 项</span></div>
    <table class="table">
      <thead><tr><th>目标</th><th style="width:120px">类型</th><th style="width:160px">资产归属</th><th style="width:110px">状态</th><th style="width:90px">发现数</th></tr></thead>
      <tbody>
        <tr><td class="mono">api.acme.com</td><td>域名</td><td>核心业务</td><td><span class="tag tag--done">已扫描</span></td><td class="mono">3</td></tr>
        <tr><td class="mono">files.acme.com</td><td>域名</td><td>文件服务</td><td><span class="tag tag--done">已扫描</span></td><td class="mono">2</td></tr>
        <tr><td class="mono">mail.acme.com</td><td>域名</td><td>邮件网关</td><td><span class="tag tag--done">已扫描</span></td><td class="mono">1</td></tr>
        <tr><td class="mono">10.0.3.0/24</td><td>网段</td><td>内网服务区</td><td><span class="tag tag--running">扫描中</span></td><td class="mono">2</td></tr>
        <tr><td class="mono">10.0.5.0/24</td><td>网段</td><td>管理区</td><td><span class="tag tag--queued">待扫描</span></td><td class="mono">1</td></tr>
      </tbody>
    </table>
  </section>
</div>
"""

PAGE_ORCHESTRATION = r"""<div class="page" id="page-orchestration" hidden>
  <div class="page-head">
    <div><h1 class="page-title">任务编排</h1><p class="page-desc">Planner 生成的任务序列，高风险任务需 Approver 放行。</p></div>
  </div>
  <div class="tabs" data-tabs="orch">
    <div class="tab active" data-panel="orch-all">全部任务 (34)</div>
    <div class="tab" data-panel="orch-run">运行中 (5)</div>
    <div class="tab" data-panel="orch-approve">待审批 (2)</div>
    <div class="tab" data-panel="orch-done">已完成 (27)</div>
  </div>
  <div data-tab-group="orch">
    <div class="tab-panel" id="orch-all">
      <section class="section" style="margin:0">
        <table class="table">
          <thead><tr><th style="width:80px">ID</th><th>任务</th><th style="width:110px">阶段</th><th style="width:110px">状态</th><th style="width:100px">风险</th><th style="width:100px">执行者</th></tr></thead>
          <tbody>
            <tr><td class="mono">0341</td><td>Nmap 全端口扫描 10.0.3.0/24</td><td>扫描</td><td><span class="tag tag--running">运行中</span></td><td><span class="sev sev--low">Low</span></td><td class="mono">recon-02</td></tr>
            <tr><td class="mono">0342</td><td>Redis 未授权访问验证</td><td>利用</td><td><span class="tag tag--blocked">待审批</span></td><td><span class="sev sev--crit">Critical</span></td><td class="mono">exploit-01</td></tr>
            <tr><td class="mono">0343</td><td>SSH 弱口令爆破 10.0.5.12</td><td>利用</td><td><span class="tag tag--blocked">待审批</span></td><td><span class="sev sev--high">High</span></td><td class="mono">exploit-01</td></tr>
            <tr><td class="mono">0344</td><td>Nuclei 模板扫描 api.acme.com</td><td>扫描</td><td><span class="tag tag--done">已完成</span></td><td><span class="sev sev--low">Low</span></td><td class="mono">scan-03</td></tr>
            <tr><td class="mono">0345</td><td>目录爆破 /admin 路径</td><td>枚举</td><td><span class="tag tag--done">已完成</span></td><td><span class="sev sev--med">Medium</span></td><td class="mono">fuzz-01</td></tr>
            <tr><td class="mono">0346</td><td>API 端点 SQL 注入验证</td><td>利用</td><td><span class="tag tag--done">已完成</span></td><td><span class="sev sev--crit">Critical</span></td><td class="mono">exploit-02</td></tr>
          </tbody>
        </table>
      </section>
    </div>
    <div class="tab-panel" id="orch-run" hidden>
      <section class="section" style="margin:0">
        <table class="table">
          <thead><tr><th style="width:80px">ID</th><th>任务</th><th style="width:110px">阶段</th><th style="width:140px">进度</th></tr></thead>
          <tbody>
            <tr><td class="mono">0341</td><td>Nmap 全端口扫描 10.0.3.0/24</td><td>扫描</td><td><div class="bar" style="margin-top:0"><div class="bar-fill" style="width:72%"></div></div></td></tr>
            <tr><td class="mono">0347</td><td>子域枚举 acme.com</td><td>侦察</td><td><div class="bar" style="margin-top:0"><div class="bar-fill" style="width:38%"></div></div></td></tr>
            <tr><td class="mono">0348</td><td>HTTP 响应指纹采集</td><td>侦察</td><td><div class="bar" style="margin-top:0"><div class="bar-fill" style="width:55%"></div></div></td></tr>
          </tbody>
        </table>
      </section>
    </div>
    <div class="tab-panel" id="orch-approve" hidden>
      <section class="section" style="margin:0">
        <div class="section-body">
          <div class="approve" style="margin-bottom:12px">
            <div class="approve-title">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 9v4M12 17h.01"/><path d="M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/></svg>
              任务 0342 · Redis 未授权访问验证
            </div>
            <div class="approve-desc">将对 10.0.3.44:6379 发起未授权访问测试，读取 keyspace 信息。</div>
            <div class="approve-cmd">redis-cli -h 10.0.3.44 -p 6379 INFO keyspace</div>
            <div class="approve-actions"><button class="btn btn--danger">拒绝</button><button class="btn btn--primary">批准执行</button></div>
          </div>
          <div class="approve">
            <div class="approve-title">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 9v4M12 17h.01"/><path d="M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/></svg>
              任务 0343 · SSH 弱口令爆破
            </div>
            <div class="approve-desc">将对 10.0.5.12:22 发起字典爆破，字典规模 1000 条。</div>
            <div class="approve-cmd">hydra -l admin -P /wordlists/top1k.txt 10.0.5.12 ssh</div>
            <div class="approve-actions"><button class="btn btn--danger">拒绝</button><button class="btn btn--primary">批准执行</button></div>
          </div>
        </div>
      </section>
    </div>
    <div class="tab-panel" id="orch-done" hidden>
      <section class="section" style="margin:0">
        <div class="empty">已完成 27 个任务，点击「全部任务」查看完整列表。</div>
      </section>
    </div>
  </div>
</div>
"""

PAGE_EXECUTION = r"""<div class="page" id="page-execution" hidden>
  <div class="page-head">
    <div><h1 class="page-title">实时执行</h1><p class="page-desc">各子代理的实时输出，本地模型负责降噪与摘要。</p></div>
    <div class="page-actions"><button class="btn">暂停全部</button><button class="btn btn--danger">终止沙箱</button></div>
  </div>
  <div class="tabs" data-tabs="exec">
    <div class="tab active" data-panel="term-recon">Recon</div>
    <div class="tab" data-panel="term-scan">Scan</div>
    <div class="tab" data-panel="term-fuzz">Fuzz</div>
    <div class="tab" data-panel="term-exploit">Exploit</div>
  </div>
  <div data-tab-group="exec">
    <div class="tab-panel" id="term-recon">
      <section class="section" style="margin:0">
        <div class="section-head"><span class="dot dot--busy"></span><span class="section-title">recon-agent-02</span><span class="section-sub">Qwen2.5-14B · 本地</span><div class="spacer"></div><span class="mono" style="font-size:10px;color:var(--muted)">task-0341 · 72%</span></div>
        <div style="padding:12px"><div class="term" style="max-height:260px">
          <div class="term-line t-dim">[09:42:11] 调度器 → 分配任务 task-0341 至 recon-agent-02</div>
          <div class="term-line t-cmd">$ nmap -sV -T4 --top-ports 1000 10.0.3.0/24 -oX /tmp/scan.xml</div>
          <div class="term-line t-dim">Starting Nmap 7.94 ( https://nmap.org )</div>
          <div class="term-line t-ok">[+] 10.0.3.44  22/tcp   open  ssh      OpenSSH 8.2p1</div>
          <div class="term-line t-ok">[+] 10.0.3.44  6379/tcp open  redis    Redis key-value store 6.0.9</div>
          <div class="term-line t-warn">[!] 10.0.3.44  6379/tcp 未授权访问 — 疑似配置缺陷</div>
          <div class="term-line t-info">[i] 本地模型摘要：2 个服务，1 个高危候选，已上报 Validator</div>
          <div class="term-line t-ok">[+] Validator 确认：Redis 未授权访问可利用，已生成 Finding</div>
          <div class="term-line t-cmd">$ <span class="t-cursor"></span></div>
        </div></div>
      </section>
    </div>
    <div class="tab-panel" id="term-scan" hidden>
      <section class="section" style="margin:0">
        <div class="section-head"><span class="dot dot--busy"></span><span class="section-title">scan-agent-03</span><span class="section-sub">Nuclei · 模板扫描</span></div>
        <div style="padding:12px"><div class="term" style="max-height:260px">
          <div class="term-line t-cmd">$ nuclei -u https://api.acme.com -severity critical,high -o /tmp/nuclei.txt</div>
          <div class="term-line t-dim">[INF] Templates loaded for current scan: 4823</div>
          <div class="term-line t-ok">[sqli] [http] [critical] https://api.acme.com/v1/search?q=1</div>
          <div class="term-line t-ok">[exposed-redis] [http] [high] https://api.acme.com/internal/redis</div>
          <div class="term-line t-info">[i] 本地模型摘要：2 条高危，去重后上报</div>
          <div class="term-line t-cmd">$ <span class="t-cursor"></span></div>
        </div></div>
      </section>
    </div>
    <div class="tab-panel" id="term-fuzz" hidden>
      <section class="section" style="margin:0">
        <div class="section-head"><span class="dot dot--on"></span><span class="section-title">fuzz-agent-01</span><span class="section-sub">ffuf · 目录爆破</span></div>
        <div style="padding:12px"><div class="term" style="max-height:260px">
          <div class="term-line t-cmd">$ ffuf -w /wordlists/common.txt -u https://files.acme.com/FUZZ</div>
          <div class="term-line t-ok">[200] admin      [Size: 4213]</div>
          <div class="term-line t-ok">[301] uploads    [Size: 0]</div>
          <div class="term-line t-ok">[403] backups    [Size: 289]</div>
          <div class="term-line t-info">[i] 本地模型摘要：发现 3 个敏感路径，已上报</div>
          <div class="term-line t-cmd">$ <span class="t-cursor"></span></div>
        </div></div>
      </section>
    </div>
    <div class="tab-panel" id="term-exploit" hidden>
      <section class="section" style="margin:0">
        <div class="section-head"><span class="dot dot--off"></span><span class="section-title">exploit-agent-01</span><span class="section-sub">等待审批放行</span></div>
        <div style="padding:12px"><div class="term" style="max-height:260px">
          <div class="term-line t-warn">[!] 任务 0342 等待人工审批，已挂起</div>
          <div class="term-line t-dim">[i] 审批通过后将执行：redis-cli -h 10.0.3.44 -p 6379 INFO keyspace</div>
          <div class="term-line t-cmd">$ <span class="t-cursor"></span></div>
        </div></div>
      </section>
    </div>
  </div>
</div>
"""

PAGE_FINDINGS = r"""<div class="page" id="page-findings" hidden>
  <div class="page-head">
    <div><h1 class="page-title">漏洞发现</h1><p class="page-desc">所有发现均经过 Validator 二次验证，误报率已降至 5% 以下。</p></div>
    <div class="page-actions"><button class="btn">导出 CSV</button><button class="btn btn--primary">生成报告</button></div>
  </div>
  <div class="toolbar">
    <input class="input" placeholder="搜索标题 / 目标…" style="width:220px" />
    <select class="select"><option>全部严重性</option><option>Critical</option><option>High</option><option>Medium</option><option>Low</option></select>
    <select class="select"><option>全部状态</option><option>已验证</option><option>待验证</option><option>误报</option></select>
    <div class="spacer"></div>
    <span class="mono" style="font-size:11px;color:var(--muted)">共 9 条</span>
  </div>
  <section class="section" style="margin:0">
    <table class="table">
      <thead><tr><th style="width:90px">严重性</th><th>标题</th><th style="width:180px">目标</th><th style="width:110px">状态</th><th style="width:70px">CVSS</th><th style="width:110px">来源工具</th></tr></thead>
      <tbody>
        <tr><td><span class="sev sev--crit">Critical</span></td><td>API 端点 SQL 注入</td><td class="mono">api.acme.com</td><td><span class="tag tag--verified">已验证</span></td><td class="mono">9.8</td><td class="mono">Nuclei</td></tr>
        <tr><td><span class="sev sev--crit">Critical</span></td><td>Redis 未授权访问</td><td class="mono">10.0.3.44:6379</td><td><span class="tag tag--pending">待验证</span></td><td class="mono">9.1</td><td class="mono">Nmap</td></tr>
        <tr><td><span class="sev sev--high">High</span></td><td>任意文件读取（路径穿越）</td><td class="mono">files.acme.com</td><td><span class="tag tag--verified">已验证</span></td><td class="mono">7.5</td><td class="mono">Burp</td></tr>
        <tr><td><span class="sev sev--high">High</span></td><td>SSH 弱口令</td><td class="mono">10.0.5.12:22</td><td><span class="tag tag--pending">待验证</span></td><td class="mono">7.2</td><td class="mono">Hydra</td></tr>
        <tr><td><span class="sev sev--high">High</span></td><td>备份文件可公开访问</td><td class="mono">files.acme.com</td><td><span class="tag tag--verified">已验证</span></td><td class="mono">7.0</td><td class="mono">ffuf</td></tr>
        <tr><td><span class="sev sev--med">Medium</span></td><td>TLS 证书过期</td><td class="mono">mail.acme.com</td><td><span class="tag tag--verified">已验证</span></td><td class="mono">5.3</td><td class="mono">Nuclei</td></tr>
        <tr><td><span class="sev sev--med">Medium</span></td><td>缺少安全响应头</td><td class="mono">api.acme.com</td><td><span class="tag tag--verified">已验证</span></td><td class="mono">4.3</td><td class="mono">Nuclei</td></tr>
        <tr><td><span class="sev sev--low">Low</span></td><td>服务器版本信息泄露</td><td class="mono">10.0.3.44</td><td><span class="tag tag--fp">误报</span></td><td class="mono">2.1</td><td class="mono">Nmap</td></tr>
        <tr><td><span class="sev sev--low">Low</span></td><td>目录列表启用</td><td class="mono">files.acme.com</td><td><span class="tag tag--verified">已验证</span></td><td class="mono">3.1</td><td class="mono">ffuf</td></tr>
      </tbody>
    </table>
  </section>
</div>
"""

PAGE_JS_ANALYSIS = r"""<div class="page" id="page-js-analysis" hidden>
  <div class="page-head">
    <div><h1 class="page-title">JS 分析 / API 绕过</h1><p class="page-desc">对目标站点 JS 做反混淆、接口提取与密钥扫描。</p></div>
    <div class="page-actions"><button class="btn">重新抓取</button><button class="btn btn--primary">+ 导入 JS 文件</button></div>
  </div>
  <div class="workbench">
    <section class="section" style="margin:0">
      <div class="section-head"><span class="section-title">JS 资源</span><div class="spacer"></div><span class="chip-mini">6 个</span></div>
      <div class="section-body" style="padding:9px">
        <div class="tree">
          <div class="tree-item active">app.min.js<span class="meta">248 KB</span></div>
          <div class="tree-item">vendor.js<span class="meta">412 KB</span></div>
          <div class="tree-item">chunk-auth.js<span class="meta">86 KB</span></div>
          <div class="tree-item">chunk-pay.js<span class="meta">52 KB</span></div>
          <div class="tree-item">runtime.js<span class="meta">18 KB</span></div>
          <div class="tree-item">inline-source.map<span class="meta">1.2 MB</span></div>
        </div>
      </div>
    </section>
    <section class="section" style="margin:0">
      <div class="section-head"><span class="section-title">app.min.js</span><span class="section-sub">反混淆后 · 12,480 行</span><div class="spacer"></div><button class="btn" style="height:26px;font-size:11px">美化</button><button class="btn" style="height:26px;font-size:11px">搜索</button></div>
      <div style="padding:12px">
        <div class="code-view">
          <div class="code-line"><span class="code-ln">1</span><span class="code-src"><span class="cmt">// 反混淆输出 · esbuild deobfuscate</span></span></div>
          <div class="code-line"><span class="code-ln">2</span><span class="code-src"><span class="kw">const</span> API_BASE = <span class="str">"https://api.acme.com/v2"</span>;</span></div>
          <div class="code-line"><span class="code-ln">3</span><span class="code-src"><span class="kw">const</span> SIGN_KEY = <span class="str">"a3f9c21e7b8d4a1f6e2c9b0d"</span>;</span></div>
          <div class="code-line hl"><span class="code-ln">4</span><span class="code-src"><span class="kw">function</span> sign(p) { <span class="kw">return</span> md5(p + SIGN_KEY); }</span></div>
          <div class="code-line"><span class="code-ln">5</span><span class="code-src"></span></div>
          <div class="code-line"><span class="code-ln">6</span><span class="code-src"><span class="kw">async function</span> getUser(uid) {</span></div>
          <div class="code-line"><span class="code-ln">7</span><span class="code-src">  <span class="kw">const</span> r = <span class="kw">await</span> fetch(<span class="str">`${API_BASE}/user/${uid}`</span>);</span></div>
          <div class="code-line hl"><span class="code-ln">8</span><span class="code-src">  <span class="kw">return</span> r.json(); <span class="cmt">// 未校验 uid 归属</span></span></div>
          <div class="code-line"><span class="code-ln">9</span><span class="code-src">}</span></div>
          <div class="code-line"><span class="code-ln">10</span><span class="code-src"></span></div>
          <div class="code-line"><span class="code-ln">11</span><span class="code-src"><span class="kw">async function</span> updateProfile(data) {</span></div>
          <div class="code-line"><span class="code-ln">12</span><span class="code-src">  <span class="kw">return</span> fetch(<span class="str">`${API_BASE}/user/profile`</span>, {</span></div>
          <div class="code-line"><span class="code-ln">13</span><span class="code-src">    method: <span class="str">"POST"</span>,</span></div>
          <div class="code-line"><span class="code-ln">14</span><span class="code-src">    headers: { <span class="str">"X-Sign"</span>: sign(JSON.stringify(data)) },</span></div>
          <div class="code-line"><span class="code-ln">15</span><span class="code-src">    body: JSON.stringify(data)</span></div>
          <div class="code-line"><span class="code-ln">16</span><span class="code-src">  });</span></div>
          <div class="code-line"><span class="code-ln">17</span><span class="code-src">}</span></div>
          <div class="code-line"><span class="code-ln">18</span><span class="code-src"></span></div>
          <div class="code-line"><span class="code-ln">19</span><span class="code-src"><span class="cmt">// 内部接口，未做权限校验</span></span></div>
          <div class="code-line hl"><span class="code-ln">20</span><span class="code-src"><span class="kw">const</span> ADMIN_API = <span class="str">"/admin/internal/export"</span>;</span></div>
        </div>
      </div>
    </section>
    <div class="wb-right" style="display:flex;flex-direction:column;gap:12px">
      <div class="card">
        <div class="card-head">敏感信息<div class="spacer"></div><span class="chip-mini chip-mini--warn">4 项</span></div>
        <div class="card-body" style="padding:11px">
          <div class="secret"><div class="secret-label">签名密钥 · 硬编码</div><div class="secret-val">SIGN_KEY = "a3f9c21e7b8d4a1f6e2c9b0d"</div><div class="secret-src">app.min.js:3</div></div>
          <div class="secret"><div class="secret-label">云存储 AK</div><div class="secret-val">AKIDa3f9c21e7b8d4a1f6e2c9b0d</div><div class="secret-src">chunk-pay.js:218</div></div>
          <div class="secret"><div class="secret-label">内网地址</div><div class="secret-val">http://10.0.3.44:8080/actuator</div><div class="secret-src">vendor.js:10422</div></div>
          <div class="secret"><div class="secret-label">测试账号</div><div class="secret-val">test_admin / Test@2025</div><div class="secret-src">chunk-auth.js:88</div></div>
        </div>
      </div>
      <div class="card">
        <div class="card-head">接口清单<div class="spacer"></div><span class="chip-mini">12 个</span></div>
        <div class="card-body" style="padding:11px">
          <div class="api-item"><div class="api-path">GET /v2/user/{uid}</div><div class="api-meta"><span>无鉴权</span><span>IDOR 候选</span></div></div>
          <div class="api-item"><div class="api-path">POST /v2/user/profile</div><div class="api-meta"><span>X-Sign 签名</span><span>算法: md5(p+key)</span></div></div>
          <div class="api-item"><div class="api-path">GET /admin/internal/export</div><div class="api-meta"><span>内部接口</span><span style="color:var(--high)">未授权候选</span></div></div>
        </div>
      </div>
      <div class="card">
        <div class="card-head">绕过建议<div class="spacer"></div><span class="chip-mini chip-mini--warn">DeepSeek</span></div>
        <div class="card-body" style="padding:11px">
          <div class="bypass-card">
            <div class="bypass-title">IDOR · 用户越权读取</div>
            <div class="bypass-desc">/v2/user/{uid} 未校验归属，尝试遍历 uid 读取他人资料。</div>
            <div class="bypass-actions"><button class="btn btn--primary">生成验证任务</button><button class="btn">查看详情</button></div>
          </div>
          <div class="bypass-card">
            <div class="bypass-title">签名算法复用</div>
            <div class="bypass-desc">SIGN_KEY 硬编码在前端，可离线复现 X-Sign 绕过参数校验。</div>
            <div class="bypass-actions"><button class="btn btn--primary">生成验证任务</button><button class="btn">查看详情</button></div>
          </div>
          <div class="bypass-card">
            <div class="bypass-title">内部接口未授权</div>
            <div class="bypass-desc">/admin/internal/export 未在路由守卫中注册，尝试无 token 访问。</div>
            <div class="bypass-actions"><button class="btn btn--primary">生成验证任务</button><button class="btn">查看详情</button></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
"""

PAGE_MINIAPP_ANALYSIS = r"""<div class="page" id="page-miniapp-analysis" hidden>
  <div class="page-head">
    <div><h1 class="page-title">小程序分析</h1><p class="page-desc">对 wxapkg 反编译产物做路由、API 与鉴权逻辑分析。</p></div>
    <div class="page-actions"><button class="btn">从设备拉取</button><button class="btn btn--primary">+ 导入 wxapkg</button></div>
  </div>
  <div class="workbench">
    <section class="section" style="margin:0">
      <div class="section-head"><span class="section-title">小程序包</span><div class="spacer"></div><span class="chip-mini">3 个</span></div>
      <div class="section-body" style="padding:9px">
        <div class="tree">
          <div class="tree-item active">acme-mall<span class="meta">v2.4.1</span></div>
          <div class="tree-children">
            <div class="tree-item">pages/<span class="meta">24</span></div>
            <div class="tree-item">components/<span class="meta">18</span></div>
            <div class="tree-item">app-service.js<span class="meta">620 KB</span></div>
            <div class="tree-item">app.json<span class="meta">4 KB</span></div>
          </div>
          <div class="tree-item">acme-pay<span class="meta">v1.8.0</span></div>
          <div class="tree-item">acme-crm<span class="meta">v0.9.2</span></div>
        </div>
      </div>
    </section>
    <section class="section" style="margin:0">
      <div class="section-head"><span class="section-title">app-service.js</span><span class="section-sub">反编译输出</span><div class="spacer"></div><button class="btn" style="height:26px;font-size:11px">美化</button></div>
      <div style="padding:12px">
        <div class="code-view">
          <div class="code-line"><span class="code-ln">1</span><span class="code-src"><span class="cmt">// 反编译输出 · wxappUnpacker</span></span></div>
          <div class="code-line"><span class="code-ln">2</span><span class="code-src"><span class="kw">const</span> baseUrl = <span class="str">"https://m.acme.com/api"</span>;</span></div>
          <div class="code-line"><span class="code-ln">3</span><span class="code-src"></span></div>
          <div class="code-line"><span class="code-ln">4</span><span class="code-src">App({</span></div>
          <div class="code-line"><span class="code-ln">5</span><span class="code-src">  onLaunch() {</span></div>
          <div class="code-line hl"><span class="code-ln">6</span><span class="code-src">    <span class="kw">const</span> token = wx.getStorageSync(<span class="str">"token"</span>);</span></div>
          <div class="code-line"><span class="code-ln">7</span><span class="code-src">    <span class="kw">this</span>.globalData = { token, baseUrl };</span></div>
          <div class="code-line"><span class="code-ln">8</span><span class="code-src">  }</span></div>
          <div class="code-line"><span class="code-ln">9</span><span class="code-src">});</span></div>
          <div class="code-line"><span class="code-ln">10</span><span class="code-src"></span></div>
          <div class="code-line"><span class="code-ln">11</span><span class="code-src"><span class="kw">function</span> request(path, data) {</span></div>
          <div class="code-line"><span class="code-ln">12</span><span class="code-src">  <span class="kw">return</span> wx.request({</span></div>
          <div class="code-line"><span class="code-ln">13</span><span class="code-src">    url: <span class="str">`${baseUrl}${path}`</span>,</span></div>
          <div class="code-line"><span class="code-ln">14</span><span class="code-src">    header: { <span class="str">"Authorization"</span>: wx.getStorageSync(<span class="str">"token"</span>) },</span></div>
          <div class="code-line"><span class="code-ln">15</span><span class="code-src">    data</span></div>
          <div class="code-line"><span class="code-ln">16</span><span class="code-src">  });</span></div>
          <div class="code-line"><span class="code-ln">17</span><span class="code-src">}</span></div>
          <div class="code-line"><span class="code-ln">18</span><span class="code-src"></span></div>
          <div class="code-line hl"><span class="code-ln">19</span><span class="code-src"><span class="cmt">// 管理端接口，仅前端做角色判断</span></span></div>
          <div class="code-line"><span class="code-ln">20</span><span class="code-src"><span class="kw">function</span> exportOrders() {</span></div>
          <div class="code-line"><span class="code-ln">21</span><span class="code-src">  <span class="kw">if</span> (wx.getStorageSync(<span class="str">"role"</span>) === <span class="str">"admin"</span>) {</span></div>
          <div class="code-line"><span class="code-ln">22</span><span class="code-src">    <span class="kw">return</span> request(<span class="str">"/admin/orders/export"</span>);</span></div>
          <div class="code-line"><span class="code-ln">23</span><span class="code-src">  }</span></div>
          <div class="code-line"><span class="code-ln">24</span><span class="code-src">}</span></div>
        </div>
      </div>
    </section>
    <div class="wb-right" style="display:flex;flex-direction:column;gap:12px">
      <div class="card">
        <div class="card-head">页面路由<div class="spacer"></div><span class="chip-mini">24 个</span></div>
        <div class="card-body" style="padding:11px">
          <div class="api-item"><div class="api-path">pages/user/profile</div><div class="api-meta"><span>需登录</span><span>含 uid 参数</span></div></div>
          <div class="api-item"><div class="api-path">pages/admin/orders</div><div class="api-meta"><span style="color:var(--high)">前端角色校验</span></div></div>
          <div class="api-item"><div class="api-path">pages/pay/checkout</div><div class="api-meta"><span>含金额参数</span></div></div>
        </div>
      </div>
      <div class="card">
        <div class="card-head">敏感信息<div class="spacer"></div><span class="chip-mini chip-mini--warn">2 项</span></div>
        <div class="card-body" style="padding:11px">
          <div class="secret"><div class="secret-label">API 基址</div><div class="secret-val">https://m.acme.com/api</div><div class="secret-src">app-service.js:2</div></div>
          <div class="secret"><div class="secret-label">内部接口路径</div><div class="secret-val">/admin/orders/export</div><div class="secret-src">app-service.js:22</div></div>
        </div>
      </div>
      <div class="card">
        <div class="card-head">绕过建议<div class="spacer"></div><span class="chip-mini chip-mini--warn">DeepSeek</span></div>
        <div class="card-body" style="padding:11px">
          <div class="bypass-card">
            <div class="bypass-title">前端角色绕过</div>
            <div class="bypass-desc">role 存在 Storage 中，可通过 devtools 改为 admin 后直接调用 exportOrders。</div>
            <div class="bypass-actions"><button class="btn btn--primary">生成验证任务</button><button class="btn">查看详情</button></div>
          </div>
          <div class="bypass-card">
            <div class="bypass-title">Token 越权</div>
            <div class="bypass-desc">Authorization 直接使用 Storage token，尝试低权账号调用高权接口。</div>
            <div class="bypass-actions"><button class="btn btn--primary">生成验证任务</button><button class="btn">查看详情</button></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
"""

PAGE_APP_ANALYSIS = r"""<div class="page" id="page-app-analysis" hidden>
  <div class="page-head">
    <div><h1 class="page-title">App 破解分析</h1><p class="page-desc">APK / IPA 反编译产物分析，含加固检测、SSL Pinning 检测与 Frida 脚本生成。</p></div>
    <div class="page-actions"><button class="btn">从设备拉取</button><button class="btn btn--primary">+ 导入 APK / IPA</button></div>
  </div>
  <div class="workbench">
    <section class="section" style="margin:0">
      <div class="section-head"><span class="section-title">应用包</span><div class="spacer"></div><span class="chip-mini">2 个</span></div>
      <div class="section-body" style="padding:9px">
        <div class="tree">
          <div class="tree-item active">acme-android.apk<span class="meta">v3.2.1</span></div>
          <div class="tree-children">
            <div class="tree-item">smali/<span class="meta">4,820</span></div>
            <div class="tree-item">res/</div>
            <div class="tree-item">lib/<span class="meta">arm64</span></div>
            <div class="tree-item">AndroidManifest.xml</div>
          </div>
          <div class="tree-item">acme-ios.ipa<span class="meta">v3.2.0</span></div>
        </div>
      </div>
    </section>
    <section class="section" style="margin:0">
      <div class="section-head"><span class="section-title">smali/com/acme/auth/LoginActivity.smali</span><div class="spacer"></div><button class="btn" style="height:26px;font-size:11px">生成 Frida 脚本</button></div>
      <div style="padding:12px">
        <div class="code-view">
          <div class="code-line"><span class="code-ln">1</span><span class="code-src"><span class="tag">.class</span> <span class="kw">public</span> Lcom/acme/auth/LoginActivity;</span></div>
          <div class="code-line"><span class="code-ln">2</span><span class="code-src"><span class="tag">.super</span> Landroidx/appcompat/app/AppCompatActivity;</span></div>
          <div class="code-line"><span class="code-ln">3</span><span class="code-src"></span></div>
          <div class="code-line"><span class="code-ln">4</span><span class="code-src"><span class="tag">.method</span> <span class="kw">private</span> checkRoot()Z</span></div>
          <div class="code-line hl"><span class="code-ln">5</span><span class="code-src">  <span class="cmt"># 检测 su / Magisk / Xposed</span></span></div>
          <div class="code-line"><span class="code-ln">6</span><span class="code-src">  <span class="kw">invoke-static</span> {p0}, Lcom/acme/sec/RootCheck;->isRooted()Z</span></div>
          <div class="code-line"><span class="code-ln">7</span><span class="code-src">  <span class="kw">move-result</span> v0</span></div>
          <div class="code-line"><span class="code-ln">8</span><span class="code-src">  <span class="kw">return</span> v0</span></div>
          <div class="code-line"><span class="code-ln">9</span><span class="code-src"><span class="tag">.end method</span></span></div>
          <div class="code-line"><span class="code-ln">10</span><span class="code-src"></span></div>
          <div class="code-line"><span class="code-ln">11</span><span class="code-src"><span class="tag">.method</span> <span class="kw">public</span> sign(Ljava/lang/String;)Ljava/lang/String;</span></div>
          <div class="code-line"><span class="code-ln">12</span><span class="code-src">  <span class="cmt"># 本地签名，密钥硬编码</span></span></div>
          <div class="code-line hl"><span class="code-ln">13</span><span class="code-src">  <span class="kw">const-string</span> v1, <span class="str">"k9X2mQ7pL4nR8sT1"</span></span></div>
          <div class="code-line"><span class="code-ln">14</span><span class="code-src">  <span class="kw">invoke-static</span> {p1, v1}, Lcom/acme/sec/MD5;->hash(...)Ljava/lang/String;</span></div>
          <div class="code-line"><span class="code-ln">15</span><span class="code-src">  <span class="kw">move-result-object</span> v0</span></div>
          <div class="code-line"><span class="code-ln">16</span><span class="code-src">  <span class="kw">return-object</span> v0</span></div>
          <div class="code-line"><span class="code-ln">17</span><span class="code-src"><span class="tag">.end method</span></span></div>
        </div>
      </div>
    </section>
    <div class="wb-right" style="display:flex;flex-direction:column;gap:12px">
      <div class="card">
        <div class="card-head">安全机制检测<div class="spacer"></div><span class="chip-mini chip-mini--warn">5 项</span></div>
        <div class="card-body" style="padding:11px">
          <div class="check-list">
            <div class="check-item"><div class="check-icon check-icon--warn">!</div><div class="check-body"><div class="check-title">加固检测</div><div class="check-desc">未检测到加固，可直接 jadx 反编译</div></div></div>
            <div class="check-item"><div class="check-icon check-icon--err">!</div><div class="check-body"><div class="check-title">SSL Pinning</div><div class="check-desc">OkHttp CertificatePinner 已启用</div></div></div>
            <div class="check-item"><div class="check-icon check-icon--warn">!</div><div class="check-body"><div class="check-title">Root 检测</div><div class="check-desc">RootCheck.isRooted()，可 Hook 绕过</div></div></div>
            <div class="check-item"><div class="check-icon check-icon--err">!</div><div class="check-body"><div class="check-title">硬编码密钥</div><div class="check-desc">LoginActivity:13 · k9X2mQ7pL4nR8sT1</div></div></div>
            <div class="check-item"><div class="check-icon check-icon--ok">✓</div><div class="check-body"><div class="check-title">反调试</div><div class="check-desc">未检测到 ptrace 保护</div></div></div>
          </div>
        </div>
      </div>
      <div class="card">
        <div class="card-head">Frida Hook 脚本<div class="spacer"></div><span class="chip-mini chip-mini--ok">已生成</span></div>
        <div class="card-body" style="padding:11px">
          <div class="req-body" style="max-height:180px;color:var(--accent)">Java.perform(function () {
  var RootCheck = Java.use('com.acme.sec.RootCheck');
  RootCheck.isRooted.implementation = function () {
    console.log('[+] Root bypass');
    return false;
  };

  var Login = Java.use('com.acme.auth.LoginActivity');
  Login.sign.implementation = function (s) {
    var r = this.sign(s);
    console.log('[+] sign(' + s + ') = ' + r);
    return r;
  };
});</div>
          <div class="bypass-actions" style="margin-top:10px">
            <button class="btn btn--primary" style="flex:1;justify-content:center">下发到设备</button>
            <button class="btn">复制</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
"""

PAGE_TRAFFIC_ANALYSIS = r"""<div class="page" id="page-traffic-analysis" hidden>
  <div class="page-head">
    <div><h1 class="page-title">抓包分析</h1><p class="page-desc">HTTP / WebSocket 流量实时捕获与重放，敏感字段自动标注，所有重放走审批。</p></div>
    <div class="page-actions"><button class="btn">导入 HAR</button><button class="btn btn--danger">停止抓包</button></div>
  </div>
  <div class="toolbar">
    <span class="dot dot--busy"></span>
    <span style="font-size:12px">代理运行中 · 127.0.0.1:8080</span>
    <div class="spacer" style="flex:1"></div>
    <select class="select"><option>全部协议</option><option>HTTP</option><option>WebSocket</option></select>
    <select class="select"><option>全部状态</option><option>2xx</option><option>3xx</option><option>4xx</option><option>5xx</option></select>
    <input class="input" placeholder="过滤 URL / Host…" style="width:200px" />
  </div>
  <div class="workbench" style="grid-template-columns:minmax(0,1.4fr) minmax(0,1fr)">
    <section class="section" style="margin:0">
      <div class="section-head"><span class="section-title">流量列表</span><div class="spacer"></div><span class="chip-mini">248 条</span></div>
      <div class="packet-head" style="padding-top:11px"><span>时间</span><span>方法</span><span>URL</span><span>状态</span><span>大小</span><span>来源</span></div>
      <div style="max-height:520px;overflow-y:auto">
        <div class="packet-row active"><span class="mono" style="font-size:10.5px">09:44:12</span><span class="method method--get">GET</span><span class="packet-url">/v2/user/1001</span><span class="status status--2xx">200</span><span class="mono" style="font-size:10.5px">1.2 KB</span><span class="mono" style="font-size:10.5px">android</span></div>
        <div class="packet-row"><span class="mono" style="font-size:10.5px">09:44:08</span><span class="method method--post">POST</span><span class="packet-url">/v2/user/profile</span><span class="status status--2xx">200</span><span class="mono" style="font-size:10.5px">2.4 KB</span><span class="mono" style="font-size:10.5px">miniapp</span></div>
        <div class="packet-row"><span class="mono" style="font-size:10.5px">09:43:55</span><span class="method method--get">GET</span><span class="packet-url">/admin/internal/export</span><span class="status status--4xx">403</span><span class="mono" style="font-size:10.5px">420 B</span><span class="mono" style="font-size:10.5px">browser</span></div>
        <div class="packet-row"><span class="mono" style="font-size:10.5px">09:43:40</span><span class="method method--post">POST</span><span class="packet-url">/v2/pay/checkout</span><span class="status status--2xx">200</span><span class="mono" style="font-size:10.5px">3.1 KB</span><span class="mono" style="font-size:10.5px">android</span></div>
        <div class="packet-row"><span class="mono" style="font-size:10.5px">09:43:22</span><span class="method method--ws">WS</span><span class="packet-url">/ws/notification</span><span class="status status--2xx">101</span><span class="mono" style="font-size:10.5px">—</span><span class="mono" style="font-size:10.5px">miniapp</span></div>
        <div class="packet-row"><span class="mono" style="font-size:10.5px">09:43:10</span><span class="method method--get">GET</span><span class="packet-url">/v2/order/list?uid=1002</span><span class="status status--2xx">200</span><span class="mono" style="font-size:10.5px">8.4 KB</span><span class="mono" style="font-size:10.5px">android</span></div>
        <div class="packet-row"><span class="mono" style="font-size:10.5px">09:42:58</span><span class="method method--post">POST</span><span class="packet-url">/v2/auth/login</span><span class="status status--2xx">200</span><span class="mono" style="font-size:10.5px">1.8 KB</span><span class="mono" style="font-size:10.5px">browser</span></div>
      </div>
    </section>
    <div style="display:flex;flex-direction:column;gap:12px">
      <div class="card">
        <div class="card-head"><span class="method method--get" style="padding:2px 8px">GET</span><span class="mono" style="font-size:11px">https://api.acme.com/v2/user/1001</span><div class="spacer"></div><span class="status status--2xx" style="font-size:12px">200 OK</span></div>
        <div class="card-body">
          <div class="req-block"><div class="req-title">请求头<div class="spacer"></div><span class="chip-mini">6</span></div><div class="req-body">Host: api.acme.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
X-Sign: 3f9a2c1e7b8d4a1f6e2c9b0d8a7f6e5d
User-Agent: AcmeApp/3.2.1 (Android 14)</div></div>
          <div class="req-block"><div class="req-title">响应体<div class="spacer"></div><button class="btn" style="height:24px;font-size:10.5px">格式化</button></div><div class="req-body" style="color:var(--text-dim)">{
  "uid": 1001,
  "nickname": "alice",
  "phone": "138****2233",
  "email": "alice@acme.com",
  "balance": 12800,
  "role": "user"
}</div></div>
          <div class="bypass-actions">
            <button class="btn btn--primary" style="flex:1;justify-content:center">重放</button>
            <button class="btn" style="flex:1;justify-content:center">修改并重放</button>
            <button class="btn" style="flex:1;justify-content:center">生成 PoC</button>
          </div>
        </div>
      </div>
      <div class="card">
        <div class="card-head">敏感信息<div class="spacer"></div><span class="chip-mini chip-mini--warn">3 项</span></div>
        <div class="card-body" style="padding:11px">
          <div class="secret"><div class="secret-label">Bearer Token</div><div class="secret-val">eyJhbGciOiJIUzI1NiIs...</div><div class="secret-src">请求头 · Authorization</div></div>
          <div class="secret"><div class="secret-label">用户余额</div><div class="secret-val">balance: 12800</div><div class="secret-src">响应体 · /v2/user/1001</div></div>
          <div class="secret"><div class="secret-label">签名头</div><div class="secret-val">X-Sign: 3f9a2c1e7b8d4a1f...</div><div class="secret-src">请求头 · X-Sign</div></div>
        </div>
      </div>
      <div class="card">
        <div class="card-head">分析建议<div class="spacer"></div><span class="chip-mini chip-mini--warn">DeepSeek</span></div>
        <div class="card-body" style="padding:11px">
          <div class="bypass-card">
            <div class="bypass-title">IDOR · 用户资料越权</div>
            <div class="bypass-desc">/v2/user/{uid} 的 uid 为用户可控参数，尝试替换为其他 uid 读取资料。</div>
            <div class="bypass-actions"><button class="btn btn--primary">生成验证任务</button></div>
          </div>
          <div class="bypass-card">
            <div class="bypass-title">参数污染</div>
            <div class="bypass-desc">/v2/order/list 同时存在 uid 与 token 中的 uid，尝试不一致触发越权。</div>
            <div class="bypass-actions"><button class="btn btn--primary">生成验证任务</button></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
"""

PAGE_MODELS = r"""<div class="page" id="page-models" hidden>
  <div class="page-head">
    <div><h1 class="page-title">模型管理</h1><p class="page-desc">云端 DeepSeek 负责规划与验证，本地模型负责高频降噪与子任务执行。</p></div>
    <div class="page-actions"><button class="btn">连通性测试</button><button class="btn btn--primary">+ 添加模型</button></div>
  </div>
  <div class="grid-2" style="margin-bottom:16px">
    <div class="model-card">
      <div class="model-card-head"><span class="dot dot--on"></span><div><div class="model-card-name">DeepSeek-Reasoner</div><div class="model-card-sub">云端 · 主模型</div></div><div class="spacer" style="flex:1"></div><span class="tag tag--done">在线</span></div>
      <div class="kv"><span class="kv-key">端点</span><span class="kv-val">api.deepseek.com</span></div>
      <div class="kv"><span class="kv-key">平均延迟</span><span class="kv-val">320 ms</span></div>
      <div class="kv"><span class="kv-key">本次成本</span><span class="kv-val">$0.42 / $5.00</span></div>
      <div class="bar"><div class="bar-fill" style="width:8.4%"></div></div>
      <div class="form-row" style="padding-bottom:0"><div class="form-label">降级时自动切换本地</div><div class="toggle on" onclick="this.classList.toggle('on')"></div></div>
    </div>
    <div class="model-card">
      <div class="model-card-head"><span class="dot dot--busy"></span><div><div class="model-card-name">Qwen2.5-14B-Instruct</div><div class="model-card-sub">本地 · QLoRA 微调</div></div><div class="spacer" style="flex:1"></div><span class="tag tag--running">推理中</span></div>
      <div class="kv"><span class="kv-key">推理引擎</span><span class="kv-val">vLLM</span></div>
      <div class="kv"><span class="kv-key">量化</span><span class="kv-val">4-bit (QLoRA)</span></div>
      <div class="kv"><span class="kv-key">GPU 占用</span><span class="kv-val">68% · 18.4 GB</span></div>
      <div class="bar"><div class="bar-fill" style="width:68%"></div></div>
      <div class="form-row" style="padding-bottom:0"><div class="form-label">启用 LoRA 适配器</div><div class="toggle on" onclick="this.classList.toggle('on')"></div></div>
    </div>
  </div>
  <section class="section">
    <div class="section-head"><span class="section-title">本地模型集群</span><span class="section-sub">Ollama / vLLM 端点</span></div>
    <table class="table">
      <thead><tr><th>模型</th><th style="width:110px">参数量</th><th style="width:120px">量化</th><th style="width:130px">GPU</th><th style="width:110px">状态</th><th style="width:80px">启用</th></tr></thead>
      <tbody>
        <tr><td>Qwen2.5-14B-Instruct</td><td class="mono">14B</td><td class="mono">4-bit</td><td class="mono">68% · 18.4GB</td><td><span class="tag tag--running">运行中</span></td><td><div class="toggle on" onclick="this.classList.toggle('on')"></div></td></tr>
        <tr><td>Qwen2.5-7B-Instruct</td><td class="mono">7B</td><td class="mono">4-bit</td><td class="mono">—</td><td><span class="tag tag--queued">待命</span></td><td><div class="toggle on" onclick="this.classList.toggle('on')"></div></td></tr>
        <tr><td>Llama-3.1-8B-Instruct</td><td class="mono">8B</td><td class="mono">4-bit</td><td class="mono">—</td><td><span class="tag tag--queued">待命</span></td><td><div class="toggle" onclick="this.classList.toggle('on')"></div></td></tr>
      </tbody>
    </table>
  </section>
  <section class="section">
    <div class="section-head"><span class="section-title">路由策略</span><span class="section-sub">决定任务走云端还是本地</span></div>
    <table class="table">
      <thead><tr><th>任务类型</th><th style="width:200px">路由目标</th><th style="width:120px">优先级</th></tr></thead>
      <tbody>
        <tr><td>攻击路径规划</td><td class="mono" style="color:var(--accent)">DeepSeek-Reasoner</td><td>高</td></tr>
        <tr><td>结果验证 / 去误报</td><td class="mono" style="color:var(--accent)">DeepSeek-Reasoner</td><td>高</td></tr>
        <tr><td>工具输出降噪摘要</td><td class="mono">Qwen2.5-14B (本地)</td><td>中</td></tr>
        <tr><td>Payload 初筛</td><td class="mono">Qwen2.5-14B (本地)</td><td>中</td></tr>
        <tr><td>日志实时分析</td><td class="mono">Qwen2.5-7B (本地)</td><td>低</td></tr>
      </tbody>
    </table>
  </section>
</div>
"""

PAGE_TOOLS = r"""<div class="page" id="page-tools" hidden>
  <div class="page-head">
    <div><h1 class="page-title">工具管理</h1><p class="page-desc">所有 MCP 工具端点均需签名校验，异常工具可一键禁用。</p></div>
    <div class="page-actions"><button class="btn">重新加载 MCP</button><button class="btn btn--primary">+ 注册工具</button></div>
  </div>
  <section class="section" style="margin:0">
    <table class="table">
      <thead><tr><th>工具端点</th><th style="width:130px">封装工具</th><th style="width:120px">权限</th><th style="width:130px">签名校验</th><th style="width:160px">最近调用</th><th style="width:80px">启用</th></tr></thead>
      <tbody>
        <tr><td>kali-mcp-server</td><td class="mono">Nmap, Hydra</td><td><span class="tag tag--pending">扫描</span></td><td><span class="tag tag--verified">已校验</span></td><td class="mono">09:42:11</td><td><div class="toggle on" onclick="this.classList.toggle('on')"></div></td></tr>
        <tr><td>burp-mcp</td><td class="mono">Burp Suite</td><td><span class="tag tag--blocked">利用</span></td><td><span class="tag tag--verified">已校验</span></td><td class="mono">09:38:44</td><td><div class="toggle on" onclick="this.classList.toggle('on')"></div></td></tr>
        <tr><td>nuclei-mcp</td><td class="mono">Nuclei</td><td><span class="tag tag--pending">扫描</span></td><td><span class="tag tag--verified">已校验</span></td><td class="mono">09:41:02</td><td><div class="toggle on" onclick="this.classList.toggle('on')"></div></td></tr>
        <tr><td>playwright-mcp</td><td class="mono">Chromium</td><td><span class="tag tag--pending">只读</span></td><td><span class="tag tag--verified">已校验</span></td><td class="mono">09:35:20</td><td><div class="toggle on" onclick="this.classList.toggle('on')"></div></td></tr>
        <tr><td>ffuf-mcp</td><td class="mono">ffuf, wfuzz</td><td><span class="tag tag--pending">扫描</span></td><td><span class="tag tag--verified">已校验</span></td><td class="mono">09:40:18</td><td><div class="toggle on" onclick="this.classList.toggle('on')"></div></td></tr>
        <tr><td>sqlmap-mcp</td><td class="mono">SQLMap</td><td><span class="tag tag--blocked">利用</span></td><td><span class="tag tag--pending">待校验</span></td><td class="mono">—</td><td><div class="toggle" onclick="this.classList.toggle('on')"></div></td></tr>
        <tr><td>metasploit-mcp</td><td class="mono">Metasploit</td><td><span class="tag tag--blocked">后渗透</span></td><td><span class="tag tag--verified">已校验</span></td><td class="mono">—</td><td><div class="toggle" onclick="this.classList.toggle('on')"></div></td></tr>
        <tr><td>unknown-mcp-server</td><td class="mono">—</td><td><span class="tag tag--fp">未知</span></td><td><span class="tag tag--fp">校验失败</span></td><td class="mono">—</td><td><div class="toggle" onclick="this.classList.toggle('on')"></div></td></tr>
      </tbody>
    </table>
  </section>
</div>
"""

PAGE_SKILLS = r"""<div class="page" id="page-skills" hidden>
  <div class="page-head">
    <div><h1 class="page-title">Skill 管理</h1><p class="page-desc">Skill 是封装了工具调用序列与推理模板的能力包，由 Planner 按阶段自动挂载。</p></div>
    <div class="page-actions">
      <button class="btn"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 3v6h-6"/></svg>重新扫描</button>
      <button class="btn btn--primary" onclick="openSkillImport()"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg>导入 Skill</button>
    </div>
  </div>
  <div class="toolbar">
    <input class="input" placeholder="搜索 Skill 名称 / 标签…" style="width:240px" />
    <select class="select"><option>全部风险等级</option><option>Critical</option><option>High</option><option>Medium</option><option>Low</option></select>
    <select class="select"><option>全部来源</option><option>官方仓库</option><option>社区</option><option>本地导入</option></select>
    <div class="spacer"></div>
    <span class="mono" style="font-size:11px;color:var(--muted)">14 个 Skill · 11 已启用</span>
  </div>
  <div class="skill-grid">
    <div class="skill-card">
      <div class="skill-top"><div class="skill-icon">🎯</div><div style="flex:1;min-width:0"><div class="skill-name">sql-injection-probe <span class="skill-ver">v1.2.0</span></div><div class="skill-author">security-team · 官方仓库</div></div></div>
      <div class="skill-desc">Web 应用 SQL 注入检测与验证，覆盖 OWASP A03，支持盲注与时间盲注确认。</div>
      <div class="skill-tags"><span class="skill-tag">web</span><span class="skill-tag">sqli</span><span class="skill-tag">T1190</span></div>
      <div class="skill-foot"><span class="skill-stat"><span class="sev sev--high" style="font-size:10px">High</span></span><span class="skill-stat">3 工具</span><span class="skill-stat">42 次</span><div class="toggle on" onclick="event.stopPropagation();this.classList.toggle('on')"></div></div>
    </div>
    <div class="skill-card">
      <div class="skill-top"><div class="skill-icon">🔍</div><div style="flex:1;min-width:0"><div class="skill-name">subdomain-enum <span class="skill-ver">v2.0.1</span></div><div class="skill-author">recon-lab · 官方仓库</div></div></div>
      <div class="skill-desc">被动 + 主动子域枚举，整合证书透明度日志、DNS 字典与搜索引擎结果。</div>
      <div class="skill-tags"><span class="skill-tag">recon</span><span class="skill-tag">dns</span><span class="skill-tag">T1590</span></div>
      <div class="skill-foot"><span class="skill-stat"><span class="sev sev--low" style="font-size:10px">Low</span></span><span class="skill-stat">2 工具</span><span class="skill-stat">128 次</span><div class="toggle on" onclick="event.stopPropagation();this.classList.toggle('on')"></div></div>
    </div>
    <div class="skill-card">
      <div class="skill-top"><div class="skill-icon">⚡</div><div style="flex:1;min-width:0"><div class="skill-name">redis-unauth-check <span class="skill-ver">v1.0.3</span></div><div class="skill-author">community · 社区</div></div></div>
      <div class="skill-desc">Redis 未授权访问检测，读取 keyspace 信息并评估数据敏感度，不含写入操作。</div>
      <div class="skill-tags"><span class="skill-tag">redis</span><span class="skill-tag">exposure</span><span class="skill-tag">T1190</span></div>
      <div class="skill-foot"><span class="skill-stat"><span class="sev sev--med" style="font-size:10px">Medium</span></span><span class="skill-stat">1 工具</span><span class="skill-stat">17 次</span><div class="toggle on" onclick="event.stopPropagation();this.classList.toggle('on')"></div></div>
    </div>
    <div class="skill-card">
      <div class="skill-top"><div class="skill-icon">🔑</div><div style="flex:1;min-width:0"><div class="skill-name">ssh-brute <span class="skill-ver">v1.4.0</span></div><div class="skill-author">security-team · 官方仓库</div></div></div>
      <div class="skill-desc">SSH 弱口令检测，支持字典分级与速率限制，所有执行均需人工审批。</div>
      <div class="skill-tags"><span class="skill-tag">ssh</span><span class="skill-tag">brute</span><span class="skill-tag">T1110</span></div>
      <div class="skill-foot"><span class="skill-stat"><span class="sev sev--high" style="font-size:10px">High</span></span><span class="skill-stat">1 工具</span><span class="skill-stat">9 次</span><div class="toggle on" onclick="event.stopPropagation();this.classList.toggle('on')"></div></div>
    </div>
    <div class="skill-card">
      <div class="skill-top"><div class="skill-icon">🛡️</div><div style="flex:1;min-width:0"><div class="skill-name">tls-audit <span class="skill-ver">v1.1.2</span></div><div class="skill-author">community · 社区</div></div></div>
      <div class="skill-desc">TLS/SSL 配置审计，检测协议版本、加密套件、证书链与常见配置缺陷。</div>
      <div class="skill-tags"><span class="skill-tag">tls</span><span class="skill-tag">audit</span></div>
      <div class="skill-foot"><span class="skill-stat"><span class="sev sev--low" style="font-size:10px">Low</span></span><span class="skill-stat">2 工具</span><span class="skill-stat">64 次</span><div class="toggle on" onclick="event.stopPropagation();this.classList.toggle('on')"></div></div>
    </div>
    <div class="skill-card">
      <div class="skill-top"><div class="skill-icon">📡</div><div style="flex:1;min-width:0"><div class="skill-name">api-fuzz <span class="skill-ver">v0.9.4</span></div><div class="skill-author">local-import · 本地导入</div></div></div>
      <div class="skill-desc">REST/GraphQL API 参数模糊测试，自动识别参数类型并生成边界值载荷。</div>
      <div class="skill-tags"><span class="skill-tag">api</span><span class="skill-tag">fuzz</span><span class="skill-tag">graphql</span></div>
      <div class="skill-foot"><span class="skill-stat"><span class="sev sev--med" style="font-size:10px">Medium</span></span><span class="skill-stat">2 工具</span><span class="skill-stat">3 次</span><div class="toggle on" onclick="event.stopPropagation();this.classList.toggle('on')"></div></div>
    </div>
    <div class="skill-card">
      <div class="skill-top"><div class="skill-icon">⬆️</div><div style="flex:1;min-width:0"><div class="skill-name">privesc-linux <span class="skill-ver">v1.0.0</span></div><div class="skill-author">local-import · 本地导入</div></div></div>
      <div class="skill-desc">Linux 本地提权路径检查，枚举 SUID、sudo 配置、计划任务与内核版本。</div>
      <div class="skill-tags"><span class="skill-tag">linux</span><span class="skill-tag">privesc</span><span class="skill-tag">T1068</span></div>
      <div class="skill-foot"><span class="skill-stat"><span class="sev sev--crit" style="font-size:10px">Critical</span></span><span class="skill-stat">1 工具</span><span class="skill-stat">0 次</span><div class="toggle" onclick="event.stopPropagation();this.classList.toggle('on')"></div></div>
    </div>
    <div class="skill-card">
      <div class="skill-top"><div class="skill-icon">📦</div><div style="flex:1;min-width:0"><div class="skill-name">smb-enum <span class="skill-ver">v1.3.1</span></div><div class="skill-author">community · 社区</div></div></div>
      <div class="skill-desc">SMB 共享枚举与会话信息收集，识别匿名访问与可写共享。</div>
      <div class="skill-tags"><span class="skill-tag">smb</span><span class="skill-tag">enum</span><span class="skill-tag">T1135</span></div>
      <div class="skill-foot"><span class="skill-stat"><span class="sev sev--low" style="font-size:10px">Low</span></span><span class="skill-stat">1 工具</span><span class="skill-stat">21 次</span><div class="toggle on" onclick="event.stopPropagation();this.classList.toggle('on')"></div></div>
    </div>
  </div>
</div>
"""

PAGE_AUDIT = r"""<div class="page" id="page-audit" hidden>
  <div class="page-head">
    <div><h1 class="page-title">审计日志</h1><p class="page-desc">所有操作均写入哈希链日志，只读展示，可导出 JSON / CSV。</p></div>
    <div class="page-actions"><button class="btn">导出 CSV</button><button class="btn">导出 JSON</button></div>
  </div>
  <div class="toolbar">
    <input class="input" placeholder="搜索操作人 / 目标…" style="width:220px" />
    <select class="select"><option>全部动作</option><option>批准</option><option>拒绝</option><option>执行</option><option>停止</option></select>
    <select class="select"><option>全部风险</option><option>Critical</option><option>High</option><option>Medium</option><option>Low</option></select>
    <div class="spacer"></div>
    <span class="mono" style="font-size:11px;color:var(--muted)">哈希链完整</span>
  </div>
  <section class="section" style="margin:0">
    <table class="table">
      <thead><tr><th style="width:150px">时间</th><th style="width:110px">操作人</th><th style="width:110px">动作</th><th>目标</th><th style="width:100px">风险</th><th style="width:130px">哈希</th></tr></thead>
      <tbody>
        <tr><td class="mono">09:43:02</td><td>operator</td><td><span class="tag tag--done">执行</span></td><td class="mono">task-0341 · nmap</td><td><span class="sev sev--low">Low</span></td><td class="mono">a3f9…c21e</td></tr>
        <tr><td class="mono">09:42:55</td><td>approver</td><td><span class="tag tag--verified">批准</span></td><td class="mono">task-0342 · redis</td><td><span class="sev sev--crit">Critical</span></td><td class="mono">7b21…9d4a</td></tr>
        <tr><td class="mono">09:41:30</td><td>operator</td><td><span class="tag tag--fp">拒绝</span></td><td class="mono">task-0339 · metasploit</td><td><span class="sev sev--high">High</span></td><td class="mono">e08c…41f2</td></tr>
        <tr><td class="mono">09:40:18</td><td>system</td><td><span class="tag tag--running">执行</span></td><td class="mono">task-0344 · nuclei</td><td><span class="sev sev--low">Low</span></td><td class="mono">2d77…b8e0</td></tr>
        <tr><td class="mono">09:38:44</td><td>operator</td><td><span class="tag tag--done">执行</span></td><td class="mono">task-0345 · ffuf</td><td><span class="sev sev--med">Medium</span></td><td class="mono">9c14…6a3b</td></tr>
        <tr><td class="mono">09:36:12</td><td>admin</td><td><span class="tag tag--pending">配置</span></td><td class="mono">model · deepseek-reasoner</td><td><span class="sev sev--info">Info</span></td><td class="mono">54ae…f09d</td></tr>
        <tr><td class="mono">09:35:00</td><td>operator</td><td><span class="tag tag--running">停止</span></td><td class="mono">sandbox · kali-02</td><td><span class="sev sev--med">Medium</span></td><td class="mono">c6b3…2e71</td></tr>
      </tbody>
    </table>
  </section>
</div>
"""

PAGE_REPORTS = r"""<div class="page" id="page-reports" hidden>
  <div class="page-head">
    <div><h1 class="page-title">报告</h1><p class="page-desc">选择发现与证据，生成 PDF / JSON / SARIF 格式报告。</p></div>
    <div class="page-actions"><button class="btn btn--primary">+ 生成新报告</button></div>
  </div>
  <div class="grid-2" style="margin-bottom:16px">
    <section class="section" style="margin:0">
      <div class="section-head"><span class="section-title">生成配置</span></div>
      <div class="section-body">
        <div class="form-row"><div class="form-label">报告格式</div><select class="select"><option>PDF</option><option>JSON</option><option>SARIF</option></select></div>
        <div class="form-row"><div class="form-label">包含误报</div><div class="toggle" onclick="this.classList.toggle('on')"></div></div>
        <div class="form-row"><div class="form-label">附加证据截图</div><div class="toggle on" onclick="this.classList.toggle('on')"></div></div>
        <div class="form-row"><div class="form-label">添加水印与签名</div><div class="toggle on" onclick="this.classList.toggle('on')"></div></div>
        <div class="form-row"><div class="form-label">修复建议</div><div class="toggle on" onclick="this.classList.toggle('on')"></div></div>
      </div>
    </section>
    <section class="section" style="margin:0">
      <div class="section-head"><span class="section-title">报告预览</span></div>
      <div class="section-body">
        <div class="kv"><span class="kv-key">Engagement</span><span class="kv-val">ENG-2041</span></div>
        <div class="kv"><span class="kv-key">发现总数</span><span class="kv-val">9</span></div>
        <div class="kv"><span class="kv-key">Critical / High</span><span class="kv-val" style="color:var(--crit)">2 / 3</span></div>
        <div class="kv"><span class="kv-key">攻击路径</span><span class="kv-val">6 阶段</span></div>
        <div class="kv"><span class="kv-key">证据文件</span><span class="kv-val">14 项</span></div>
        <div class="kv"><span class="kv-key">预计页数</span><span class="kv-val">28 页</span></div>
      </div>
    </section>
  </div>
  <section class="section" style="margin:0">
    <div class="section-head"><span class="section-title">历史报告</span><span class="section-sub">最近 3 份</span></div>
    <div>
      <div class="report-item">
        <div class="report-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></svg></div>
        <div style="flex:1;min-width:0"><div style="font-size:12.5px;font-weight:600">ENG-2041 中期报告 · 2026-09-23</div><div class="mono" style="font-size:11px;color:var(--muted);margin-top:2px">9 发现 · 2 Critical · PDF · 4.2 MB</div></div>
        <span class="tag tag--done">已生成</span><button class="btn" style="height:28px;font-size:11px">下载</button>
      </div>
      <div class="report-item">
        <div class="report-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></svg></div>
        <div style="flex:1;min-width:0"><div style="font-size:12.5px;font-weight:600">ENG-2041 侦察阶段报告 · 2026-09-23</div><div class="mono" style="font-size:11px;color:var(--muted);margin-top:2px">12 资产 · 扫描摘要 · JSON · 820 KB</div></div>
        <span class="tag tag--done">已生成</span><button class="btn" style="height:28px;font-size:11px">下载</button>
      </div>
      <div class="report-item">
        <div class="report-icon" style="color:var(--muted)"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></div>
        <div style="flex:1;min-width:0"><div style="font-size:12.5px;font-weight:600">ENG-2041 最终报告 · 生成中</div><div class="mono" style="font-size:11px;color:var(--muted);margin-top:2px">等待所有阶段完成…</div></div>
        <span class="tag tag--running">生成中</span><button class="btn" style="height:28px;font-size:11px" disabled>下载</button>
      </div>
    </div>
  </section>
</div>
"""

ASIDE = r"""<aside class="aside">
  <div class="approve">
    <div class="approve-title">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 9v4M12 17h.01"/><path d="M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/></svg>
      需要审批
    </div>
    <div class="approve-desc">利用类操作需要人工放行。该命令将对目标发起认证绕过尝试。</div>
    <div class="approve-cmd">hydra -l admin -P /wordlists/top1k.txt 10.0.5.12 ssh</div>
    <div class="approve-actions"><button class="btn btn--danger">拒绝</button><button class="btn btn--primary">批准执行</button></div>
  </div>
  <div class="card">
    <div class="card-head">当前任务<div class="spacer"></div><span class="dot dot--busy"></span></div>
    <div class="card-body">
      <div class="kv"><span class="kv-key">任务 ID</span><span class="kv-val">task-0341</span></div>
      <div class="kv"><span class="kv-key">执行代理</span><span class="kv-val">recon-agent-02</span></div>
      <div class="kv"><span class="kv-key">模型</span><span class="kv-val">Qwen2.5-14B</span></div>
      <div class="kv"><span class="kv-key">工具</span><span class="kv-val">nmap</span></div>
      <div class="kv"><span class="kv-key">开始时间</span><span class="kv-val">09:42:11</span></div>
      <div class="kv"><span class="kv-key">风险等级</span><span class="kv-val" style="color:var(--accent)">低</span></div>
      <div style="margin-top:10px">
        <div style="display:flex;justify-content:space-between;font-size:11px;color:var(--muted)"><span>执行进度</span><span class="mono">72%</span></div>
        <div class="bar"><div class="bar-fill" style="width:72%"></div></div>
      </div>
    </div>
  </div>
  <div class="card">
    <div class="card-head">模型调用<div class="spacer"></div><span class="mono" style="font-size:10px;color:var(--muted)">近 10 分钟</span></div>
    <div class="card-body" style="padding-top:4px;padding-bottom:4px">
      <div class="call"><span class="dot dot--on"></span><div class="call-body"><div class="call-name">deepseek-reasoner</div><div class="call-meta">Planner · 1,240 tok · $0.004</div></div><span class="mono" style="color:var(--muted);font-size:10px">320ms</span></div>
      <div class="call"><span class="dot dot--busy"></span><div class="call-body"><div class="call-name">qwen2.5-14b-local</div><div class="call-meta">Recon 摘要 · 860 tok · $0</div></div><span class="mono" style="color:var(--muted);font-size:10px">1.4s</span></div>
      <div class="call"><span class="dot dot--on"></span><div class="call-body"><div class="call-name">deepseek-reasoner</div><div class="call-meta">Validator · 2,010 tok · $0.007</div></div><span class="mono" style="color:var(--muted);font-size:10px">2.1s</span></div>
    </div>
  </div>
  <div class="card">
    <div class="card-head">运行环境</div>
    <div class="card-body">
      <div class="kv"><span class="kv-key">沙箱容器</span><span class="kv-val">kali-01 · 运行中</span></div>
      <div class="kv"><span class="kv-key">网络隔离</span><span class="kv-val" style="color:var(--accent)">已启用</span></div>
      <div class="kv"><span class="kv-key">本地 GPU</span><span class="kv-val">68% · 18.4GB</span></div>
      <div class="kv"><span class="kv-key">云端成本</span><span class="kv-val">$0.42 / $5.00</span></div>
      <div class="bar"><div class="bar-fill" style="width:8.4%"></div></div>
    </div>
  </div>
  <div class="card">
    <div class="card-head">降级链路</div>
    <div class="card-body">
      <div class="kv"><span class="kv-key">模式</span><span class="kv-val" style="color:var(--accent)">云主本辅</span></div>
      <div class="kv"><span class="kv-key">回退率</span><span class="kv-val">3.6%</span></div>
      <div class="kv"><span class="kv-key">记忆账本</span><span class="kv-val">已同步</span></div>
    </div>
  </div>
</aside>
"""

MODALS = r"""<div class="overlay" id="stopOverlay">
  <div class="modal">
    <div class="modal-icon">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ff4d4f" stroke-width="2.2"><rect x="6" y="6" width="12" height="12" rx="2"/></svg>
    </div>
    <h3>确认紧急停止？</h3>
    <p>将立即终止所有沙箱容器、模型调用与待执行任务，并冻结审计日志。此操作会记录操作人与时间戳，无法撤销。</p>
    <div class="modal-actions"><button class="btn" onclick="closeStop()">取消</button><button class="btn btn--danger" onclick="closeStop()">确认停止</button></div>
  </div>
</div>

<div class="overlay" id="skillOverlay">
  <div class="modal modal--lg">
    <div class="modal-head">
      <div class="modal-icon" style="width:34px;height:34px;margin:0;background:rgba(0,217,163,.12);border-color:rgba(0,217,163,.35)">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#00d9a3" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M17 8l-5-5-5 5M12 3v12"/></svg>
      </div>
      <h3>导入 Skill</h3>
      <button class="modal-close" onclick="closeSkillImport()">×</button>
    </div>
    <div class="steps">
      <div class="step active" data-step="1"><span class="step-num">1</span> 选择来源</div>
      <div class="step-line" data-line="1"></div>
      <div class="step" data-step="2"><span class="step-num">2</span> 预览与校验</div>
      <div class="step-line" data-line="2"></div>
      <div class="step" data-step="3"><span class="step-num">3</span> 确认导入</div>
    </div>
    <div class="modal-scroll">
      <div class="import-pane" data-pane="1">
        <div class="tabs" data-tabs="import" style="margin-bottom:16px">
          <div class="tab active" data-panel="imp-file">上传文件</div>
          <div class="tab" data-panel="imp-paste">粘贴内容</div>
          <div class="tab" data-panel="imp-url">从 URL</div>
          <div class="tab" data-panel="imp-git">Git 仓库</div>
        </div>
        <div data-tab-group="import">
          <div class="tab-panel" id="imp-file">
            <div class="dropzone" id="dropzone">
              <div class="dropzone-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M17 8l-5-5-5 5M12 3v12"/></svg></div>
              <div class="dropzone-title">拖拽 Skill 包到此处</div>
              <div class="dropzone-hint">支持 <code>.json</code> <code>.yaml</code> <code>.yml</code> <code>.zip</code> <code>.skill</code><br>单个文件最大 10 MB · 导入前会自动做签名与敏感操作扫描</div>
            </div>
            <div class="file-chip" id="dropzoneFile" hidden></div>
          </div>
          <div class="tab-panel" id="imp-paste" hidden>
            <div style="display:flex;gap:8px;margin-bottom:11px">
              <select class="select" style="width:120px"><option>YAML</option><option>JSON</option></select>
              <div class="spacer" style="flex:1"></div>
              <button class="btn" style="height:32px">载入示例</button>
            </div>
            <textarea class="input" style="height:200px;padding:11px;font-family:var(--mono);font-size:11.5px;line-height:1.7;resize:vertical;width:100%" placeholder="name: my-skill&#10;version: 1.0.0&#10;permissions:&#10;  tools: [nmap]&#10;  risk_level: low"></textarea>
          </div>
          <div class="tab-panel" id="imp-url" hidden>
            <div style="font-size:12px;color:var(--muted);margin-bottom:11px;line-height:1.7">从 HTTPS URL 拉取 Skill manifest，仅允许 https，且会校验 TLS 证书与响应哈希。</div>
            <input class="input" style="width:100%" placeholder="https://registry.example.com/skills/sql-injection-probe.yaml" />
          </div>
          <div class="tab-panel" id="imp-git" hidden>
            <div style="font-size:12px;color:var(--muted);margin-bottom:11px;line-height:1.7">从 Git 仓库的指定路径导入 Skill，支持固定 commit 以保证可复现性。</div>
            <input class="input" style="width:100%;margin-bottom:9px" placeholder="https://github.com/org/skills.git" />
            <div style="display:flex;gap:9px">
              <input class="input" style="flex:1" placeholder="分支 / 标签，如 main" />
              <input class="input" style="flex:1" placeholder="Skill 路径，如 skills/sqli" />
            </div>
          </div>
        </div>
      </div>
      <div class="import-pane" data-pane="2" hidden>
        <div class="grid-2" style="gap:16px;margin-bottom:18px">
          <div>
            <div style="font-size:12px;font-weight:620;margin-bottom:9px">Manifest 预览</div>
            <div class="manifest"><span class="c"># sql-injection-probe.yaml</span>
<span class="k">name</span>: <span class="s">sql-injection-probe</span>
<span class="k">version</span>: <span class="s">1.2.0</span>
<span class="k">author</span>: <span class="s">security-team</span>
<span class="k">description</span>: <span class="s">Web 应用 SQL 注入检测与验证</span>
<span class="k">mitre</span>: [<span class="s">T1190</span>]

<span class="k">permissions</span>:
  <span class="k">tools</span>: [<span class="s">nuclei</span>, <span class="s">sqlmap</span>, <span class="s">burp</span>]
  <span class="k">network</span>: <span class="s">restricted</span>
  <span class="k">filesystem</span>: <span class="s">read-only</span>
  <span class="k">risk_level</span>: <span class="s">high</span>

<span class="k">safety</span>:
  <span class="k">rollback</span>: <span class="s">snapshot</span>
  <span class="k">deny_list</span>: [<span class="s">--os-shell</span>, <span class="s">--os-pwn</span>]</div>
          </div>
          <div>
            <div style="font-size:12px;font-weight:620;margin-bottom:9px">安全校验</div>
            <div class="check-list" id="validateList">
              <div class="check-item"><div class="check-icon check-icon--ok">✓</div><div class="check-body"><div class="check-title">签名验证通过</div><div class="check-desc">ed25519 · security-team@acme.com</div></div></div>
              <div class="check-item"><div class="check-icon check-icon--ok">✓</div><div class="check-body"><div class="check-title">敏感命令扫描通过</div><div class="check-desc">未发现 rm -rf / 反弹 shell</div></div></div>
              <div class="check-item"><div class="check-icon check-icon--warn">!</div><div class="check-body"><div class="check-title">包含高风险步骤</div><div class="check-desc">step:confirm 已标记 requires_approval</div></div></div>
            </div>
          </div>
        </div>
        <div style="font-size:12px;font-weight:620;margin-bottom:9px">权限声明</div>
        <div class="check-list">
          <div class="check-item"><div class="check-icon check-icon--ok" style="background:rgba(77,171,247,.15);color:var(--blue)">⚙</div><div class="check-body"><div class="check-title">工具调用</div><div class="check-desc">nuclei · sqlmap · burp</div></div></div>
          <div class="check-item"><div class="check-icon check-icon--ok" style="background:rgba(77,171,247,.15);color:var(--blue)">🌐</div><div class="check-body"><div class="check-title">网络访问</div><div class="check-desc">restricted — 仅限目标白名单</div></div></div>
          <div class="check-item"><div class="check-icon check-icon--ok" style="background:rgba(77,171,247,.15);color:var(--blue)">📁</div><div class="check-body"><div class="check-title">文件系统</div><div class="check-desc">read-only — 沙箱内 /tmp 可写</div></div></div>
        </div>
      </div>
      <div class="import-pane" data-pane="3" hidden>
        <div class="section" style="margin-bottom:16px">
          <div class="section-head"><span class="section-title">导入摘要</span><div class="spacer"></div><span class="tag tag--verified">校验通过</span></div>
          <div class="section-body" style="padding-top:8px;padding-bottom:8px">
            <div class="kv"><span class="kv-key">Skill 名称</span><span class="kv-val">sql-injection-probe</span></div>
            <div class="kv"><span class="kv-key">版本</span><span class="kv-val">v1.2.0</span></div>
            <div class="kv"><span class="kv-key">作者</span><span class="kv-val">security-team</span></div>
            <div class="kv"><span class="kv-key">风险等级</span><span class="kv-val" style="color:var(--high)">High</span></div>
            <div class="kv"><span class="kv-key">所需工具</span><span class="kv-val">3 个</span></div>
            <div class="kv"><span class="kv-key">执行步骤</span><span class="kv-val">2 步（1 步需审批）</span></div>
            <div class="kv"><span class="kv-key">MITRE 映射</span><span class="kv-val">T1190</span></div>
          </div>
        </div>
        <div class="confirm-box" onclick="toggleConfirm(this)">
          <div class="checkbox">
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5"><path d="M20 6L9 17l-5-5"/></svg>
          </div>
          <div>
            <div style="font-size:12.5px;font-weight:600">我已审查该 Skill 的权限声明与执行逻辑</div>
            <div style="font-size:11.5px;color:var(--text-dim);margin-top:4px;line-height:1.65">
              导入后该 Skill 将注册到 MCP 工具层，可被 Planner 在匹配阶段自动挂载。高风险步骤仍会在执行前触发人工审批，不会绕过现有门禁。
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-foot">
      <button class="btn" onclick="closeSkillImport()">取消</button>
      <div class="spacer"></div>
      <button class="btn" id="prevBtn" onclick="setImportStep(importStep - 1)" hidden>上一步</button>
      <button class="btn btn--primary" id="nextBtn" onclick="nextImportStep()">下一步</button>
    </div>
  </div>
</div>
"""

# 组装完整 index.html
INDEX_HTML = (
    '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n'
    '<meta charset="UTF-8" />\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
    '<title>AI 渗透测试控制台 · ENG-2041</title>\n'
    '<link rel="stylesheet" href="./styles/tokens.css" />\n'
    '<link rel="stylesheet" href="./styles/base.css" />\n'
    '<link rel="stylesheet" href="./styles/layout.css" />\n'
    '<link rel="stylesheet" href="./styles/components.css" />\n'
    '<link rel="stylesheet" href="./styles/pages.css" />\n'
    '<link rel="stylesheet" href="./styles/modal.css" />\n'
    '</head>\n<body>\n\n<div class="app">\n'
    + TOPBAR + '<div class="body-grid">\n' + SIDEBAR
    + '<main class="main" id="main">\n'
    + PAGE_DASHBOARD + PAGE_ENGAGEMENT + PAGE_ORCHESTRATION + PAGE_EXECUTION
    + PAGE_FINDINGS + PAGE_JS_ANALYSIS + PAGE_MINIAPP_ANALYSIS + PAGE_APP_ANALYSIS
    + PAGE_TRAFFIC_ANALYSIS + PAGE_MODELS + PAGE_TOOLS + PAGE_SKILLS + PAGE_AUDIT + PAGE_REPORTS
    + '</main>\n' + ASIDE + '</div>\n</div>\n\n'
    + MODALS
    + '\n<script type="module" src="./js/main.js"></script>\n</body>\n</html>\n'
)

# ================================================================
# CSS（和上一版一致，直接复用）
# ================================================================

STYLES = {}

STYLES["styles/tokens.css"] = r""":root {
  --bg:#0a0e14; --panel:#111721; --panel-2:#161d29; --panel-3:#1b2432;
  --border:#1e2836; --border-soft:#182130;
  --text:#d6e0ec; --text-dim:#8b9bb0; --muted:#6b7a8f;
  --accent:#00d9a3; --accent-dim:#00d9a322; --accent-glow:0 0 24px rgba(0,217,163,.25);
  --blue:#4dabf7; --crit:#ff4d4f; --high:#ff8c1a; --med:#ffd60a; --low:#4dabf7; --info:#6b7a8f;
  --mono:"JetBrains Mono","SF Mono","Cascadia Code",Consolas,monospace;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
  --r-sm:6px; --r-md:10px; --r-lg:14px;
  --topbar-h:56px; --sidebar-w:216px; --aside-w:320px;
}
"""

STYLES["styles/base.css"] = r"""* { margin:0; padding:0; box-sizing:border-box; }
html, body { height:100%; }
body {
  background:var(--bg); color:var(--text); font-family:var(--sans);
  font-size:13px; line-height:1.55; -webkit-font-smoothing:antialiased; overflow:hidden;
}
body::before {
  content:""; position:fixed; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(900px 500px at 12% -8%, rgba(0,217,163,.07), transparent 60%),
    radial-gradient(700px 460px at 92% 4%, rgba(77,171,247,.06), transparent 62%);
}
::-webkit-scrollbar { width:8px; height:8px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:#253044; border-radius:99px; }
::-webkit-scrollbar-thumb:hover { background:#33415a; }
.spacer { flex:1; }
"""

STYLES["styles/layout.css"] = r""".app { position:relative; z-index:1; display:grid; grid-template-rows:var(--topbar-h) 1fr; height:100vh; }
.body-grid { display:grid; grid-template-columns:var(--sidebar-w) minmax(0,1fr) var(--aside-w); overflow:hidden; }

.topbar { display:flex; align-items:center; gap:16px; padding:0 16px; background:rgba(17,23,33,.82); backdrop-filter:blur(14px); border-bottom:1px solid var(--border); }
.brand { display:flex; align-items:center; gap:9px; padding-right:16px; border-right:1px solid var(--border); height:30px; }
.brand-mark { width:26px; height:26px; display:grid; place-items:center; border-radius:7px; background:linear-gradient(140deg,var(--accent),#009e78); box-shadow:var(--accent-glow); color:#04120e; font-weight:800; font-size:13px; }
.brand-name { font-weight:650; letter-spacing:.2px; font-size:13px; }
.brand-sub { font-size:10px; color:var(--muted); letter-spacing:.8px; text-transform:uppercase; }
.eng-switch { display:flex; align-items:center; gap:10px; padding:5px 11px; background:var(--panel-2); border:1px solid var(--border); border-radius:var(--r-sm); cursor:pointer; transition:border-color .15s, background .15s; }
.eng-switch:hover { border-color:#2b3a52; background:var(--panel-3); }
.eng-id { font-family:var(--mono); font-size:10px; color:var(--accent); background:var(--accent-dim); padding:1px 6px; border-radius:4px; }
.eng-title { font-size:12px; font-weight:550; }

.badge { display:inline-flex; align-items:center; gap:6px; height:24px; padding:0 9px; border-radius:999px; font-size:11px; font-weight:550; border:1px solid transparent; white-space:nowrap; }
.badge--lock { color:var(--accent); background:var(--accent-dim); border-color:rgba(0,217,163,.28); }

.model-chips { display:flex; gap:8px; }
.chip { display:flex; align-items:center; gap:8px; height:34px; padding:0 11px; background:var(--panel-2); border:1px solid var(--border); border-radius:var(--r-sm); min-width:0; }
.chip-label { font-size:10px; color:var(--muted); text-transform:uppercase; letter-spacing:.6px; }
.chip-meta { font-family:var(--mono); font-size:10px; color:var(--muted); }

.dot { width:7px; height:7px; border-radius:50%; flex-shrink:0; position:relative; }
.dot--on { background:var(--accent); box-shadow:0 0 8px var(--accent); }
.dot--busy { background:var(--med); box-shadow:0 0 8px var(--med); }
.dot--off { background:#47536b; }
.dot--on::after, .dot--busy::after { content:""; position:absolute; inset:-4px; border-radius:50%; border:1px solid currentColor; opacity:.45; animation:pulse 2.2s ease-out infinite; }
.dot--on::after { border-color:var(--accent); }
.dot--busy::after { border-color:var(--med); }
@keyframes pulse { 0% { transform:scale(.7); opacity:.6; } 100% { transform:scale(1.9); opacity:0; } }

.btn-stop { display:inline-flex; align-items:center; gap:7px; height:34px; padding:0 14px; border-radius:var(--r-sm); background:rgba(255,77,79,.1); border:1px solid rgba(255,77,79,.4); color:#ff7b7d; font-size:12px; font-weight:650; cursor:pointer; transition:all .15s; }
.btn-stop:hover { background:rgba(255,77,79,.2); border-color:var(--crit); color:#ff9a9c; box-shadow:0 0 20px rgba(255,77,79,.25); }

.sidebar { background:rgba(17,23,33,.6); border-right:1px solid var(--border); padding:14px 10px; overflow-y:auto; display:flex; flex-direction:column; gap:22px; }
.nav-group-title { font-size:10px; color:var(--muted); text-transform:uppercase; letter-spacing:1px; padding:0 9px 7px; font-weight:600; }
.nav { display:flex; flex-direction:column; gap:2px; }
.nav-item { display:flex; align-items:center; gap:10px; padding:8px 10px; border-radius:var(--r-sm); color:var(--text-dim); font-size:12.5px; cursor:pointer; border-left:2px solid transparent; transition:background .13s, color .13s; user-select:none; }
.nav-item:hover { background:var(--panel-2); color:var(--text); }
.nav-item.active { background:linear-gradient(90deg,rgba(0,217,163,.14),rgba(0,217,163,.02)); color:var(--accent); border-left-color:var(--accent); font-weight:600; }
.nav-icon { width:15px; height:15px; flex-shrink:0; opacity:.9; }
.nav-count { margin-left:auto; font-family:var(--mono); font-size:10px; background:var(--panel-3); color:var(--text-dim); padding:1px 6px; border-radius:99px; }
.nav-item.active .nav-count { background:rgba(0,217,163,.16); color:var(--accent); }
.nav-count--alert { background:rgba(255,77,79,.16); color:#ff7b7d; }

.main { overflow-y:auto; padding:18px 20px 40px; }
.page[hidden] { display:none !important; }
.page-head { display:flex; align-items:flex-start; gap:16px; margin-bottom:18px; }
.page-title { font-size:19px; font-weight:680; letter-spacing:-.2px; }
.page-desc { font-size:12px; color:var(--muted); margin-top:3px; }
.page-actions { margin-left:auto; display:flex; gap:8px; }

.aside { background:rgba(17,23,33,.6); border-left:1px solid var(--border); overflow-y:auto; padding:14px; display:flex; flex-direction:column; gap:12px; }

@media (max-width:1600px) {
  .workbench { grid-template-columns:260px minmax(0,1fr); }
  .workbench > .wb-right { grid-column:1 / -1; }
}
@media (max-width:1400px) {
  .body-grid { grid-template-columns:var(--sidebar-w) minmax(0,1fr); }
  .aside { display:none; }
}
@media (max-width:1200px) { .workbench, .analysis-grid { grid-template-columns:1fr; } }
@media (max-width:1080px) {
  .kpis { grid-template-columns:repeat(2,minmax(0,1fr)); }
  .model-chips { display:none; }
  .grid-2, .grid-3 { grid-template-columns:1fr; }
}
"""

STYLES["styles/components.css"] = r""".btn { height:32px; padding:0 13px; border-radius:var(--r-sm); border:1px solid var(--border); background:var(--panel-2); color:var(--text); font-size:12px; font-weight:550; cursor:pointer; display:inline-flex; align-items:center; gap:6px; transition:all .15s; white-space:nowrap; }
.btn:hover { background:var(--panel-3); border-color:#2b3a52; }
.btn:disabled { opacity:.4; cursor:not-allowed; }
.btn--primary { background:rgba(0,217,163,.14); border-color:rgba(0,217,163,.4); color:var(--accent); }
.btn--primary:hover { background:rgba(0,217,163,.22); box-shadow:var(--accent-glow); }
.btn--danger { background:rgba(255,77,79,.12); border-color:rgba(255,77,79,.38); color:#ff7b7d; }
.btn--danger:hover { background:rgba(255,77,79,.2); }

.card { background:var(--panel); border:1px solid var(--border); border-radius:var(--r-md); overflow:hidden; }
.card-head { padding:10px 13px; border-bottom:1px solid var(--border-soft); font-size:11.5px; font-weight:620; display:flex; align-items:center; gap:8px; }
.card-head .spacer { flex:1; }
.card-body { padding:12px 13px; }

.kv { display:flex; justify-content:space-between; gap:10px; padding:5px 0; font-size:12px; }
.kv + .kv { border-top:1px solid var(--border-soft); }
.kv-key { color:var(--muted); }
.kv-val { font-family:var(--mono); font-size:11.5px; text-align:right; }

.bar { height:5px; background:var(--panel-3); border-radius:99px; overflow:hidden; margin-top:7px; }
.bar-fill { height:100%; border-radius:99px; background:linear-gradient(90deg,var(--accent),#4ade80); transition:width .5s ease; }
.bar-fill--warn { background:linear-gradient(90deg,var(--high),var(--med)); }

.call { display:flex; align-items:center; gap:9px; padding:8px 0; font-size:11.5px; }
.call + .call { border-top:1px solid var(--border-soft); }
.call-body { flex:1; min-width:0; }
.call-name { font-family:var(--mono); font-size:11px; color:var(--text); }
.call-meta { font-size:10.5px; color:var(--muted); margin-top:2px; }

.approve { border:1px solid rgba(255,140,26,.35); background:linear-gradient(180deg,rgba(255,140,26,.08),rgba(255,140,26,.02)); border-radius:var(--r-md); padding:13px; }
.approve-title { display:flex; align-items:center; gap:7px; font-size:12.5px; font-weight:650; color:var(--high); margin-bottom:7px; }
.approve-desc { font-size:11.5px; color:var(--text-dim); line-height:1.6; margin-bottom:11px; }
.approve-cmd { font-family:var(--mono); font-size:11px; background:#070a0f; border:1px solid var(--border); border-radius:var(--r-sm); padding:8px 10px; color:var(--accent); margin-bottom:11px; word-break:break-all; }
.approve-actions { display:flex; gap:8px; }
.approve-actions .btn { flex:1; justify-content:center; }

.table { width:100%; border-collapse:collapse; }
.table th { text-align:left; font-size:10px; font-weight:600; color:var(--muted); text-transform:uppercase; letter-spacing:.8px; padding:0 14px 9px; border-bottom:1px solid var(--border-soft); }
.table td { padding:11px 14px; font-size:12.5px; border-bottom:1px solid var(--border-soft); vertical-align:middle; }
.table tbody tr { transition:background .13s; cursor:pointer; }
.table tbody tr:hover { background:var(--panel-2); }
.table tbody tr:last-child td { border-bottom:none; }

.sev { display:inline-flex; align-items:center; gap:6px; font-size:10.5px; font-weight:650; letter-spacing:.5px; text-transform:uppercase; }
.sev::before { content:""; width:6px; height:6px; border-radius:2px; background:currentColor; box-shadow:0 0 7px currentColor; }
.sev--crit { color:var(--crit); }
.sev--high { color:var(--high); }
.sev--med  { color:var(--med); }
.sev--low  { color:var(--low); }
.sev--info { color:var(--info); }

.mono { font-family:var(--mono); font-size:11.5px; color:var(--text-dim); }

.tag { display:inline-block; padding:2px 8px; border-radius:4px; font-size:10.5px; font-weight:600; border:1px solid transparent; white-space:nowrap; }
.tag--verified { color:var(--accent); background:var(--accent-dim); border-color:rgba(0,217,163,.25); }
.tag--pending { color:var(--med); background:rgba(255,214,10,.1); border-color:rgba(255,214,10,.24); }
.tag--fp { color:var(--muted); background:rgba(107,122,143,.12); border-color:rgba(107,122,143,.24); }
.tag--running { color:var(--blue); background:rgba(77,171,247,.1); border-color:rgba(77,171,247,.26); }
.tag--done { color:var(--accent); background:var(--accent-dim); border-color:rgba(0,217,163,.25); }
.tag--queued { color:var(--muted); background:rgba(107,122,143,.12); border-color:rgba(107,122,143,.24); }
.tag--blocked { color:var(--high); background:rgba(255,140,26,.1); border-color:rgba(255,140,26,.26); }

.term { background:#070a0f; border:1px solid var(--border); border-radius:var(--r-sm); font-family:var(--mono); font-size:11.5px; line-height:1.75; padding:12px 14px; max-height:190px; overflow-y:auto; }
.term-line { white-space:pre-wrap; word-break:break-all; }
.t-dim { color:#4a5568; }
.t-cmd { color:var(--accent); }
.t-ok { color:#4ade80; }
.t-warn { color:var(--med); }
.t-err { color:var(--crit); }
.t-info { color:var(--blue); }
.t-cursor { display:inline-block; width:7px; height:13px; background:var(--accent); vertical-align:-2px; animation:blink 1.1s step-end infinite; }
@keyframes blink { 50% { opacity:0; } }

.toolbar { display:flex; align-items:center; gap:8px; margin-bottom:14px; flex-wrap:wrap; }
.toolbar .spacer { flex:1; }
.input, .select { height:32px; padding:0 11px; background:var(--panel-2); border:1px solid var(--border); border-radius:var(--r-sm); color:var(--text); font-size:12px; font-family:var(--sans); outline:none; transition:border-color .15s; }
.input:focus, .select:focus { border-color:rgba(0,217,163,.5); }
.input::placeholder { color:var(--muted); }
.select { cursor:pointer; }
.select option { background:var(--panel-2); }

.grid-2 { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:14px; }
.grid-3 { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:14px; }

.tabs { display:flex; gap:4px; border-bottom:1px solid var(--border); margin-bottom:14px; }
.tab { padding:8px 14px; font-size:12px; color:var(--muted); cursor:pointer; border-bottom:2px solid transparent; margin-bottom:-1px; transition:all .15s; user-select:none; }
.tab:hover { color:var(--text); }
.tab.active { color:var(--accent); border-bottom-color:var(--accent); font-weight:600; }
.tab-panel[hidden] { display:none !important; }

.toggle { width:38px; height:21px; border-radius:99px; background:var(--panel-3); border:1px solid var(--border); position:relative; cursor:pointer; transition:all .2s; flex-shrink:0; }
.toggle::after { content:""; position:absolute; top:2px; left:2px; width:15px; height:15px; border-radius:50%; background:var(--muted); transition:all .2s; }
.toggle.on { background:rgba(0,217,163,.2); border-color:rgba(0,217,163,.5); }
.toggle.on::after { left:19px; background:var(--accent); box-shadow:0 0 8px var(--accent); }

.form-row { display:flex; justify-content:space-between; align-items:center; gap:14px; padding:11px 0; }
.form-row + .form-row { border-top:1px solid var(--border-soft); }
.form-label { font-size:12.5px; }
.form-hint { font-size:11px; color:var(--muted); margin-top:2px; }

.empty { padding:40px 20px; text-align:center; color:var(--muted); font-size:12.5px; }

.model-card { background:var(--panel); border:1px solid var(--border); border-radius:var(--r-md); padding:15px; transition:border-color .18s; }
.model-card:hover { border-color:#2b3a52; }
.model-card-head { display:flex; align-items:center; gap:9px; margin-bottom:10px; }
.model-card-name { font-size:13px; font-weight:650; }
.model-card-sub { font-size:11px; color:var(--muted); margin-top:1px; }

.report-item { display:flex; align-items:center; gap:14px; padding:14px 15px; border-bottom:1px solid var(--border-soft); transition:background .13s; cursor:pointer; }
.report-item:hover { background:var(--panel-2); }
.report-item:last-child { border-bottom:none; }
.report-icon { width:36px; height:36px; border-radius:var(--r-sm); display:grid; place-items:center; background:var(--panel-3); border:1px solid var(--border); flex-shrink:0; color:var(--accent); }

.section { background:var(--panel); border:1px solid var(--border); border-radius:var(--r-md); margin-bottom:16px; overflow:hidden; }
.section-head { display:flex; align-items:center; gap:10px; padding:12px 15px; border-bottom:1px solid var(--border-soft); }
.section-title { font-size:13px; font-weight:620; }
.section-sub { font-size:11px; color:var(--muted); }
.section-head .spacer { flex:1; }
.section-body { padding:15px; }
"""

STYLES["styles/pages.css"] = r""".kpis { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:12px; margin-bottom:18px; }
.kpi { position:relative; background:var(--panel); border:1px solid var(--border); border-radius:var(--r-md); padding:14px 15px; overflow:hidden; transition:border-color .18s; }
.kpi:hover { border-color:#2b3a52; }
.kpi::after { content:""; position:absolute; top:0; left:0; right:0; height:1px; background:linear-gradient(90deg,transparent,var(--accent),transparent); opacity:0; transition:opacity .2s; }
.kpi:hover::after { opacity:.6; }
.kpi-label { font-size:11px; color:var(--muted); text-transform:uppercase; letter-spacing:.7px; margin-bottom:8px; }
.kpi-value { font-family:var(--mono); font-size:26px; font-weight:600; line-height:1; letter-spacing:-.5px; }
.kpi-foot { margin-top:8px; font-size:11px; color:var(--muted); display:flex; align-items:center; gap:5px; }
.kpi-delta { font-family:var(--mono); }
.kpi-delta--up { color:var(--crit); }
.kpi-delta--down { color:var(--accent); }

.flow { display:flex; align-items:center; gap:0; overflow-x:auto; padding:4px 0 6px; }
.flow-node { flex-shrink:0; display:flex; flex-direction:column; align-items:center; gap:7px; min-width:92px; position:relative; }
.flow-circle { width:40px; height:40px; border-radius:50%; display:grid; place-items:center; font-family:var(--mono); font-size:12px; font-weight:600; border:1.5px solid var(--border); background:var(--panel-2); color:var(--muted); transition:all .2s; }
.flow-node.done .flow-circle { border-color:rgba(0,217,163,.5); background:rgba(0,217,163,.1); color:var(--accent); }
.flow-node.active .flow-circle { border-color:var(--accent); background:rgba(0,217,163,.16); color:var(--accent); box-shadow:0 0 0 5px rgba(0,217,163,.08), var(--accent-glow); animation:breathe 2s ease-in-out infinite; }
@keyframes breathe { 0%, 100% { box-shadow:0 0 0 5px rgba(0,217,163,.08), 0 0 18px rgba(0,217,163,.2); } 50% { box-shadow:0 0 0 9px rgba(0,217,163,.04), 0 0 30px rgba(0,217,163,.32); } }
.flow-label { font-size:11px; color:var(--text-dim); white-space:nowrap; }
.flow-node.active .flow-label { color:var(--accent); font-weight:600; }
.flow-node.done .flow-label { color:var(--text); }
.flow-meta { font-family:var(--mono); font-size:10px; color:var(--muted); }
.flow-link { flex:1; min-width:26px; height:1.5px; background:var(--border); margin-bottom:34px; border-radius:2px; position:relative; }
.flow-link.done { background:linear-gradient(90deg,rgba(0,217,163,.6),rgba(0,217,163,.25)); }
.flow-link.active { background:linear-gradient(90deg,rgba(0,217,163,.7),var(--border)); overflow:hidden; }
.flow-link.active::after { content:""; position:absolute; inset:0; background:linear-gradient(90deg,transparent,var(--accent),transparent); animation:slide 1.6s linear infinite; }
@keyframes slide { 0% { transform:translateX(-100%); } 100% { transform:translateX(100%); } }

.workbench { display:grid; grid-template-columns:300px minmax(0,1fr) 320px; gap:14px; align-items:start; }
.analysis-grid { display:grid; grid-template-columns:260px minmax(0,1fr); gap:14px; }

.code-view { background:#070a0f; border:1px solid var(--border); border-radius:var(--r-sm); font-family:var(--mono); font-size:11.5px; line-height:1.75; overflow:auto; max-height:460px; }
.code-line { display:flex; padding:0 12px; cursor:pointer; }
.code-line:hover { background:rgba(0,217,163,.05); }
.code-line.hl { background:rgba(255,214,10,.1); }
.code-ln { width:42px; color:#3a4658; text-align:right; padding-right:14px; user-select:none; flex-shrink:0; }
.code-src { white-space:pre; color:var(--text-dim); }
.code-src .kw { color:#c792ea; }
.code-src .str { color:#4ade80; }
.code-src .num { color:var(--med); }
.code-src .cmt { color:#4a5568; font-style:italic; }
.code-src .fn { color:var(--blue); }
.code-src .tag { color:var(--high); }

.tree { font-size:12px; user-select:none; }
.tree-item { display:flex; align-items:center; gap:7px; padding:5px 9px; border-radius:var(--r-sm); cursor:pointer; color:var(--text-dim); transition:background .12s; }
.tree-item:hover { background:var(--panel-2); color:var(--text); }
.tree-item.active { background:rgba(0,217,163,.1); color:var(--accent); }
.tree-item .ico { width:13px; height:13px; opacity:.7; flex-shrink:0; }
.tree-item .meta { margin-left:auto; font-family:var(--mono); font-size:10px; color:var(--muted); }
.tree-children { padding-left:14px; }

.packet-head { display:grid; grid-template-columns:74px 52px minmax(0,1fr) 56px 66px 62px; gap:10px; padding:0 12px 9px; font-size:10px; color:var(--muted); text-transform:uppercase; letter-spacing:.7px; border-bottom:1px solid var(--border-soft); }
.packet-row { display:grid; grid-template-columns:74px 52px minmax(0,1fr) 56px 66px 62px; gap:10px; padding:9px 12px; font-size:12px; border-bottom:1px solid var(--border-soft); cursor:pointer; align-items:center; transition:background .12s; }
.packet-row:hover { background:var(--panel-2); }
.packet-row.active { background:rgba(0,217,163,.08); box-shadow:inset 2px 0 0 var(--accent); }
.packet-url { font-family:var(--mono); font-size:11.5px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.method { font-family:var(--mono); font-size:10px; font-weight:700; text-align:center; padding:2px 0; border-radius:3px; }
.method--get { color:var(--blue); background:rgba(77,171,247,.14); }
.method--post { color:var(--accent); background:rgba(0,217,163,.14); }
.method--put { color:var(--high); background:rgba(255,140,26,.14); }
.method--del { color:var(--crit); background:rgba(255,77,79,.14); }
.method--ws { color:#c792ea; background:rgba(199,146,234,.14); }
.status { font-family:var(--mono); font-size:11px; }
.status--2xx { color:var(--accent); }
.status--3xx { color:var(--blue); }
.status--4xx { color:var(--med); }
.status--5xx { color:var(--crit); }

.req-block { margin-bottom:14px; }
.req-title { font-size:11.5px; font-weight:620; margin-bottom:7px; display:flex; align-items:center; gap:7px; }
.req-title .spacer { flex:1; }
.req-body { background:#070a0f; border:1px solid var(--border); border-radius:var(--r-sm); font-family:var(--mono); font-size:11px; line-height:1.75; padding:11px 13px; max-height:220px; overflow:auto; white-space:pre-wrap; word-break:break-all; color:var(--text-dim); }

.secret { padding:10px 12px; background:rgba(255,140,26,.06); border:1px solid rgba(255,140,26,.25); border-radius:var(--r-sm); margin-bottom:8px; }
.secret-label { font-size:10.5px; color:var(--high); font-weight:650; text-transform:uppercase; letter-spacing:.5px; }
.secret-val { font-family:var(--mono); font-size:11px; color:var(--text); margin-top:5px; word-break:break-all; line-height:1.55; }
.secret-src { font-size:10px; color:var(--muted); margin-top:4px; }

.api-item { padding:10px 12px; background:var(--panel-2); border:1px solid var(--border-soft); border-radius:var(--r-sm); margin-bottom:7px; cursor:pointer; transition:border-color .15s; }
.api-item:hover { border-color:rgba(0,217,163,.4); }
.api-path { font-family:var(--mono); font-size:11.5px; color:var(--accent); word-break:break-all; }
.api-meta { font-size:10.5px; color:var(--muted); margin-top:5px; display:flex; gap:10px; flex-wrap:wrap; }

.bypass-card { padding:11px 13px; background:var(--panel-2); border:1px solid var(--border); border-left:2px solid var(--high); border-radius:var(--r-sm); margin-bottom:9px; }
.bypass-title { font-size:12px; font-weight:620; margin-bottom:5px; }
.bypass-desc { font-size:11px; color:var(--text-dim); line-height:1.6; }
.bypass-actions { display:flex; gap:6px; margin-top:10px; }
.bypass-actions .btn { height:26px; font-size:11px; }

.chip-mini { display:inline-flex; align-items:center; gap:4px; font-family:var(--mono); font-size:10px; padding:2px 7px; border-radius:4px; background:var(--panel-3); color:var(--text-dim); }
.chip-mini--warn { color:var(--high); background:rgba(255,140,26,.12); }
.chip-mini--ok { color:var(--accent); background:var(--accent-dim); }

.skill-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(290px,1fr)); gap:14px; }
.skill-card { position:relative; background:var(--panel); border:1px solid var(--border); border-radius:var(--r-md); padding:15px; cursor:pointer; overflow:hidden; transition:border-color .18s, transform .18s; }
.skill-card:hover { border-color:rgba(0,217,163,.4); transform:translateY(-1px); }
.skill-card::before { content:""; position:absolute; top:0; left:0; right:0; height:2px; background:linear-gradient(90deg,var(--accent),transparent); opacity:0; transition:opacity .2s; }
.skill-card:hover::before { opacity:1; }
.skill-top { display:flex; align-items:flex-start; gap:11px; margin-bottom:10px; }
.skill-icon { width:38px; height:38px; border-radius:var(--r-sm); display:grid; place-items:center; background:var(--panel-3); border:1px solid var(--border); font-size:17px; flex-shrink:0; }
.skill-name { font-size:13px; font-weight:650; display:flex; align-items:center; gap:6px; flex-wrap:wrap; }
.skill-ver { font-family:var(--mono); font-size:10px; color:var(--muted); background:var(--panel-3); padding:1px 5px; border-radius:3px; }
.skill-author { font-size:11px; color:var(--muted); margin-top:2px; }
.skill-desc { font-size:11.5px; color:var(--text-dim); line-height:1.6; margin-bottom:11px; min-height:36px; }
.skill-tags { display:flex; flex-wrap:wrap; gap:5px; margin-bottom:11px; }
.skill-tag { font-family:var(--mono); font-size:10px; color:var(--muted); background:var(--panel-3); padding:2px 7px; border-radius:4px; border:1px solid var(--border-soft); }
.skill-foot { display:flex; align-items:center; gap:12px; padding-top:11px; border-top:1px solid var(--border-soft); font-size:11px; color:var(--muted); }
.skill-stat { display:flex; align-items:center; gap:5px; }
.skill-foot .toggle { margin-left:auto; }
"""

STYLES["styles/modal.css"] = r""".overlay { position:fixed; inset:0; background:rgba(4,7,11,.78); backdrop-filter:blur(5px); display:none; place-items:center; z-index:100; }
.overlay.show { display:grid; }

.modal { width:400px; background:var(--panel); border:1px solid rgba(255,77,79,.35); border-radius:var(--r-lg); padding:22px; box-shadow:0 24px 70px rgba(0,0,0,.7), 0 0 50px rgba(255,77,79,.1); }
.modal-icon { width:42px; height:42px; border-radius:50%; display:grid; place-items:center; background:rgba(255,77,79,.12); border:1px solid rgba(255,77,79,.35); margin-bottom:14px; }
.modal h3 { font-size:16px; margin-bottom:7px; }
.modal p { font-size:12.5px; color:var(--text-dim); line-height:1.65; margin-bottom:18px; }
.modal-actions { display:flex; gap:9px; }
.modal-actions .btn { flex:1; height:36px; justify-content:center; }

.steps { display:flex; align-items:center; margin-bottom:20px; flex-shrink:0; }
.step { display:flex; align-items:center; gap:8px; font-size:12px; color:var(--muted); white-space:nowrap; }
.step-num { width:24px; height:24px; border-radius:50%; display:grid; place-items:center; border:1.5px solid var(--border); font-family:var(--mono); font-size:11px; background:var(--panel-2); transition:all .2s; }
.step.active { color:var(--accent); font-weight:600; }
.step.active .step-num { border-color:var(--accent); background:rgba(0,217,163,.12); color:var(--accent); box-shadow:0 0 0 4px rgba(0,217,163,.07); }
.step.done { color:var(--text); }
.step.done .step-num { border-color:rgba(0,217,163,.5); background:rgba(0,217,163,.1); color:var(--accent); }
.step-line { flex:1; height:1.5px; background:var(--border); margin:0 12px; min-width:18px; transition:background .2s; }
.step-line.done { background:rgba(0,217,163,.4); }

.dropzone { border:1.5px dashed var(--border); border-radius:var(--r-md); padding:34px 20px; text-align:center; cursor:pointer; background:var(--panel-2); transition:all .2s; }
.dropzone:hover, .dropzone.drag { border-color:rgba(0,217,163,.5); background:rgba(0,217,163,.04); }
.dropzone-icon { width:48px; height:48px; border-radius:50%; display:grid; place-items:center; background:var(--panel-3); border:1px solid var(--border); margin:0 auto 13px; color:var(--accent); }
.dropzone-title { font-size:13px; font-weight:600; margin-bottom:6px; }
.dropzone-hint { font-size:11.5px; color:var(--muted); line-height:1.8; }
.dropzone-hint code { font-family:var(--mono); font-size:10.5px; background:var(--panel-3); padding:1px 5px; border-radius:3px; color:var(--text-dim); }

.file-chip { display:flex; align-items:center; gap:9px; margin-top:11px; padding:9px 12px; background:rgba(0,217,163,.07); border:1px solid rgba(0,217,163,.28); border-radius:var(--r-sm); font-size:12px; color:var(--accent); }
.file-chip span:nth-child(2) { font-family:var(--mono); font-size:11px; flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }

.check-list { display:flex; flex-direction:column; gap:8px; }
.check-item { display:flex; align-items:flex-start; gap:10px; padding:10px 12px; background:var(--panel-2); border:1px solid var(--border-soft); border-radius:var(--r-sm); font-size:12px; transition:opacity .3s; }
.check-icon { width:18px; height:18px; border-radius:50%; display:grid; place-items:center; flex-shrink:0; margin-top:1px; font-size:10px; font-weight:700; }
.check-icon--ok { background:rgba(0,217,163,.15); color:var(--accent); }
.check-icon--warn { background:rgba(255,214,10,.15); color:var(--med); }
.check-icon--err { background:rgba(255,77,79,.15); color:var(--crit); }
.check-body { flex:1; min-width:0; }
.check-title { font-weight:600; }
.check-desc { font-size:11px; color:var(--muted); margin-top:2px; line-height:1.55; font-family:var(--mono); word-break:break-all; }

.manifest { background:#070a0f; border:1px solid var(--border); border-radius:var(--r-sm); font-family:var(--mono); font-size:11px; line-height:1.75; padding:13px 15px; max-height:300px; overflow-y:auto; white-space:pre; color:var(--text-dim); }
.manifest .k { color:var(--blue); }
.manifest .s { color:#4ade80; }
.manifest .n { color:var(--med); }
.manifest .c { color:#4a5568; }

.modal--lg { width:min(760px,92vw); max-height:88vh; display:flex; flex-direction:column; border-color:var(--border); box-shadow:0 24px 70px rgba(0,0,0,.75), 0 0 60px rgba(0,217,163,.06); }
.modal-head { display:flex; align-items:center; gap:11px; padding-bottom:16px; border-bottom:1px solid var(--border-soft); margin-bottom:18px; flex-shrink:0; }
.modal-head h3 { font-size:15px; }
.modal-close { margin-left:auto; width:28px; height:28px; border-radius:var(--r-sm); border:1px solid var(--border); background:var(--panel-2); color:var(--muted); cursor:pointer; display:grid; place-items:center; font-size:16px; line-height:1; transition:all .15s; }
.modal-close:hover { background:var(--panel-3); color:var(--text); }
.modal-scroll { overflow-y:auto; flex:1; padding-right:4px; }
.modal-foot { display:flex; gap:9px; padding-top:16px; border-top:1px solid var(--border-soft); margin-top:18px; flex-shrink:0; }
.modal-foot .spacer { flex:1; }

.confirm-box { display:flex; align-items:flex-start; gap:11px; padding:13px 15px; background:rgba(255,214,10,.06); border:1px solid rgba(255,214,10,.22); border-radius:var(--r-sm); cursor:pointer; user-select:none; transition:border-color .15s; }
.confirm-box:hover { border-color:rgba(255,214,10,.4); }
.checkbox { width:17px; height:17px; border-radius:4px; border:1.5px solid var(--border); background:var(--panel-2); flex-shrink:0; display:grid; place-items:center; margin-top:1px; transition:all .15s; color:#04120e; }
.checkbox svg { opacity:0; transition:opacity .15s; }
.checkbox.on { background:var(--accent); border-color:var(--accent); }
.checkbox.on svg { opacity:1; }
"""

# ================================================================
# JS（同上一版，全部保留）
# ================================================================

JS = {}

JS["js/main.js"] = r"""import { Toast } from './core/toast.js';
import { bindAll } from './bindings/index.js';

function bootstrap() {
  bindAll();
  Toast.show('控制台已就绪', 'info', 2000);
}

document.readyState === 'loading'
  ? document.addEventListener('DOMContentLoaded', bootstrap)
  : bootstrap();
"""

JS["js/utils.js"] = r"""export const $  = (sel, root = document) => root.querySelector(sel);
export const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
export const sleep = ms => new Promise(r => setTimeout(r, ms));

export function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({
    '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
  }[c]));
}

export function fmtTime(d = new Date()) {
  return `${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}:${String(d.getSeconds()).padStart(2,'0')}`;
}
"""

JS["js/core/toast.js"] = r"""const COLORS = {
  info:    { bg:'rgba(77,171,247,.12)',  border:'rgba(77,171,247,.4)',  color:'#4dabf7' },
  success: { bg:'rgba(0,217,163,.12)',   border:'rgba(0,217,163,.4)',   color:'#00d9a3' },
  warning: { bg:'rgba(255,214,10,.12)',  border:'rgba(255,214,10,.4)',  color:'#ffd60a' },
  error:   { bg:'rgba(255,77,79,.12)',   border:'rgba(255,77,79,.4)',   color:'#ff4d4f' },
};

let container = null;

function ensure() {
  if (container) return container;
  container = document.createElement('div');
  container.id = 'toast-container';
  Object.assign(container.style, {
    position:'fixed', top:'70px', right:'20px',
    display:'flex', flexDirection:'column', gap:'8px',
    zIndex:'200', pointerEvents:'none',
  });
  document.body.appendChild(container);
  return container;
}

export const Toast = {
  show(message, type = 'info', duration = 3000) {
    const c = COLORS[type] || COLORS.info;
    const el = document.createElement('div');
    Object.assign(el.style, {
      background:c.bg, border:`1px solid ${c.border}`, color:c.color,
      padding:'10px 14px', borderRadius:'8px', fontSize:'12.5px',
      backdropFilter:'blur(10px)', boxShadow:'0 8px 24px rgba(0,0,0,.4)',
      maxWidth:'320px', pointerEvents:'auto',
      opacity:'0', transform:'translateX(20px)', transition:'all .25s ease',
    });
    el.textContent = message;
    ensure().appendChild(el);
    requestAnimationFrame(() => {
      el.style.opacity = '1';
      el.style.transform = 'translateX(0)';
    });
    setTimeout(() => {
      el.style.opacity = '0';
      el.style.transform = 'translateX(20px)';
      setTimeout(() => el.remove(), 260);
    }, duration);
  },
};
"""

JS["js/core/store.js"] = r"""export const Store = {
  get: () => ({}),
  set: () => {},
  subscribe: () => () => {},
};
"""

JS["js/core/router.js"] = r"""export const Router = {
  current() { return location.hash.replace(/^#\/?/, '') || 'dashboard'; },
  go(pageId) { location.hash = `#/${pageId}`; },
};
"""

JS["js/data/seed.js"] = r"""export const initialState = {};
export const seed = {};
"""

JS["js/data/mock-api.js"] = r"""export const MockAPI = {};
"""

JS["js/data/mock-ws.js"] = r"""export const WSMock = {
  on: () => () => {},
  emit: () => {},
  start: () => {},
  stop: () => {},
};
"""

JS["js/render/index.js"] = r"""export function renderAll() {}
"""

for name in ["layout", "findings", "orchestration", "skills", "audit"]:
    JS[f"js/render/{name}.js"] = f"export function render{name.capitalize()}() {{}}\n"

JS["js/bindings/index.js"] = r"""import { bindNav } from './nav.js';
import { bindEmergency } from './emergency.js';
import { bindSkillImport } from './skills-import.js';
import { bindCodeView } from './code-view.js';

export function bindAll() {
  bindNav();
  bindEmergency();
  bindSkillImport();
  bindCodeView();
}
"""

JS["js/bindings/nav.js"] = r"""import { $$ } from '../utils.js';

export function bindNav() {
  const navItems = $$('.nav-item[data-page]');
  const pages    = $$('.page');
  const mainEl   = document.getElementById('main');

  function go(pageId) {
    navItems.forEach(i => i.classList.toggle('active', i.dataset.page === pageId));
    pages.forEach(p => { p.hidden = (p.id !== 'page-' + pageId); });
    if (mainEl) mainEl.scrollTop = 0;
  }

  navItems.forEach(item => {
    item.addEventListener('click', () => go(item.dataset.page));
  });

  document.querySelectorAll('.tabs[data-tabs]').forEach(group => {
    const groupName = group.dataset.tabs;
    group.querySelectorAll('.tab').forEach(tab => {
      tab.addEventListener('click', () => {
        group.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        const container = document.querySelector(`[data-tab-group="${groupName}"]`);
        if (!container) return;
        container.querySelectorAll('.tab-panel').forEach(p => { p.hidden = true; });
        const target = document.getElementById(tab.dataset.panel);
        if (target) target.hidden = false;
      });
    });
  });

  window.go = go;
}
"""

JS["js/bindings/emergency.js"] = r"""import { Toast } from '../core/toast.js';

export function bindEmergency() {
  const overlay = document.getElementById('stopOverlay');
  if (!overlay) return;

  function openStop() { overlay.classList.add('show'); }
  function closeStop() { overlay.classList.remove('show'); }

  const confirmBtn = overlay.querySelector('.btn--danger');
  if (confirmBtn) {
    confirmBtn.addEventListener('click', () => {
      Toast.show('已执行紧急停止，所有沙箱任务已终止', 'error', 4000);
    });
  }

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeStop();
  });

  window.openStop = openStop;
  window.closeStop = closeStop;
}
"""

JS["js/bindings/skills-import.js"] = r"""import { $$ } from '../utils.js';
import { Toast } from '../core/toast.js';

let importStep = 1;
let importConfirmed = false;

export function bindSkillImport() {
  const overlay = document.getElementById('skillOverlay');
  if (!overlay) return;

  const stepEls = $$('#skillOverlay .step[data-step]');
  const lineEls = $$('#skillOverlay .step-line[data-line]');
  const paneEls = $$('#skillOverlay .import-pane');

  function openSkillImport() {
    overlay.classList.add('show');
    importConfirmed = false;
    const cb = overlay.querySelector('.checkbox');
    if (cb) cb.classList.remove('on');
    const fileChip = document.getElementById('dropzoneFile');
    if (fileChip) fileChip.hidden = true;
    setImportStep(1);
  }

  function closeSkillImport() { overlay.classList.remove('show'); }

  function setImportStep(n) {
    n = Math.min(3, Math.max(1, n));
    importStep = n;

    stepEls.forEach(s => {
      const sn = +s.dataset.step;
      s.classList.toggle('active', sn === n);
      s.classList.toggle('done', sn < n);
    });
    lineEls.forEach(l => l.classList.toggle('done', +l.dataset.line < n));
    paneEls.forEach(p => { p.hidden = (+p.dataset.pane !== n); });

    const prev = document.getElementById('prevBtn');
    const next = document.getElementById('nextBtn');
    prev.hidden = (n === 1);
    next.textContent = (n === 3) ? '确认导入' : '下一步';
    next.disabled = (n === 3 && !importConfirmed);
    if (n === 2) runValidation();
  }

  function nextImportStep() {
    if (importStep < 3) { setImportStep(importStep + 1); return; }
    const btn = document.getElementById('nextBtn');
    const original = btn.textContent;
    btn.textContent = '导入中…';
    btn.disabled = true;
    setTimeout(() => {
      closeSkillImport();
      btn.textContent = original;
      btn.disabled = false;
      Toast.show('Skill 导入成功，已注册到 MCP 工具层', 'success');
    }, 900);
  }

  function runValidation() {
    $$('#validateList .check-item').forEach((it, i) => {
      it.style.opacity = '.25';
      setTimeout(() => { it.style.opacity = '1'; }, 130 * i);
    });
  }

  function toggleConfirm(el) {
    const cb = el.querySelector('.checkbox');
    cb.classList.toggle('on');
    importConfirmed = cb.classList.contains('on');
    const next = document.getElementById('nextBtn');
    if (importStep === 3) next.disabled = !importConfirmed;
  }

  (function initDropzone() {
    const dz = document.getElementById('dropzone');
    if (!dz) return;
    dz.addEventListener('dragover', e => { e.preventDefault(); dz.classList.add('drag'); });
    dz.addEventListener('dragleave', () => dz.classList.remove('drag'));
    dz.addEventListener('drop', e => {
      e.preventDefault();
      dz.classList.remove('drag');
      if (e.dataTransfer.files.length) showPickedFile(e.dataTransfer.files[0]);
    });
    dz.addEventListener('click', () => {
      const inp = document.createElement('input');
      inp.type = 'file';
      inp.accept = '.json,.yaml,.yml,.zip,.skill';
      inp.onchange = () => { if (inp.files[0]) showPickedFile(inp.files[0]); };
      inp.click();
    });
  })();

  function showPickedFile(file) {
    const box = document.getElementById('dropzoneFile');
    box.hidden = false;
    box.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></svg><span>${file.name}</span><span style="color:var(--muted);font-family:var(--mono);font-size:10.5px">${(file.size/1024).toFixed(1)} KB</span>`;
  }

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeSkillImport();
  });

  window.openSkillImport  = openSkillImport;
  window.closeSkillImport = closeSkillImport;
  window.setImportStep    = setImportStep;
  window.nextImportStep   = nextImportStep;
  window.toggleConfirm    = toggleConfirm;
}
"""

JS["js/bindings/code-view.js"] = r"""import { $$ } from '../utils.js';

export function bindCodeView() {
  $$('.code-view').forEach(view => {
    view.querySelectorAll('.code-line').forEach(line => {
      line.addEventListener('click', () => {
        view.querySelectorAll('.code-line').forEach(l => l.classList.remove('hl'));
        line.classList.add('hl');
      });
    });
  });

  $$('.tree-item').forEach(item => {
    item.addEventListener('click', () => {
      const parent = item.closest('.tree');
      if (!parent) return;
      parent.querySelectorAll('.tree-item').forEach(i => i.classList.remove('active'));
      item.classList.add('active');
    });
  });

  $$('.packet-row').forEach(row => {
    row.addEventListener('click', () => {
      const list = row.parentElement;
      list.querySelectorAll('.packet-row').forEach(r => r.classList.remove('active'));
      row.classList.add('active');
    });
  });
}
"""

VSCODE = {
    ".vscode/settings.json": '{\n  "editor.formatOnSave": true,\n  "editor.defaultFormatter": "esbenp.prettier-vscode",\n  "liveServer.settings.port": 5500\n}\n',
    ".vscode/extensions.json": '{\n  "recommendations": [\n    "ritwickdey.liveserver",\n    "esbenp.prettier-vscode",\n    "christian-kohler.path-intellisense",\n    "usernamehw.errorlens"\n  ]\n}\n',
    ".gitignore": ".DS_Store\nnode_modules/\n*.log\n.vscode/*\n!.vscode/settings.json\n!.vscode/extensions.json\n",
}

# ================================================================
# 主流程
# ================================================================

def main():
    print(f"▶ 创建项目: {ROOT}")
    ROOT.mkdir(parents=True, exist_ok=True)
    for d in DIRS:
        (ROOT / d).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {d}/")

    (ROOT / "index.html").write_text(INDEX_HTML, encoding="utf-8")
    print(f"  + index.html ({len(INDEX_HTML)} 字符)")

    all_files = {**STYLES, **JS, **VSCODE}
    for rel, content in all_files.items():
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
    print("  code .")
    print("  右键 index.html → Open with Live Server")
    print("  或: python -m http.server 8000")


if __name__ == "__main__":
    main()