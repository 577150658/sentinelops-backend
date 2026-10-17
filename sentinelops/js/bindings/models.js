import { MockAPI } from '../data/mock-api.js';
import { Store } from '../core/store.js';
import { Toast } from '../core/toast.js';
import { openModal } from '../core/modal.js';

export function bindModels() {
  document.addEventListener('click', async (e) => {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;
    const action = btn.dataset.action;

    // 连通性测试
    if (action === 'test-model') {
      const id = btn.dataset.modelId;
      btn.disabled = true;
      btn.textContent = '测试中…';
      try {
        const r = await MockAPI.testModel(id);
        Toast.show(`${id} 在线 · 延迟 ${r.latency}ms`, 'success');
        const models = await MockAPI.fetchModels();
        Store.set({ models });
      } catch (err) {
        Toast.show('测试失败：' + err.message, 'error');
      } finally {
        btn.disabled = false;
        btn.textContent = '连通性测试';
      }
      return;
    }

    // 添加模型（模态框）
    if (action === 'open-add-model') {
      openModal({
        title: '添加模型',
        icon: '◈',
        confirmText: '添加',
        fields: [
          {
            key: 'name',
            label: '模型名称',
            placeholder: '如 Qwen2.5-14B-Instruct',
            required: true,
          },
          {
            key: 'endpoint',
            label: '端点',
            placeholder: '如 localhost:11434',
            required: true,
            hint: '云端填域名，本地填 host:port',
          },
          {
            key: 'kind',
            label: '类型',
            placeholder: 'local 或 cloud',
            default: 'local',
            hint: 'local = 本地 Ollama/vLLM；cloud = 云端 API',
          },
        ],
        onConfirm: async (data) => {
          try {
            const r = await MockAPI.addModel({
              name: data.name,
              kind: data.kind === 'cloud' ? 'cloud' : 'local',
              endpoint: data.endpoint,
            });
            Toast.show(`已添加模型 ${r.id}：${data.name}`, 'success');
            const models = await MockAPI.fetchModels();
            Store.set({ models });
          } catch (err) {
            Toast.show('添加失败：' + err.message, 'error');
            return false;
          }
        },
      });
    }
  });
}
