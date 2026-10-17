import { escapeHtml } from '../utils.js';

export function renderTools(state) {
  const tbody = document.getElementById('tools-tbody');
  if (!tbody) return;

  if (!state.tools?.length) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;color:var(--muted);padding:30px">暂无工具</td></tr>`;
    return;
  }

  tbody.innerHTML = state.tools.map(t => `
    <tr>
      <td>${escapeHtml(t.endpoint)}</td>
      <td class="mono">${escapeHtml(t.tools)}</td>
      <td><span class="tag tag--${t.permission === '利用' ? 'blocked' : t.permission === '未知' ? 'fp' : 'pending'}">${t.permission}</span></td>
      <td><span class="tag tag--${t.signature === '已校验' ? 'verified' : t.signature === '校验失败' ? 'fp' : 'pending'}">${t.signature}</span></td>
      <td class="mono">${t.lastCall}</td>
      <td>
        <div class="toggle ${t.enabled ? 'on' : ''}" data-tool-id="${t.id}"></div>
      </td>
    </tr>
  `).join('');
}
