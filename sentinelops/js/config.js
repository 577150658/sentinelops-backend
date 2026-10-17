// ============================================================
// 全局配置
//   可通过 window.__SENTINEL_CONFIG__ 覆盖，方便部署时注入
// ============================================================

const DEFAULT = {
  API_BASE: 'http://localhost:8089',
  WS_BASE: 'ws://localhost:8089/ws',
  ENGAGEMENT_ID: 'ENG-2041',
  WS_RECONNECT_DELAY: 3000,
  WS_MAX_RECONNECT: 10,
};

const override = (typeof window !== 'undefined' && window.__SENTINEL_CONFIG__) || {};

export const CONFIG = { ...DEFAULT, ...override };

export function apiUrl(path) {
  return `${CONFIG.API_BASE}${path}`;
}

export function engagementPath(suffix) {
  return `/api/engagements/${CONFIG.ENGAGEMENT_ID}${suffix}`;
}
