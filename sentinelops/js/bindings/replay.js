import { MockAPI } from '../data/mock-api.js';
import { Store } from '../core/store.js';
import { Toast } from '../core/toast.js';

export function bindReplay() {
  document.addEventListener('click', async (e) => {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;
    const action = btn.dataset.action;

    if (action === 'replay-traffic' || action === 'replay-modified') {
      const target = btn.dataset.target || '/v2/user/1001';
      const modified = action === 'replay-modified';

      btn.disabled = true;
      try {
        const r = await MockAPI.replayTraffic(target, modified);
        Toast.show(`重放成功 · 状态 ${r.status}${modified ? '（已修改）' : ''}`, 'success');
        const auditLogs = await MockAPI.fetchAuditLogs();
        Store.set({ auditLogs });
      } catch (err) {
        Toast.show('重放失败：' + err.message, 'error');
      } finally {
        btn.disabled = false;
      }
    }

    if (action === 'generate-poc') {
      const target = btn.dataset.target || '';
      Toast.show(`已生成 PoC 到 /uploads/`, 'info');
    }
  });
}
