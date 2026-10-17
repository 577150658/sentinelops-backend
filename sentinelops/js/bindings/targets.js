import { MockAPI } from '../data/mock-api.js';
import { Store } from '../core/store.js';
import { Toast } from '../core/toast.js';
import { openModal } from '../core/modal.js';

export function bindTargets() {
  document.addEventListener('click', async (e) => {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;
    const action = btn.dataset.action;

    if (action === 'open-add-target') {
      openModal({
        title: '添加目标',
        icon: '◎',
        confirmText: '添加',
        fields: [
          {
            key: 'target',
            label: '目标',
            placeholder: '如 api.acme.com 或 10.0.3.0/24',
            required: true,
          },
          {
            key: 'type',
            label: '类型',
            placeholder: '域名 或 网段',
            default: '域名',
          },
          {
            key: 'owner',
            label: '资产归属',
            placeholder: '如 核心业务',
          },
        ],
        onConfirm: async (data) => {
          try {
            const r = await MockAPI.addTarget({
              target: data.target,
              type: data.type || '域名',
              owner: data.owner || '',
            });
            Toast.show(`已添加目标 ${r.id}：${r.target}`, 'success');

            const targets = await MockAPI.fetchTargets();
            Store.set({ targets });
          } catch (err) {
            Toast.show('添加失败：' + err.message, 'error');
            return false;
          }
        },
      });
    }
  });
}
