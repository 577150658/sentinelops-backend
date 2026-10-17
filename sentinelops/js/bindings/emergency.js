import { MockAPI } from '../data/mock-api.js';
import { Store } from '../core/store.js';
import { Toast } from '../core/toast.js';
import { WSMock } from '../data/mock-ws.js';

export function bindEmergency() {
  const overlay = document.getElementById('stopOverlay');
  if (!overlay) return;

  window.openStop = () => overlay.classList.add('show');
  window.closeStop = () => overlay.classList.remove('show');

  const confirmBtn = overlay.querySelector('.btn--danger');
  confirmBtn?.addEventListener('click', async () => {
    try {
      await MockAPI.emergencyStop();
      WSMock.stop();
      Toast.show('已执行紧急停止', 'error', 4000);

      const [tasks, auditLogs] = await Promise.all([
        MockAPI.fetchTasks(),
        MockAPI.fetchAuditLogs(),
      ]);
      Store.set({ tasks, auditLogs });
    } catch (err) {
      Toast.show('停止失败：' + err.message, 'error');
    } finally {
      overlay.classList.remove('show');
    }
  });
}