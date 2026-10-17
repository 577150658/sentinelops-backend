// ============================================================
// 骨架屏工具
//   renderSkeleton(tbody, columns) —— 渲染加载中的行
// ============================================================

export function renderSkeleton(tbody, columns = 4, rows = 3) {
  if (!tbody) return;
  const cells = Array.from({ length: columns }, (_, i) => {
    const widths = ['60%', '90%', '70%', '40%', '50%'];
    const w = widths[i % widths.length];
    return `<td><div class="skeleton skeleton-row" style="width:${w}"></div></td>`;
  }).join('');
  tbody.innerHTML = Array.from({ length: rows }, () =>
    `<tr class="table-loading">${cells}</tr>`
  ).join('');
}
