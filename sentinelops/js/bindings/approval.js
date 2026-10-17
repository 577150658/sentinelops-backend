import { MockAPI } from '../data/mock-api.js';
import { Store } from '../core/store.js';
import { Toast } from '../core/toast.js';
import { closeTaskDrawer } from '../render/orchestration.js';

// ============================================================
// 审批：唯一 owner
//   所有 [data-action="approve"] / [data-action="reject"]
//   都由这个模块处理
// ============================================================

let busy = false;   // 防止重复提交

export function bindApproval() {
  document.addEventListener('click', async (e) => {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;

    const action = btn.dataset.action;
    if (action !== 'approve' && action !== 'reject') return;

    if (busy) return;
    const taskId = btn.dataset.taskId;
    if (!taskId) return;

    busy = true;
    btn.disabled = true;

    try {
      if (action === 'approve') {
        await MockAPI.approveTask(taskId);
        Toast.show(`已批准 task-${taskId}`, 'success');
      } else {
        await MockAPI.rejectTask(taskId);
        Toast.show(`已拒绝 task-${taskId}`, 'warning');
      }

      // 关闭抽屉（如果打开）
      closeTaskDrawer();

      // 刷新数据
      const [tasks, approvals, auditLogs] = await Promise.all([
        MockAPI.fetchTasks(),
        MockAPI.fetchApprovals(),
        MockAPI.fetchAuditLogs(),
      ]);
      Store.set({ tasks, approvals, auditLogs });
    } catch (err) {
      Toast.show('操作失败：' + err.message, 'error');
    } finally {
      busy = false;
      btn.disabled = false;
    }
  });
}
