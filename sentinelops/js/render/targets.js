import { escapeHtml } from '../utils.js';

export function renderTargets(state) {
  const tbody = document.getElementById('targets-tbody');
  if (!tbody) return;

  if (!state.targets?.length) {
    tbody.innerHTML = `
      <tr>
        <td colspan="5">
          <div style="text-align:center;color:var(--muted);padding:30px">
            暂无目标，点击「+ 添加目标」开始
          </div>
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = state.targets.map(t => {
    const statusCls = {
      '已扫描': 'done',
      '扫描中': 'running',
      '待扫描': 'queued',
    }[t.status] || 'queued';

    return `
      <tr>
        <td class="mono">${escapeHtml(t.target)}</td>
        <td>${escapeHtml(t.type)}</td>
        <td>${escapeHtml(t.owner || '—')}</td>
        <td><span class="tag tag--${statusCls}">${t.status}</span></td>
        <td class="mono">${t.findings}</td>
      </tr>
    `;
  }).join('');
}
