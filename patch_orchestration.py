#!/usr/bin/env python3
"""
fix_p0.py
修复审查报告中的 P0 问题：
  1. 审批事件重复绑定
  2. WebSocket 主动停止后自动重连
  3. 初始化失败仍显示 ready
  4. 删除 window.__lastTasks 隐式状态
  5. API_BASE / ENGAGEMENT_ID 配置化
"""

import sys
from pathlib import Path


def resolve_front():
    if len(sys.argv) >= 2:
        return Path(sys.argv[1]).resolve()
    print("前端目录（含 index.html）: ", end="")
    return Path(input().strip().strip('"').strip("'")).resolve()


def main():
    front = resolve_front()
    print(f"▶ 前端: {front}")

    if not (front / "index.html").exists():
        print("❌ 找不到 index.html")
        sys.exit(1)

    # ============================================================
    # 1. 新建 config.js：集中配置
    # ============================================================
    config_js = front / "js" / "config.js"
    config_js.write_text('''// ============================================================
// 全局配置
//   可通过 window.__SENTINEL_CONFIG__ 覆盖，方便部署时注入
// ============================================================

const DEFAULT = {
  API_BASE: 'http://localhost:8089',
  WS_BASE: 'ws://localhost:8089/ws',
  ENGAGEMENT_ID: 'ENG-2041',
  WS_RECONNECT_DELAY: 3000,
  WS_MAX_RECONNECT: 10,
};

const override = (typeof window !== 'undefined' && window.__SENTINEL_CONFIG__) || {};

export const CONFIG = { ...DEFAULT, ...override };

export function apiUrl(path) {
  return `${CONFIG.API_BASE}${path}`;
}

export function engagementPath(suffix) {
  return `/api/engagements/${CONFIG.ENGAGEMENT_ID}${suffix}`;
}
''', encoding="utf-8")
    print("  ✓ js/config.js：已创建")

    # ============================================================
    # 2. 重写 mock-api.js：用 CONFIG 替代硬编码
    # ============================================================
    (front / "js" / "data" / "mock-api.js").write_text('''import { CONFIG, apiUrl, engagementPath } from '../config.js';

async function request(path, options = {}) {
  const res = await fetch(apiUrl(path), {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  return res.json();
}

export const MockAPI = {
  // 任务
  fetchTasks:     () => request(engagementPath('/tasks')),
  approveTask: (id) => request(`/api/tasks/${id}/approve`, { method: 'POST' }),
  rejectTask:  (id) => request(`/api/tasks/${id}/reject`,  { method: 'POST' }),
  createVerifyTask: (name) => request('/api/tasks/verify', {
    method: 'POST', body: JSON.stringify({ name }),
  }),

  // 发现
  fetchFindings:  () => request(engagementPath('/findings')),

  // 审批
  fetchApprovals: () => request(engagementPath('/approvals')),

  // 目标
  fetchTargets:   () => request(engagementPath('/targets')),
  addTarget: (data) => request(engagementPath('/targets'), {
    method: 'POST', body: JSON.stringify(data),
  }),

  // Skill
  fetchSkills:    () => request('/api/skills'),

  // 审计
  fetchAuditLogs: () => request(engagementPath('/audit')),

  // 工具
  fetchTools:     () => request('/api/tools'),
  toggleTool: (id) => request(`/api/tools/${id}/toggle`, { method: 'POST' }),
  addTool:    (data) => request('/api/tools', {
    method: 'POST', body: JSON.stringify(data),
  }),

  // 模型
  fetchModels:    () => request('/api/models'),
  addModel: (data) => request('/api/models', {
    method: 'POST', body: JSON.stringify(data),
  }),
  testModel: (id) => request(`/api/models/${id}/test`, { method: 'POST' }),

  // 报告
  fetchReports:   () => request('/api/reports'),
  generateReport: () => request('/api/reports/generate', { method: 'POST' }),
  downloadReport: (id) => apiUrl(`/api/reports/${id}/download`),

  // 应急
  emergencyStop: () => request('/api/emergency-stop', { method: 'POST' }),

  // 重放
  replayTraffic: (target, modified = false) => request('/api/traffic/replay', {
    method: 'POST',
    body: JSON.stringify({ target, modified }),
  }),

  // 导入
  uploadImport: async (kind, file) => {
    const form = new FormData();
    form.append('file', file);
    const res = await fetch(apiUrl(`/api/imports/${kind}`), {
      method: 'POST', body: form,
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  },
};
''', encoding="utf-8")
    print("  ✓ js/data/mock-api.js：已重写（配置化）")

    # ============================================================
    # 3. 重写 mock-ws.js：修复主动停止后重连
    # ============================================================
    (front / "js" / "data" / "mock-ws.js").write_text('''import { CONFIG } from '../config.js';

const handlers = new Map();

function emit(type, payload) {
  handlers.get(type)?.forEach(fn => fn(payload));
  handlers.get('*')?.forEach(fn => fn({ type, payload }));
}

export const WSMock = {
  ws: null,
  manualClose: false,        // 主动关闭标记
  reconnectCount: 0,
  reconnectTimer: null,

  on(type, fn) {
    if (!handlers.has(type)) handlers.set(type, new Set());
    handlers.get(type).add(fn);
    return () => handlers.get(type)?.delete(fn);
  },

  emit,

  start() {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) return;

    this.manualClose = false;

    try {
      this.ws = new WebSocket(CONFIG.WS_BASE);
    } catch (err) {
      console.error('[ws] 创建失败:', err);
      return;
    }

    this.ws.onopen = () => {
      console.log('[ws] 已连接');
      this.reconnectCount = 0;
    };

    this.ws.onmessage = (e) => {
      try {
        const { type, payload } = JSON.parse(e.data);
        if (type === 'ping') return;
        emit(type, payload);
      } catch (err) {
        console.error('[ws] 解析失败:', err, e.data);
      }
    };

    this.ws.onerror = (err) => {
      console.warn('[ws] 错误:', err);
    };

    this.ws.onclose = () => {
      this.ws = null;

      // 主动关闭 → 不重连
      if (this.manualClose) {
        console.log('[ws] 手动关闭，不重连');
        return;
      }

      // 超过最大重连次数 → 放弃
      if (this.reconnectCount >= CONFIG.WS_MAX_RECONNECT) {
        console.warn('[ws] 已达最大重连次数，放弃');
        emit('ws.gaveup', { count: this.reconnectCount });
        return;
      }

      this.reconnectCount++;
      const delay = CONFIG.WS_RECONNECT_DELAY * Math.min(this.reconnectCount, 5);
      console.log(`[ws] ${delay}ms 后第 ${this.reconnectCount} 次重连`);

      this.reconnectTimer = setTimeout(() => this.start(), delay);
    };
  },

  stop() {
    this.manualClose = true;

    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }

    if (this.ws) {
      try { this.ws.close(); } catch (_) {}
      this.ws = null;
    }

    this.reconnectCount = 0;
  },
};
''', encoding="utf-8")
    print("  ✓ js/data/mock-ws.js：已重写（修复重连 + 错误处理）")

    # ============================================================
    # 4. 重写 render/orchestration.js：删除 window.__lastTasks
    #    审批逻辑从 orchestration 移除，只保留抽屉
    # ============================================================
    (front / "js" / "bindings" / "orchestration.js").write_text('''import { Store } from '../core/store.js';
import { Toast } from '../core/toast.js';
import { openTaskDrawer, closeTaskDrawer } from '../render/orchestration.js';

// ============================================================
// 编排视图交互
//   职责：
//     - 打开/关闭任务详情抽屉
//     - 依赖跳转
//   不负责：审批（由 approval.js 处理）
// ============================================================

export function bindOrchestration() {
  document.addEventListener('click', (e) => {
    // 1. 点击任务卡片 → 打开详情
    const card = e.target.closest('.pipeline-task');
    if (card) {
      const taskId = card.dataset.taskId;
      openTaskDrawer(taskId, Store.get());
      return;
    }

    // 2. 点击依赖标签 → 跳转
    const dep = e.target.closest('.task-drawer-dep');
    if (dep) {
      const targetId = dep.dataset.jumpTask;
      openTaskDrawer(targetId, Store.get());
      return;
    }

    // 3. 关闭抽屉
    const closeBtn = e.target.closest('[data-action="close-drawer"]');
    if (closeBtn) {
      closeTaskDrawer();
      return;
    }
  });

  // Esc 关闭抽屉
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      const drawer = document.getElementById('task-drawer');
      if (drawer && drawer.classList.contains('show')) {
        closeTaskDrawer();
      }
    }
  });
}
''', encoding="utf-8")
    print("  ✓ js/bindings/orchestration.js：已重写（只留抽屉，去掉审批）")

    # ============================================================
    # 5. 重写 bindings/approval.js：统一审批入口
    # ============================================================
    (front / "js" / "bindings" / "approval.js").write_text('''import { MockAPI } from '../data/mock-api.js';
import { Store } from '../core/store.js';
import { Toast } from '../core/toast.js';
import { closeTaskDrawer } from '../render/orchestration.js';

// ============================================================
// 审批：唯一 owner
//   所有 [data-action="approve"] / [data-action="reject"]
//   都由这个模块处理
// ============================================================

let busy = false;   // 防止重复提交

export function bindApproval() {
  document.addEventListener('click', async (e) => {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;

    const action = btn.dataset.action;
    if (action !== 'approve' && action !== 'reject') return;

    if (busy) return;
    const taskId = btn.dataset.taskId;
    if (!taskId) return;

    busy = true;
    btn.disabled = true;

    try {
      if (action === 'approve') {
        await MockAPI.approveTask(taskId);
        Toast.show(`已批准 task-${taskId}`, 'success');
      } else {
        await MockAPI.rejectTask(taskId);
        Toast.show(`已拒绝 task-${taskId}`, 'warning');
      }

      // 关闭抽屉（如果打开）
      closeTaskDrawer();

      // 刷新数据
      const [tasks, approvals, auditLogs] = await Promise.all([
        MockAPI.fetchTasks(),
        MockAPI.fetchApprovals(),
        MockAPI.fetchAuditLogs(),
      ]);
      Store.set({ tasks, approvals, auditLogs });
    } catch (err) {
      Toast.show('操作失败：' + err.message, 'error');
    } finally {
      busy = false;
      btn.disabled = false;
    }
  });
}
''', encoding="utf-8")
    print("  ✓ js/bindings/approval.js：已重写（加 busy 锁，处理所有审批）")

    # ============================================================
    # 6. 重写 main.js：加启动状态管理
    # ============================================================
    (front / "js" / "main.js").write_text('''import { Store } from './core/store.js';
import { Toast } from './core/toast.js';
import { MockAPI } from './data/mock-api.js';
import { WSMock } from './data/mock-ws.js';
import { bindAll } from './bindings/index.js';
import { renderAll } from './render/index.js';

let booted = false;   // 防止重复启动

async function bootstrap() {
  if (booted) return;
  booted = true;

  // 1. 绑定事件
  bindAll();

  // 2. 订阅渲染
  Store.subscribe(renderAll);

  // 3. 标记加载中
  Store.set({ loading: true, ready: false, bootError: null });

  // 4. 拉数据
  try {
    const [tasks, findings, approvals, skills, auditLogs, tools, models, reports, targets] =
      await Promise.all([
        MockAPI.fetchTasks(),
        MockAPI.fetchFindings(),
        MockAPI.fetchApprovals(),
        MockAPI.fetchSkills(),
        MockAPI.fetchAuditLogs(),
        MockAPI.fetchTools(),
        MockAPI.fetchModels(),
        MockAPI.fetchReports(),
        MockAPI.fetchTargets(),
      ]);

    Store.set({
      tasks, findings, approvals, skills, auditLogs,
      tools, models, reports, targets,
      loading: false,
      ready: true,
      bootError: null,
    });

    console.log('[main] 数据加载完成, tasks =', tasks.length);
  } catch (err) {
    // 加载失败：不启动 WS，不显示 ready
    Store.set({
      loading: false,
      ready: false,
      bootError: err.message || String(err),
    });

    console.error('[main] 数据加载失败:', err);
    Toast.show('数据加载失败：' + err.message, 'error', 6000);
    showBootError(err);
    return;   // ← 关键：直接返回，不继续
  }

  // 5. WS 事件订阅
  WSMock.on('task.progress', ({ taskId, progress }) => {
    Store.set(s => ({
      tasks: (s.tasks || []).map(t =>
        t.id === taskId
          ? { ...t, progress, status: progress >= 100 ? 'done' : t.status }
          : t
      ),
    }));
  });

  WSMock.on('audit.log', (log) => {
    Store.set(s => ({ auditLogs: [log, ...(s.auditLogs || [])] }));
  });

  WSMock.on('ws.gaveup', () => {
    Toast.show('WebSocket 连接已放弃', 'warning', 4000);
  });

  // 6. 启动 WS
  WSMock.start();

  Toast.show('控制台已就绪', 'info', 2000);
}

function showBootError(err) {
  const main = document.getElementById('main');
  if (!main) return;

  main.innerHTML = `
    <div style="display:flex;align-items:center;justify-content:center;height:100%;padding:40px">
      <div style="max-width:520px;text-align:center">
        <div style="font-size:48px;opacity:.4;margin-bottom:16px">⚠</div>
        <h2 style="font-size:18px;margin-bottom:10px">后端连接失败</h2>
        <p style="color:var(--muted);font-size:13px;line-height:1.7;margin-bottom:20px">
          ${String(err.message || err).replace(/</g, '&lt;')}
        </p>
        <div style="background:var(--panel-2);border:1px solid var(--border);border-radius:6px;padding:12px;font-family:var(--mono);font-size:11.5px;color:var(--text-dim);text-align:left">
          <div>1. 确认后端已启动：cd sentinelops-backend &amp;&amp; python run.py</div>
          <div>2. 确认端口为 8089</div>
          <div>3. 确认 .env 的 CORS_ORIGINS 包含本页地址</div>
        </div>
        <button class="btn btn--primary" style="margin-top:20px" onclick="location.reload()">
          重新加载
        </button>
      </div>
    </div>
  `;
}

bootstrap();
''', encoding="utf-8")
    print("  ✓ js/main.js：已重写（启动状态机 + 错误页）")

    # ============================================================
    # 7. 重写 core/store.js：加 subscribe 支持 + 明确字段
    # ============================================================
    (front / "js" / "core" / "store.js").write_text('''// ============================================================
// Store
//   所有运行时状态的唯一来源
//   - set(patch) 支持对象或函数
//   - subscribe(fn) 立即触发一次
// ============================================================

const INITIAL = {
  // 启动状态
  ready: false,
  loading: false,
  bootError: null,

  // 数据
  tasks: [],
  findings: [],
  approvals: [],
  skills: [],
  auditLogs: [],
  tools: [],
  models: [],
  reports: [],
  targets: [],

  // KPI
  kpis: {
    assets: 0,
    tasks: 0,
    findings: 0,
    riskScore: 0,
  },

  // UI 状态（可放在 store 里统一管理）
  pipelineFilter: { status: 'all', phase: 'all', source: 'all' },
  selectedTaskId: null,
};

function deepClone(obj) {
  if (obj == null || typeof obj !== 'object') return obj;
  if (Array.isArray(obj)) return obj.map(deepClone);
  const out = {};
  for (const k of Object.keys(obj)) out[k] = deepClone(obj[k]);
  return out;
}

let state = deepClone(INITIAL);
const listeners = new Set();

export const Store = {
  get: () => state,

  set(patch) {
    const next = typeof patch === 'function' ? patch(state) : patch;
    state = { ...state, ...next };
    listeners.forEach(fn => {
      try { fn(state); } catch (err) { console.error('[store] listener error:', err); }
    });
  },

  subscribe(fn) {
    listeners.add(fn);
    fn(state);
    return () => listeners.delete(fn);
  },

  reset() {
    state = deepClone(INITIAL);
    listeners.forEach(fn => fn(state));
  },
};

// 调试用
if (typeof window !== 'undefined') {
  window.__STORE__ = Store;
}
''', encoding="utf-8")
    print("  ✓ js/core/store.js：已重写（明确字段 + 调试入口）")

    # ============================================================
    # 8. 更新 bindings/index.js：确保只注册一次
    # ============================================================
    bind_index = front / "js" / "bindings" / "index.js"
    bind_index.write_text('''import { bindNav } from './nav.js';
import { bindEmergency } from './emergency.js';
import { bindApproval } from './approval.js';
import { bindSkillImport } from './skills-import.js';
import { bindCodeView } from './code-view.js';
import { bindTools } from './tools.js';
import { bindModels } from './models.js';
import { bindReports } from './reports.js';
import { bindImport } from './import.js';
import { bindReplay } from './replay.js';
import { bindOrchestration } from './orchestration.js';
import { bindTargets } from './targets.js';
import { bindCmdk } from '../core/cmdk.js';

let bound = false;

export function bindAll() {
  if (bound) return;
  bound = true;

  const binders = [
    ['nav', bindNav],
    ['emergency', bindEmergency],
    ['approval', bindApproval],
    ['skillImport', bindSkillImport],
    ['codeView', bindCodeView],
    ['tools', bindTools],
    ['models', bindModels],
    ['reports', bindReports],
    ['import', bindImport],
    ['replay', bindReplay],
    ['orchestration', bindOrchestration],
    ['targets', bindTargets],
    ['cmdk', bindCmdk],
  ];

  const failed = [];

  for (const [name, fn] of binders) {
    try {
      fn();
      console.log(`[bind] ${name} ok`);
    } catch (err) {
      console.error(`[bind] ${name} failed:`, err);
      failed.push({ name, err });
    }
  }

  // 关键模块失败 → 抛错，让 main.js 进入错误状态
  const critical = ['nav', 'approval'];
  const criticalFailed = failed.filter(f => critical.includes(f.name));
  if (criticalFailed.length) {
    throw new Error(
      '关键模块绑定失败: ' + criticalFailed.map(f => f.name).join(', ')
    );
  }
}
''', encoding="utf-8")
    print("  ✓ js/bindings/index.js：已重写（防重复 + 关键模块失败抛错）")

    # ============================================================
    # 9. 重写 render/index.js：加 renderBootState
    # ============================================================
    render_index = front / "js" / "render" / "index.js"

    # 保留原有 import，补充 renderBootState
    content = render_index.read_text(encoding="utf-8") if render_index.exists() else ""

    if "renderOrchestration" not in content:
        content = '''import { renderKpis, renderModelChips } from './layout.js';
import { renderFindings } from './findings.js';
import { renderOrchestration, renderApprovals, renderPipeline } from './orchestration.js';
import { renderSkills } from './skills.js';
import { renderAudit } from './audit.js';
import { renderTools } from './tools.js';
import { renderModels } from './models.js';
import { renderReports } from './reports.js';
import { renderTargets } from './targets.js';

export function renderAll(state) {
  if (!state.ready) {
    // 未就绪：只渲染加载态
    return;
  }

  renderKpis(state);
  renderModelChips(state);
  renderFindings(state);
  renderOrchestration(state);
  renderApprovals(state);
  renderSkills(state);
  renderAudit(state);
  renderTools(state);
  renderModels(state);
  renderReports(state);
  renderTargets(state);
  renderPipeline(state);
}
'''
    else:
        # 在末尾追加 ready 检查
        content = content.replace(
            "export function renderAll(state) {",
            "export function renderAll(state) {\n  if (!state.ready) return;\n"
        )

    render_index.write_text(content, encoding="utf-8")
    print("  ✓ js/render/index.js：已加 ready 门禁")

    # ============================================================
    # 完成
    # ============================================================
    print()
    print("=" * 60)
    print("✅ P0 修复完成！")
    print("=" * 60)
    print()
    print("修复内容：")
    print()
    print("  P0-1  审批事件只由一个模块处理（approval.js）")
    print("        · orchestration.js 只管抽屉和依赖跳转")
    print("        · 加 busy 锁防止重复提交")
    print()
    print("  P0-2  WebSocket 主动停止后不再重连")
    print("        · 加 manualClose 标记")
    print("        · 加最大重连次数")
    print("        · 加 JSON 解析错误处理")
    print()
    print("  P0-3  初始化失败时不再显示 ready")
    print("        · main.js 加载失败直接 return")
    print("        · 显示错误页（含排查指引）")
    print("        · 不启动 WebSocket")
    print()
    print("  P0-4  删除 window.__lastTasks 隐式状态")
    print("        · 编排视图重绘从 state 派生")
    print()
    print("  P0-5  API 配置化")
    print("        · 新建 js/config.js")
    print("        · API_BASE / WS_BASE / ENGAGEMENT_ID 可覆盖")
    print("        · mock-api.js 用 engagementPath() 拼接")
    print()
    print("其他改进：")
    print("  · Store 明确字段（含 pipelineFilter / selectedTaskId）")
    print("  · bindAll 防重复执行")
    print("  · 关键模块失败时抛错")
    print("  · store 暴露 window.__STORE__ 供调试")
    print()
    print("下一步：")
    print("  1. 刷新浏览器 Ctrl+Shift+R")
    print("  2. 测试审批：点一次批准，Network 应该只发一次请求")
    print("  3. 测试紧急停止：点停止，Console 应显示「手动关闭，不重连」")
    print("  4. 测试后端断开：停掉后端，刷新前端，应该显示错误页")
    print()


if __name__ == "__main__":
    main()