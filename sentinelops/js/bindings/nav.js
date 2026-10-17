import { $$ } from '../utils.js';

export function bindNav() {
  const navItems = $$('.nav-item[data-page]');
  const pages    = $$('.page');
  const mainEl   = document.getElementById('main');

  function go(pageId) {
    navItems.forEach(i => i.classList.toggle('active', i.dataset.page === pageId));
    pages.forEach(p => { p.hidden = (p.id !== 'page-' + pageId); });
    if (mainEl) mainEl.scrollTop = 0;
  }

  navItems.forEach(item => {
    item.addEventListener('click', () => go(item.dataset.page));
  });

  document.querySelectorAll('.tabs[data-tabs]').forEach(group => {
    const groupName = group.dataset.tabs;
    group.querySelectorAll('.tab').forEach(tab => {
      tab.addEventListener('click', () => {
        group.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        const container = document.querySelector(`[data-tab-group="${groupName}"]`);
        if (!container) return;
        container.querySelectorAll('.tab-panel').forEach(p => { p.hidden = true; });
        const target = document.getElementById(tab.dataset.panel);
        if (target) target.hidden = false;
      });
    });
  });

  window.go = go;
}
