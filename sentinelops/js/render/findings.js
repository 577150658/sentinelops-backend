import { escapeHtml } from '../utils.js';

function sevClass(s) {
  return { critical: 'crit', high: 'high', med: 'med', medium: 'med', low: 'low' }[s] || 'info';
}

export function renderFindings(state) {
  const tbody = document.getElementById('findings-tbody');
  if (!tbody) return;

  // 加载态
  if (state.loading && !state.findings?.length) {
    const cols = 6;
    const rows = 5;
    const widths = ['60%', '90%', '70%', '40%', '50%', '60%'];
    const cells = Array.from({ length: cols }, (_, i) =>
      `<td><div class="skeleton skeleton-row" style="width:${widths[i % widths.length]}"></div></td>`
    ).join('');
    tbody.innerHTML = Array.from({ length: rows }, () =>
      `<tr class="table-loading">${cells}</tr>`
    ).join('');
    return;
  }

  // 空态
  if (!state.findings?.length) {
    tbody.innerHTML = `
      <tr>
        <td colspan="6">
          <div style="text-align:center;color:var(--muted);padding:40px 20px">
            <div style="font-size:28px;opacity:.4;margin-bottom:8px">⛨</div>
            <div style="font-size:12.5px">暂无漏洞发现</div>
            <div style="font-size:11px;margin-top:4px;opacity:.7">运行扫描任务后，发现的漏洞会出现在这里</div>
          </div>
        </td>
      </tr>
    `;
    return;
  }

  // 正常渲染
  tbody.innerHTML = state.findings.map(f => `
    <tr>
      <td><span class="sev sev--${sevClass(f.severity)}">${f.severity}</span></td>
      <td>${escapeHtml(f.title)}</td>
      <td class="mono">${escapeHtml(f.target)}</td>
      <td><span class="tag tag--${f.status === 'verified' ? 'verified' : f.status === 'pending' ? 'pending' : 'fp'}">${
        f.status === 'verified' ? '已验证' : f.status === 'pending' ? '待验证' : '误报'
      }</span></td>
      <td class="mono">${f.cvss}</td>
      <td class="mono">${escapeHtml(f.tool)}</td>
    </tr>
  `).join('');
}
