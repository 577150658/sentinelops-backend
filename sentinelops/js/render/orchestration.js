import { escapeHtml } from '../utils.js';

// ============================================================
// 基础工具
// ============================================================

function riskSev(r) {
  return { low:'low', medium:'med', med:'med', high:'high', critical:'crit', crit:'crit' }[r] || 'info';
}

function stTag(s) {
  return {
    running:  ['running', '运行中'],
    blocked:  ['blocked', '待审批'],
    done:     ['done', '已完成'],
    queued:   ['queued', '待执行'],
    stopped:  ['fp', '已停止'],
    rejected: ['fp', '已拒绝'],
  }[s] || ['queued', s];
}

const STAGES = ['侦察', '扫描', '枚举', '利用', '后渗透', '报告'];

// ============================================================
// 全部任务表格
// ============================================================
export function renderOrchestration(state) {
  const tbody = document.getElementById('orch-tbody');
  if (!tbody) return;

  if (!state.tasks?.length) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;color:var(--muted);padding:30px">暂无任务</td></tr>`;
    return;
  }

  tbody.innerHTML = state.tasks.map(t => {
    const [cls, txt] = stTag(t.status);
    return `
      <tr>
        <td class="mono">${t.id}</td>
        <td>${escapeHtml(t.title)}</td>
        <td>${t.phase}</td>
        <td><span class="tag tag--${cls}">${txt}</span></td>
        <td><span class="sev sev--${riskSev(t.risk)}">${t.risk}</span></td>
        <td class="mono">${t.agent}</td>
      </tr>
    `;
  }).join('');
}

// ============================================================
// 审批面板
// ============================================================
export function renderApprovals(state) {
  const panel = document.getElementById('approval-container');
  if (!panel) return;

  if (!state.approvals?.length) {
    panel.innerHTML = `<div class="card"><div class="card-body" style="text-align:center;color:var(--muted);font-size:12px;padding:24px">当前没有待审批事项</div></div>`;
    return;
  }

  panel.innerHTML = state.approvals.map(a => `
    <div class="approve" data-task-id="${a.taskId}">
      <div class="approve-title">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
          <path d="M12 9v4M12 17h.01"/>
          <path d="M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/>
        </svg>
        ${escapeHtml(a.title)}
      </div>
      <div class="approve-desc">${escapeHtml(a.desc)}</div>
      <div class="approve-cmd">${escapeHtml(a.command)}</div>
      <div class="approve-actions">
        <button class="btn btn--danger" data-action="reject" data-task-id="${a.taskId}">拒绝</button>
        <button class="btn btn--primary" data-action="approve" data-task-id="${a.taskId}">批准</button>
      </div>
    </div>
  `).join('');
}

// ============================================================
// 编排视图（泳道 + 依赖连线 + 统计 + 筛选）
// ============================================================

let currentFilter = { status: 'all', phase: 'all', source: 'all' };
let selectedTaskId = null;

// 从 task 对象派生依赖
function getDeps(task) {
  if (!task) return [];
  if (Array.isArray(task.depends_on)) return task.depends_on;
  if (typeof task.depends_on === 'string' && task.depends_on) {
    return task.depends_on.split(',').map(s => s.trim()).filter(Boolean);
  }
  // 兼容旧字段
  if (Array.isArray(task.dependsOn)) return task.dependsOn;
  return [];
}

// 从 task 对象派生来源
function getSource(task) {
  return task.source || 'template';
}

export function renderPipeline(state) {
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
}

function renderStatChip(status, label, count) {
  return `
    <div class="orch-stat ${currentFilter.status === status ? 'active' : ''}" data-status="${status}">
      <span class="orch-stat-dot" data-status="${status}"></span>
      <span class="orch-stat-count">${count}</span>
      <span class="orch-stat-label">${label}</span>
    </div>
  `;
}

function renderTaskCard(t) {
  const deps = getDeps(t);
  const source = getSource(t);
  const [statusCls, statusTxt] = stTag(t.status);

  return `
    <div class="pipeline-task ${selectedTaskId === t.id ? 'selected' : ''}"
         data-status="${t.status}"
         data-task-id="${t.id}"
         data-stage="${t.phase}">
      <div class="pipeline-task-head">
        <span class="pipeline-task-id">${t.id}</span>
        <span class="pipeline-task-source" data-source="${source}">${
          source === 'planner' ? 'AI' : source === 'manual' ? '手动' : '模板'
        }</span>
        <span class="pipeline-task-risk" data-risk="${t.risk}">${t.risk}</span>
      </div>
      <div class="pipeline-task-title">${escapeHtml(t.title)}</div>
      <div class="pipeline-task-foot">
        <span class="pipeline-task-status">${statusTxt}</span>
        ${t.status === 'running' && t.progress != null
          ? `<span class="pipeline-task-progress">${t.progress}%</span>`
          : ''}
      </div>
      ${deps.length
        ? `<div class="pipeline-task-deps">前置：${deps.map(d => `<span>#${d}</span>`).join(' ')}</div>`
        : ''}
    </div>
  `;
}

// ============================================================
// 依赖连线
// ============================================================

function drawDependencyLines(tasks) {
  const svg = document.getElementById('pipeline-svg');
  const wrap = svg?.parentElement;
  if (!svg || !wrap) return;

  const rect = wrap.getBoundingClientRect();
  svg.setAttribute('viewBox', `0 0 ${rect.width} ${rect.height}`);
  svg.setAttribute('width', rect.width);
  svg.setAttribute('height', rect.height);
  svg.innerHTML = '';

  const taskById = new Map(tasks.map(t => [t.id, t]));
  const paths = [];

  tasks.forEach(t => {
    const deps = getDeps(t);
    if (!deps.length) return;

    const targetEl = document.querySelector(`.pipeline-task[data-task-id="${t.id}"]`);
    if (!targetEl) return;
    const targetRect = targetEl.getBoundingClientRect();

    deps.forEach(depId => {
      const dep = taskById.get(depId);
      if (!dep) return;
      const sourceEl = document.querySelector(`.pipeline-task[data-task-id="${depId}"]`);
      if (!sourceEl) return;

      const sourceRect = sourceEl.getBoundingClientRect();

      // 起点：前置任务右侧中心
      const x1 = sourceRect.right - rect.left;
      const y1 = sourceRect.top - rect.top + sourceRect.height / 2;

      // 终点：当前任务左侧中心
      const x2 = targetRect.left - rect.left;
      const y2 = targetRect.top - rect.top + targetRect.height / 2;

      // 控制点
      const dx = Math.max(20, Math.abs(x2 - x1) / 2);
      const path = `M ${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`;

      paths.push({ path, taskId: t.id, depId });
    });
  });

  svg.innerHTML = paths.map(p =>
    `<path d="${p.path}" data-task-id="${p.taskId}" data-dep-id="${p.depId}" />`
  ).join('');

  // 高亮选中任务相关的连线
  if (selectedTaskId) {
    svg.querySelectorAll(`path[data-task-id="${selectedTaskId}"], path[data-dep-id="${selectedTaskId}"]`)
      .forEach(el => el.classList.add('highlight'));
  }
}

// 窗口 resize 时重画
let resizeTimer = null;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    const tasks = window.__lastTasks || [];
    if (tasks.length) drawDependencyLines(tasks);
  }, 200);
});

// ============================================================
// 详情抽屉
// ============================================================

export function openTaskDrawer(taskId, state) {
  const task = (state.tasks || []).find(t => t.id === taskId);
  if (!task) return;

  selectedTaskId = taskId;

  let drawer = document.getElementById('task-drawer');
  if (!drawer) {
    drawer = document.createElement('div');
    drawer.id = 'task-drawer';
    drawer.className = 'task-drawer';
    document.body.appendChild(drawer);
  }

  const deps = getDeps(task);
  const source = getSource(task);
  const [statusCls, statusTxt] = stTag(task.status);

  const canApprove = task.status === 'blocked';
  const canReject  = task.status === 'blocked';
  const canRetry   = ['stopped', 'rejected'].includes(task.status);

  drawer.innerHTML = `
    <div class="task-drawer-head">
      <span class="pipeline-task-id" style="font-size:11px">${task.id}</span>
      <h3>任务详情</h3>
      <button class="task-drawer-close" data-action="close-drawer">×</button>
    </div>
    <div class="task-drawer-body">
      <div class="task-drawer-section">
        <div class="task-drawer-section-title">标题</div>
        <div style="font-size:13px;line-height:1.6">${escapeHtml(task.title)}</div>
      </div>

      <div class="task-drawer-section">
        <div class="task-drawer-section-title">状态</div>
        <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
          <span class="tag tag--${statusCls}">${statusTxt}</span>
          <span class="pipeline-task-source" data-source="${source}">${
            source === 'planner' ? 'AI 生成' : source === 'manual' ? '人工添加' : '模板生成'
          }</span>
          <span class="pipeline-task-risk" data-risk="${task.risk}" style="font-size:10px">${task.risk}</span>
        </div>
      </div>

      <div class="task-drawer-section">
        <div class="task-drawer-section-title">基本信息</div>
        <div class="kv"><span class="kv-key">阶段</span><span class="kv-val">${task.phase}</span></div>
        <div class="kv"><span class="kv-key">执行者</span><span class="kv-val">${task.agent}</span></div>
        ${task.progress != null
          ? `<div class="kv"><span class="kv-key">进度</span><span class="kv-val">${task.progress}%</span></div>`
          : ''}
      </div>

      ${deps.length ? `
        <div class="task-drawer-section">
          <div class="task-drawer-section-title">前置依赖</div>
          <div class="task-drawer-deps">
            ${deps.map(d => `<span class="task-drawer-dep" data-jump-task="${d}">#${d}</span>`).join('')}
          </div>
        </div>
      ` : ''}

      ${task.command ? `
        <div class="task-drawer-section">
          <div class="task-drawer-section-title">命令</div>
          <div class="task-drawer-cmd">${escapeHtml(task.command)}</div>
        </div>
      ` : ''}
    </div>
    <div class="task-drawer-foot">
      ${canApprove ? `
        <button class="btn btn--danger" data-action="reject" data-task-id="${task.id}">拒绝</button>
        <button class="btn btn--primary" data-action="approve" data-task-id="${task.id}">批准执行</button>
      ` : canRetry ? `
        <button class="btn" data-action="close-drawer">关闭</button>
        <button class="btn btn--primary" data-action="retry-task" data-task-id="${task.id}">重试</button>
      ` : `
        <button class="btn" data-action="close-drawer">关闭</button>
      `}
    </div>
  `;

  requestAnimationFrame(() => drawer.classList.add('show'));
}

export function closeTaskDrawer() {
  const drawer = document.getElementById('task-drawer');
  if (drawer) drawer.classList.remove('show');
  selectedTaskId = null;
}

export function setPipelineFilter(filter) {
  Object.assign(currentFilter, filter);
}

export function getPipelineFilter() {
  return { ...currentFilter };
}

// ============================================================
// 默认 Planner 日志
// ============================================================

const DEFAULT_LOG = [
  { time: '09:41:30', level: 'info', text: '接收目标范围：12 个资产，3 个域名 + 9 个 IP 段' },
  { time: '09:41:45', level: 'cmd',  text: 'Planner → 生成侦察任务 0347（子域枚举）' },
  { time: '09:42:11', level: 'info', text: '侦察完成，发现 3 个子域：api / files / mail' },
  { time: '09:42:30', level: 'cmd',  text: 'Planner → 基于子域列表生成扫描任务 0341（Nmap）' },
  { time: '09:43:02', level: 'warn', text: 'Nmap 发现 Redis 6379 未授权，触发利用任务 0342' },
  { time: '09:43:15', level: 'warn', text: '利用类任务需人工审批，0342 / 0343 已挂起' },
  { time: '09:43:40', level: 'info', text: '目录爆破发现 /admin，触发利用任务 0346（SQL 注入）' },
  { time: '09:43:42', level: 'dim',  text: '等待审批放行，暂不生成后续任务' },
];
