#!/usr/bin/env python3
"""
patch_pipeline_simple.py
1. 恢复任务数据（后端 seed + 前端 seed）
2. 编排视图只保留 Planner 决策日志，去掉泳道
"""

import sys
import re
from pathlib import Path


def resolve_paths():
    if len(sys.argv) >= 3:
        return Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()

    print("=" * 60)
    print("修复任务编排")
    print("=" * 60)
    print()
    front = input("前端目录（含 index.html）: ").strip().strip('"').strip("'")
    back = input("后端目录（含 app/）: ").strip().strip('"').strip("'")
    print()
    return Path(front).resolve(), Path(back).resolve()


def main():
    front, back = resolve_paths()

    print(f"▶ 前端: {front}")
    print(f"▶ 后端: {back}")
    print()

    # ============================================================
    # 1. 后端 seed.py：恢复 8 个任务
    # ============================================================
    seed_py = back / "app" / "db" / "seed.py"
    if seed_py.exists():
        content = seed_py.read_text(encoding="utf-8")

        new_tasks = '''tasks = [
            Task(id="0347", title="子域枚举 acme.com", phase="侦察",
                 status="done", risk="low", agent="recon-01",
                 progress=100, source="template", depends_on=""),
            Task(id="0348", title="HTTP 响应指纹采集", phase="侦察",
                 status="done", risk="low", agent="recon-01",
                 progress=100, source="template", depends_on=""),
            Task(id="0341", title="Nmap 全端口扫描 10.0.3.0/24", phase="扫描",
                 status="running", risk="low", agent="recon-02",
                 progress=72, source="planner", depends_on="0347"),
            Task(id="0344", title="Nuclei 模板扫描 api.acme.com", phase="扫描",
                 status="done", risk="low", agent="scan-03",
                 progress=100, source="planner", depends_on="0347"),
            Task(id="0345", title="目录爆破 /admin 路径", phase="枚举",
                 status="done", risk="medium", agent="fuzz-01",
                 progress=100, source="planner", depends_on="0347"),
            Task(id="0342", title="Redis 未授权访问验证", phase="利用",
                 status="blocked", risk="critical", agent="exploit-01",
                 progress=0, source="planner", depends_on="0341",
                 command="redis-cli -h 10.0.3.44 -p 6379 INFO keyspace"),
            Task(id="0343", title="SSH 弱口令爆破 10.0.5.12", phase="利用",
                 status="blocked", risk="high", agent="exploit-01",
                 progress=0, source="planner", depends_on="0341",
                 command="hydra -l admin -P /wordlists/top1k.txt 10.0.5.12 ssh"),
            Task(id="0346", title="API 端点 SQL 注入验证", phase="利用",
                 status="done", risk="critical", agent="exploit-02",
                 progress=100, source="planner", depends_on="0344,0345",
                 command="sqlmap -u https://api.acme.com/v1/search?q=1 --batch"),
        ]'''

        pattern = r'tasks\s*=\s*\[.*?\n\s*\]'
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, new_tasks, content, count=1, flags=re.DOTALL)
            seed_py.write_text(content, encoding="utf-8")
            print("  ✓ 后端 app/db/seed.py：8 个任务已恢复")
        else:
            print("  ⚠ 没找到 tasks = [...] 块")
    else:
        print("  ⚠ 找不到 app/db/seed.py")

    # ============================================================
    # 2. 前端 render/orchestration.js：精简 renderPipeline
    #    只保留 Planner 日志，去掉泳道
    # ============================================================
    orch_js = front / "js" / "render" / "orchestration.js"
    if orch_js.exists():
        content = orch_js.read_text(encoding="utf-8")

        # 替换 renderPipeline 函数整体
        new_render_pipeline = '''export function renderPipeline(state) {
  const container = document.getElementById('pipeline-view');
  if (!container) return;

  // 只保留 Planner 决策日志
  container.innerHTML = `
    <div class="section" style="margin:0">
      <div class="section-head">
        <span class="dot dot--busy"></span>
        <span class="section-title">Planner 决策日志</span>
        <span class="section-sub">DeepSeek-Reasoner · 编排推理</span>
      </div>
      <div style="padding:12px">
        <div class="planner-log">
          ${(state.plannerLog || DEFAULT_LOG).map(l => `
            <div class="planner-log-line t-${l.level || 'dim'}">[${l.time}] ${escapeHtml(l.text)}</div>
          `).join('')}
        </div>
      </div>
    </div>
  `;
}'''

        # 匹配原 renderPipeline 函数（从 export function renderPipeline 到下一个 export 或 EOF）
        pattern = r'export function renderPipeline\(state\) \{.*?\n\}'
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, new_render_pipeline, content, count=1, flags=re.DOTALL)
            orch_js.write_text(content, encoding="utf-8")
            print("  ✓ 前端 orchestration.js：renderPipeline 已精简（只留 Planner 日志）")
        else:
            print("  ⚠ 没找到 renderPipeline 函数")
    else:
        print("  ⚠ 找不到 js/render/orchestration.js")

    # ============================================================
    # 3. 前端 seed.js：恢复 pipelineTasks（供「全部任务」使用）
    # ============================================================
    seed_js = front / "js" / "data" / "seed.js"
    if seed_js.exists():
        content = seed_js.read_text(encoding="utf-8")

        new_pipeline_tasks = '''export const pipelineTasks = [
  { id: '0347', title: '子域枚举 acme.com',           phase: '侦察', status: 'done',    risk: 'low',      agent: 'recon-01',   progress: 100, source: 'template', depends_on: [] },
  { id: '0348', title: 'HTTP 响应指纹采集',           phase: '侦察', status: 'done',    risk: 'low',      agent: 'recon-01',   progress: 100, source: 'template', depends_on: [] },
  { id: '0341', title: 'Nmap 全端口扫描 10.0.3.0/24', phase: '扫描', status: 'running', risk: 'low',      agent: 'recon-02',   progress: 72,  source: 'planner',  depends_on: ['0347'] },
  { id: '0344', title: 'Nuclei 模板扫描 api.acme.com', phase: '扫描', status: 'done',    risk: 'low',      agent: 'scan-03',    progress: 100, source: 'planner',  depends_on: ['0347'] },
  { id: '0345', title: '目录爆破 /admin 路径',         phase: '枚举', status: 'done',    risk: 'medium',   agent: 'fuzz-01',    progress: 100, source: 'planner',  depends_on: ['0347'] },
  { id: '0342', title: 'Redis 未授权访问验证',         phase: '利用', status: 'blocked', risk: 'critical', agent: 'exploit-01', progress: 0,   source: 'planner',  depends_on: ['0341'], command: 'redis-cli -h 10.0.3.44 -p 6379 INFO keyspace' },
  { id: '0343', title: 'SSH 弱口令爆破 10.0.5.12',     phase: '利用', status: 'blocked', risk: 'high',     agent: 'exploit-01', progress: 0,   source: 'planner',  depends_on: ['0341'], command: 'hydra -l admin -P top1k.txt 10.0.5.12 ssh' },
  { id: '0346', title: 'API 端点 SQL 注入验证',         phase: '利用', status: 'done',    risk: 'critical', agent: 'exploit-02', progress: 100, source: 'planner',  depends_on: ['0344', '0345'], command: 'sqlmap -u https://api.acme.com/v1/search?q=1 --batch' },
];'''

        pattern = r'export const pipelineTasks\s*=\s*\[.*?\];'
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, new_pipeline_tasks, content, count=1, flags=re.DOTALL)
            seed_js.write_text(content, encoding="utf-8")
            print("  ✓ 前端 seed.js：pipelineTasks 已恢复")
        else:
            # 没有的话追加
            seed_js.write_text(content.rstrip() + "\n\n" + new_pipeline_tasks + "\n", encoding="utf-8")
            print("  ✓ 前端 seed.js：已追加 pipelineTasks")
    else:
        print("  ⚠ 找不到 js/data/seed.js")

    # ============================================================
    # 4. 前端 main.js：恢复合并 pipelineTasks 的逻辑
    # ============================================================
    main_js = front / "js" / "main.js"
    if main_js.exists():
        content = main_js.read_text(encoding="utf-8")

        # 检查 import
        if "import { pipelineTasks }" not in content:
            content = content.replace(
                "import { Store } from './core/store.js';",
                "import { Store } from './core/store.js';\nimport { pipelineTasks } from './data/seed.js';"
            )

        # 检查合并逻辑
        if "enrichedTasks" not in content:
            # 找到 Store.set({ tasks, findings, ... }) 那一行
            old_set = "Store.set({ tasks, findings, approvals, skills, auditLogs, tools, models, reports, loading: false });"
            new_set = '''// 用 pipelineTasks 补充依赖和来源字段
    const enrichedTasks = tasks.map(t => {
      const demo = pipelineTasks.find(p => p.id === t.id);
      return demo ? { ...t, depends_on: demo.depends_on, source: demo.source } : t;
    });
    Store.set({ tasks: enrichedTasks, findings, approvals, skills, auditLogs, tools, models, reports, loading: false });'''

            if old_set in content:
                content = content.replace(old_set, new_set, 1)
            else:
                # 尝试不带 loading 的版本
                old_set2 = "Store.set({ tasks, findings, approvals, skills, auditLogs, tools, models, reports });"
                if old_set2 in content:
                    content = content.replace(old_set2, new_set.replace(", loading: false", ""), 1)

        main_js.write_text(content, encoding="utf-8")
        print("  ✓ 前端 main.js：合并逻辑已恢复")
    else:
        print("  ⚠ 找不到 js/main.js")

    # ============================================================
    # 完成
    # ============================================================
    print()
    print("=" * 60)
    print("✅ 修复完成！")
    print("=" * 60)
    print()
    print("接下来：")
    print()
    print(f"1. 重建数据库：")
    print(f"   cd {back}")
    print("   del sentinelops.db")
    print("   python run.py")
    print()
    print("2. 刷新前端 Ctrl+Shift+R")
    print()
    print("预期效果：")
    print()
    print("  【全部任务】Tab")
    print("    · 显示 8 个任务的表格")
    print("    · ID、标题、阶段、状态、风险、执行者")
    print()
    print("  【编排视图】Tab")
    print("    · 只显示 Planner 决策日志")
    print("    · 没有泳道、没有卡片、没有统计条")
    print()


if __name__ == "__main__":
    main()