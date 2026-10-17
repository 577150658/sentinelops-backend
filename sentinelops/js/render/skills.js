import { escapeHtml } from '../utils.js';

export function renderSkills(state) {
  const grid = document.getElementById('skill-grid');
  if (!grid) return;

  grid.innerHTML = state.skills.map(s => `
    <div class="skill-card">
      <div class="skill-top">
        <div class="skill-icon">${s.icon}</div>
        <div style="flex:1;min-width:0">
          <div class="skill-name">${escapeHtml(s.name)} <span class="skill-ver">${s.version}</span></div>
          <div class="skill-author">${escapeHtml(s.author)}</div>
        </div>
      </div>
      <div class="skill-desc">${escapeHtml(s.desc)}</div>
      <div class="skill-tags">${s.tags.map(t => `<span class="skill-tag">${t}</span>`).join('')}</div>
      <div class="skill-foot">
        <span class="sev sev--${s.risk}" style="font-size:10px">${s.risk}</span>
        <span>${s.tools} 工具</span>
        <span>${s.runs} 次</span>
        <div class="toggle ${s.enabled ? 'on' : ''}"></div>
      </div>
    </div>
  `).join('');
}
