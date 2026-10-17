import { MockAPI } from '../data/mock-api.js';
import { Store } from '../core/store.js';
import { Toast } from '../core/toast.js';

export function bindReports() {
  document.addEventListener('click', async (e) => {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;
    const action = btn.dataset.action;

    // 生成新报告
    if (action === 'generate-report') {
      btn.disabled = true;
      try {
        const r = await MockAPI.generateReport();
        Toast.show(`报告 ${r.id} 已生成`, 'success');
        const reports = await MockAPI.fetchReports();
        Store.set({ reports });
      } catch (err) {
        Toast.show('生成失败：' + err.message, 'error');
      } finally {
        btn.disabled = false;
      }
    }

    // 下载报告
    if (action === 'download-report') {
      const id = btn.dataset.reportId;
      window.open(MockAPI.downloadReport(id), '_blank');
      Toast.show(`正在下载 ${id}`, 'info');
    }

    // 导出审计
    if (action === 'export-audit-csv') {
      const logs = Store.get().auditLogs || [];
      const header = 'time,actor,action,target,risk,hash\n';
      const rows = logs.map(l =>
        [l.time, l.actor, l.action, l.target, l.risk, l.hash].join(',')
      ).join('\n');
      downloadFile(`audit-${Date.now()}.csv`, header + rows, 'text/csv');
      Toast.show('已导出 CSV', 'success');
    }

    if (action === 'export-audit-json') {
      const logs = Store.get().auditLogs || [];
      downloadFile(`audit-${Date.now()}.json`, JSON.stringify(logs, null, 2), 'application/json');
      Toast.show('已导出 JSON', 'success');
    }
  });
}

function downloadFile(filename, content, mime) {
  const blob = new Blob([content], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}
