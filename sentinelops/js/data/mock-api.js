import { CONFIG, apiUrl, engagementPath } from '../config.js';

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
