import { escapeHtml } from '../utils.js';

export function renderReports(state) {
  const container = document.getElementById('reports-list');
  if (!container) return;

  if (!state.reports?.length) {
    container.innerHTML = `<div style="color:var(--muted);padding:30px;text-align:center">暂无报告</div>`;
    return;
  }

  container.innerHTML = state.reports.map(r => `
    <div class="report-item" data-report-id="${r.id}">
      <div class="report-icon">📄</div>
      <div style="flex:1;min-width:0">
        <div style="font-size:12.5px;font-weight:600">${escapeHtml(r.title)}</div>
        <div class="mono" style="font-size:11px;color:var(--muted);margin-top:2px">${r.fmt} · ${r.created} · ${r.size}</div>
      </div>
      <span class="tag tag--${r.status === 'ready' ? 'done' : 'running'}">${r.status === 'ready' ? '已生成' : '生成中'}</span>
      ${r.status === 'ready'
        ? `<button class="btn" style="height:28px;font-size:11px" data-action="download-report" data-report-id="${r.id}">下载</button>`
        : `<button class="btn" style="height:28px;font-size:11px" disabled>下载</button>`}
    </div>
  `).join('');
}
