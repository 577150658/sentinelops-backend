import { MockAPI } from '../data/mock-api.js';
import { Store } from '../core/store.js';
import { Toast } from '../core/toast.js';
import { openModal } from '../core/modal.js';

export function bindTools() {
  document.addEventListener('click', async (e) => {
    const toggle = e.target.closest('.toggle[data-tool-id]');
    const btn = e.target.closest('[data-action]');

    // toggle 开关
    if (toggle) {
      e.stopPropagation();
      const toolId = toggle.dataset.toolId;
      try {
        const r = await MockAPI.toggleTool(toolId);
        toggle.classList.toggle('on', r.enabled);
        Toast.show(`工具 ${toolId} 已${r.enabled ? '启用' : '禁用'}`, 'info');
        const tools = await MockAPI.fetchTools();
        Store.set({ tools });
      } catch (err) {
        Toast.show('切换失败：' + err.message, 'error');
      }
      return;
    }

    if (!btn) return;
    const action = btn.dataset.action;

    // 注册工具（模态框）
    if (action === 'open-add-tool') {
      openModal({
        title: '注册工具端点',
        icon: '⚙',
        confirmText: '注册',
        fields: [
          {
            key: 'endpoint',
            label: '工具端点',
            placeholder: '如 nmap-mcp-server',
            required: true,
          },
          {
            key: 'tools',
            label: '封装工具',
            placeholder: '如 Nmap, Masscan',
            hint: '多个工具用逗号分隔',
          },
          {
            key: 'permission',
            label: '权限',
            placeholder: '扫描',
            default: '扫描',
            hint: '扫描 / 利用 / 只读 / 后渗透',
          },
        ],
        onConfirm: async (data) => {
          try {
            const r = await MockAPI.addTool({
              endpoint: data.endpoint,
              tools: data.tools,
              permission: data.permission || '扫描',
              signature: '待校验',
            });
            Toast.show(`已注册 ${r.id}：${r.endpoint}`, 'success');
            const list = await MockAPI.fetchTools();
            Store.set({ tools: list });
          } catch (err) {
            Toast.show('注册失败：' + err.message, 'error');
            return false;
          }
        },
      });
      return;
    }

    // 重新加载 MCP
    if (action === 'reload-mcp') {
      btn.disabled = true;
      const original = btn.textContent;
      btn.textContent = '加载中…';
      try {
        const tools = await MockAPI.fetchTools();
        Store.set({ tools });
        Toast.show(`已重新加载 ${tools.length} 个工具端点`, 'success');
      } catch (err) {
        Toast.show('加载失败：' + err.message, 'error');
      } finally {
        btn.disabled = false;
        btn.textContent = original;
      }
    }
  });
}
