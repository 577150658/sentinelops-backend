// ============================================================
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
