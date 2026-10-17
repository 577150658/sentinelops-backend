import { CONFIG } from '../config.js';

const handlers = new Map();

function emit(type, payload) {
  handlers.get(type)?.forEach(fn => fn(payload));
  handlers.get('*')?.forEach(fn => fn({ type, payload }));
}

export const WSMock = {
  ws: null,
  manualClose: false,        // 主动关闭标记
  reconnectCount: 0,
  reconnectTimer: null,

  on(type, fn) {
    if (!handlers.has(type)) handlers.set(type, new Set());
    handlers.get(type).add(fn);
    return () => handlers.get(type)?.delete(fn);
  },

  emit,

  start() {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) return;

    this.manualClose = false;

    try {
      this.ws = new WebSocket(CONFIG.WS_BASE);
    } catch (err) {
      console.error('[ws] 创建失败:', err);
      return;
    }

    this.ws.onopen = () => {
      console.log('[ws] 已连接');
      this.reconnectCount = 0;
    };

    this.ws.onmessage = (e) => {
      try {
        const { type, payload } = JSON.parse(e.data);
        if (type === 'ping') return;
        emit(type, payload);
      } catch (err) {
        console.error('[ws] 解析失败:', err, e.data);
      }
    };

    this.ws.onerror = (err) => {
      console.warn('[ws] 错误:', err);
    };

    this.ws.onclose = () => {
      this.ws = null;

      // 主动关闭 → 不重连
      if (this.manualClose) {
        console.log('[ws] 手动关闭，不重连');
        return;
      }

      // 超过最大重连次数 → 放弃
      if (this.reconnectCount >= CONFIG.WS_MAX_RECONNECT) {
        console.warn('[ws] 已达最大重连次数，放弃');
        emit('ws.gaveup', { count: this.reconnectCount });
        return;
      }

      this.reconnectCount++;
      const delay = CONFIG.WS_RECONNECT_DELAY * Math.min(this.reconnectCount, 5);
      console.log(`[ws] ${delay}ms 后第 ${this.reconnectCount} 次重连`);

      this.reconnectTimer = setTimeout(() => this.start(), delay);
    };
  },

  stop() {
    this.manualClose = true;

    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }

    if (this.ws) {
      try { this.ws.close(); } catch (_) {}
      this.ws = null;
    }

    this.reconnectCount = 0;
  },
};
