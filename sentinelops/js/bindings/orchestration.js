import { Store } from '../core/store.js';
import { Toast } from '../core/toast.js';
import { openTaskDrawer, closeTaskDrawer } from '../render/orchestration.js';

// ============================================================
// 编排视图交互
//   职责：
//     - 打开/关闭任务详情抽屉
//     - 依赖跳转
//   不负责：审批（由 approval.js 处理）
// ============================================================

export function bindOrchestration() {
  document.addEventListener('click', (e) => {
    // 1. 点击任务卡片 → 打开详情
    const card = e.target.closest('.pipeline-task');
    if (card) {
      const taskId = card.dataset.taskId;
      openTaskDrawer(taskId, Store.get());
      return;
    }

    // 2. 点击依赖标签 → 跳转
    const dep = e.target.closest('.task-drawer-dep');
    if (dep) {
      const targetId = dep.dataset.jumpTask;
      openTaskDrawer(targetId, Store.get());
      return;
    }

    // 3. 关闭抽屉
    const closeBtn = e.target.closest('[data-action="close-drawer"]');
    if (closeBtn) {
      closeTaskDrawer();
      return;
    }
  });

  // Esc 关闭抽屉
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      const drawer = document.getElementById('task-drawer');
      if (drawer && drawer.classList.contains('show')) {
        closeTaskDrawer();
      }
    }
  });
}
