// ============================================================
// 通用模态框
//   UI.modal({ title, icon, fields, confirmText, onConfirm })
//   fields: [{ key, label, placeholder, hint, required, default }]
// ============================================================

let activeMask = null;

function escapeHtml(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  }[c]));
}

export function openModal({
  title = '输入',
  icon = '✎',
  fields = [],
  confirmText = '确认',
  cancelText = '取消',
  onConfirm,
} = {}) {
  closeModal();

  const mask = document.createElement('div');
  mask.className = 'ui-modal-mask';

  const fieldsHtml = fields.map(f => `
    <div class="ui-modal-field">
      <label class="ui-modal-label">
        ${escapeHtml(f.label)}
        ${f.required ? '<span class="req">*</span>' : ''}
      </label>
      <input
        class="ui-modal-input"
        data-key="${escapeHtml(f.key)}"
        type="${f.type || 'text'}"
        placeholder="${escapeHtml(f.placeholder || '')}"
        value="${escapeHtml(f.default || '')}"
        ${f.required ? 'data-required="1"' : ''}
      />
      ${f.hint ? `<div class="ui-modal-hint">${escapeHtml(f.hint)}</div>` : ''}
    </div>
  `).join('');

  mask.innerHTML = `
    <div class="ui-modal" role="dialog" aria-modal="true">
      <div class="ui-modal-head">
        <div class="ui-modal-icon">${icon}</div>
        <h3>${escapeHtml(title)}</h3>
        <button class="ui-modal-close" aria-label="close">×</button>
      </div>
      <div class="ui-modal-body">
        ${fieldsHtml}
      </div>
      <div class="ui-modal-foot">
        <button class="btn" data-action="cancel">${escapeHtml(cancelText)}</button>
        <div class="spacer"></div>
        <button class="btn btn--primary" data-action="confirm">${escapeHtml(confirmText)}</button>
      </div>
    </div>
  `;

  document.body.appendChild(mask);
  requestAnimationFrame(() => mask.classList.add('show'));
  activeMask = mask;

  const inputs = mask.querySelectorAll('.ui-modal-input');
  if (inputs.length) {
    setTimeout(() => inputs[0].focus(), 60);
  }

  function collect() {
    const data = {};
    let valid = true;
    inputs.forEach(inp => {
      const key = inp.dataset.key;
      const value = inp.value.trim();
      data[key] = value;
      if (inp.dataset.required === '1' && !value) {
        inp.classList.add('error');
        valid = false;
      } else {
        inp.classList.remove('error');
      }
    });
    return { data, valid };
  }

  async function confirm() {
    const { data, valid } = collect();
    if (!valid) {
      // 聚焦第一个空字段
      for (const inp of inputs) {
        if (inp.dataset.required === '1' && !inp.value.trim()) {
          inp.focus();
          break;
        }
      }
      return;
    }
    const result = onConfirm ? await onConfirm(data) : data;
    if (result !== false) closeModal();
  }

  mask.addEventListener('click', (e) => {
    if (e.target === mask) { closeModal(); return; }
    const btn = e.target.closest('[data-action]');
    if (!btn) return;
    if (btn.dataset.action === 'cancel') closeModal();
    else if (btn.dataset.action === 'confirm') confirm();
    else if (btn.classList.contains('ui-modal-close')) closeModal();
  });

  mask.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.target.tagName === 'INPUT') {
      e.preventDefault();
      confirm();
    }
  });
}

export function closeModal() {
  if (!activeMask) return;
  const m = activeMask;
  activeMask = null;
  m.classList.remove('show');
  setTimeout(() => m.remove(), 200);
}

export function isModalOpen() {
  return !!activeMask;
}
