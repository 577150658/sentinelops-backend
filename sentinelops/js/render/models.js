import { escapeHtml } from '../utils.js';

export function renderModels(state) {
  const grid = document.getElementById('models-grid');
  if (!grid) return;

  if (!state.models?.length) {
    grid.innerHTML = `<div style="color:var(--muted);padding:30px;text-align:center">暂无模型</div>`;
    return;
  }

  grid.innerHTML = state.models.map(m => `
    <div class="model-card" data-model-id="${m.id}">
      <div class="model-card-head">
        <span class="dot dot--${m.status === 'online' ? 'on' : m.status === 'busy' ? 'busy' : 'off'}"></span>
        <div>
          <div class="model-card-name">${escapeHtml(m.name)}</div>
          <div class="model-card-sub">${m.kind === 'cloud' ? '云端' : '本地'} · ${escapeHtml(m.endpoint)}</div>
        </div>
        <div class="spacer" style="flex:1"></div>
        <span class="tag tag--${m.status === 'online' ? 'done' : m.status === 'busy' ? 'running' : 'queued'}">${
          m.status === 'online' ? '在线' : m.status === 'busy' ? '推理中' : '离线'
        }</span>
      </div>
      <div class="kv"><span class="kv-key">延迟</span><span class="kv-val">${m.latency} ms</span></div>
      <div class="kv"><span class="kv-key">ID</span><span class="kv-val">${m.id}</span></div>
      <div style="display:flex;gap:8px;margin-top:10px">
        <button class="btn btn--primary" style="flex:1" data-action="test-model" data-model-id="${m.id}">连通性测试</button>
      </div>
    </div>
  `).join('');
}
