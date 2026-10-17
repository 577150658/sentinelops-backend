// ============================================================
// 命令面板（Ctrl+K）
// ============================================================

import { Router } from './router.js';

const COMMANDS = [
  { id: 'dashboard',    title: '仪表盘',       desc: '作战总览', icon: '▦', kbd: '1' },
  { id: 'engagement',   title: '目标范围',     desc: '授权与目标', icon: '◎', kbd: '2' },
  { id: 'orchestration',title: '任务编排',     desc: '编排视图', icon: '≡', kbd: '3' },
  { id: 'execution',    title: '实时执行',     desc: '子代理日志', icon: '▶', kbd: '4' },
  { id: 'findings',     title: '漏洞发现',     desc: '已验证发现', icon: '⛨', kbd: '5' },
  { id: 'js-analysis',  title: 'JS 分析',      desc: '反混淆与密钥', icon: '⟨⟩' },
  { id: 'miniapp-analysis', title: '小程序分析', desc: 'wxapkg 反编译', icon: '▢' },
  { id: 'app-analysis', title: 'App 分析',     desc: 'APK / IPA', icon: '▢' },
  { id: 'traffic-analysis', title: '抓包分析', desc: 'HTTP 流量', icon: '∿' },
  { id: 'models',       title: '模型管理',     desc: '云端 / 本地模型', icon: '◈' },
  { id: 'tools',        title: '工具管理',     desc: 'MCP 工具端点', icon: '⚙' },
  { id: 'skills',       title: 'Skill 管理',   desc: '能力包', icon: '★' },
  { id: 'audit',        title: '审计日志',     desc: '哈希链', icon: '≡' },
  { id: 'reports',      title: '报告',         desc: '生成与下载', icon: '▤' },
];

let mask = null;
let listEl = null;
let inputEl = null;
let filtered = [];
let activeIndex = 0;

function ensure() {
  if (mask && document.body.contains(mask)) return;

  mask = document.createElement('div');
  mask.className = 'cmdk-mask';
  mask.innerHTML = `
    <div class="cmdk" role="dialog" aria-modal="true">
      <input class="cmdk-input" placeholder="搜索页面或操作…（Esc 关闭）" />
      <div class="cmdk-list"></div>
    </div>
  `;
  document.body.appendChild(mask);

  inputEl = mask.querySelector('.cmdk-input');
  listEl = mask.querySelector('.cmdk-list');

  inputEl.addEventListener('input', () => {
    activeIndex = 0;
    renderList();
  });

  inputEl.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      activeIndex = Math.min(activeIndex + 1, filtered.length - 1);
      renderList();
      scrollActiveIntoView();
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      activeIndex = Math.max(activeIndex - 1, 0);
      renderList();
      scrollActiveIntoView();
    } else if (e.key === 'Enter') {
      e.preventDefault();
      runActive();
    }
  });

  mask.addEventListener('click', (e) => {
    if (e.target === mask) closeCmdk();
  });

  listEl.addEventListener('click', (e) => {
    const item = e.target.closest('.cmdk-item');
    if (!item) return;
    const id = item.dataset.id;
    const cmd = COMMANDS.find(c => c.id === id);
    if (cmd) {
      Router.go(cmd.id);
      closeCmdk();
    }
  });
}

function renderList() {
  const q = inputEl.value.trim().toLowerCase();
  filtered = !q
    ? COMMANDS.slice()
    : COMMANDS.filter(c =>
        c.title.toLowerCase().includes(q) ||
        c.desc.toLowerCase().includes(q) ||
        c.id.includes(q)
      );

  if (!filtered.length) {
    listEl.innerHTML = `<div class="cmdk-empty">没有匹配的结果</div>`;
    return;
  }

  listEl.innerHTML = filtered.map((c, i) => `
    <div class="cmdk-item ${i === activeIndex ? 'active' : ''}" data-id="${c.id}">
      <span class="cmdk-item-icon">${c.icon}</span>
      <div class="cmdk-item-body">
        <div class="cmdk-item-title">${c.title}</div>
        <div class="cmdk-item-desc">${c.desc}</div>
      </div>
      ${c.kbd ? `<span class="cmdk-item-kbd">Ctrl+${c.kbd}</span>` : ''}
    </div>
  `).join('');
}

function scrollActiveIntoView() {
  const el = listEl.querySelector('.cmdk-item.active');
  if (el) el.scrollIntoView({ block: 'nearest' });
}

function runActive() {
  const cmd = filtered[activeIndex];
  if (!cmd) return;
  Router.go(cmd.id);
  closeCmdk();
}

export function openCmdk() {
  ensure();
  mask.classList.add('show');
  inputEl.value = '';
  activeIndex = 0;
  renderList();
  setTimeout(() => inputEl.focus(), 50);
}

export function closeCmdk() {
  if (!mask) return;
  mask.classList.remove('show');
}

export function isCmdkOpen() {
  return mask && mask.classList.contains('show');
}

export function bindCmdk() {
  document.addEventListener('keydown', (e) => {
    const isMac = navigator.platform.toLowerCase().includes('mac');
    const mod = isMac ? e.metaKey : e.ctrlKey;

    // Ctrl+K 打开
    if (mod && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      if (isCmdkOpen()) closeCmdk();
      else openCmdk();
      return;
    }

    // Esc 关闭
    if (e.key === 'Escape' && isCmdkOpen()) {
      e.preventDefault();
      closeCmdk();
      return;
    }

    // Ctrl+1~9 快速切换
    if (mod && e.key >= '1' && e.key <= '9') {
      const cmd = COMMANDS.find(c => c.kbd === e.key);
      if (cmd) {
        e.preventDefault();
        Router.go(cmd.id);
      }
    }
  });
}
