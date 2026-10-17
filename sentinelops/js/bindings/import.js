import { MockAPI } from '../data/mock-api.js';
import { Store } from '../core/store.js';
import { Toast } from '../core/toast.js';

export function bindImport() {
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-action="import-file"]');
    if (!btn) return;
    const kind = btn.dataset.kind || 'generic';
    const accept = btn.dataset.accept || '*';

    const inp = document.createElement('input');
    inp.type = 'file';
    inp.accept = accept;
    inp.onchange = async () => {
      if (!inp.files[0]) return;
      const file = inp.files[0];
      try {
        const r = await MockAPI.uploadImport(kind, file);
        Toast.show(`已导入 ${r.filename}（${(r.size/1024).toFixed(1)} KB）`, 'success');
        // 刷新审计日志
        const auditLogs = await MockAPI.fetchAuditLogs();
        Store.set({ auditLogs });
      } catch (err) {
        Toast.show('导入失败：' + err.message, 'error');
      }
    };
    inp.click();
  });
}
