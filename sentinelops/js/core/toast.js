// ============================================================
// Toast 增强版
//   - 图标 + 关闭按钮
//   - 最多同时显示 4 条，超出时移除最旧的
//   - 相同内容 2 秒内去重
// ============================================================

const ICONS = {
  info:    'i',
  success: '✓',
  warning: '!',
  error:   '×',
};

const MAX_TOASTS = 4;
const DEDUP_WINDOW = 2000;

let container = null;
let recentMessages = new Map();

function ensure() {
  if (container && document.body.contains(container)) return container;
  container = document.createElement('div');
  container.id = 'toast-container';
  Object.assign(container.style, {
    position: 'fixed',
    top: '70px',
    right: '20px',
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
    zIndex: '200',
    pointerEvents: 'none',
  });
  document.body.appendChild(container);
  return container;
}

function dismiss(el) {
  el.classList.remove('show');
  setTimeout(() => el.remove(), 260);
}

export const Toast = {
  show(message, type = 'info', duration = 3000) {
    // 去重
    const key = `${type}:${message}`;
    const now = Date.now();
    if (recentMessages.has(key)) {
      const last = recentMessages.get(key);
      if (now - last < DEDUP_WINDOW) return;
    }
    recentMessages.set(key, now);

    // 清理过期的去重记录
    if (recentMessages.size > 30) {
      const cutoff = now - DEDUP_WINDOW * 2;
      for (const [k, t] of recentMessages.entries()) {
        if (t < cutoff) recentMessages.delete(k);
      }
    }

    const box = ensure();

    // 数量限制
    const existing = box.querySelectorAll('.toast-item');
    if (existing.length >= MAX_TOASTS) {
      dismiss(existing[0]);
    }

    const el = document.createElement('div');
    el.className = 'toast-item';
    el.dataset.type = type;
    el.innerHTML = `
      <div class="toast-icon">${ICONS[type] || ICONS.info}</div>
      <div class="toast-body"></div>
      <button class="toast-close" aria-label="close">×</button>
    `;
    el.querySelector('.toast-body').textContent = message;
    el.querySelector('.toast-close').addEventListener('click', () => dismiss(el));

    box.appendChild(el);

    requestAnimationFrame(() => {
      el.classList.add('show');
    });

    if (duration > 0) {
      setTimeout(() => dismiss(el), duration);
    }
  },
};
