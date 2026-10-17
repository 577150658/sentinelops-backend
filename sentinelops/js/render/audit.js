import { escapeHtml } from '../utils.js';

export function renderAudit(state) {
  const tbody = document.getElementById('audit-tbody');
  if (!tbody) return;

  tbody.innerHTML = state.auditLogs.map(l => `
    <tr>
      <td class="mono">${l.time}</td>
      <td>${l.actor}</td>
      <td><span class="tag tag--done">${l.action}</span></td>
      <td class="mono">${escapeHtml(l.target)}</td>
      <td><span class="sev sev--${l.risk}">${l.risk}</span></td>
      <td class="mono">${l.hash}</td>
    </tr>
  `).join('');
}