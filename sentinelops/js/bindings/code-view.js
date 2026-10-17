import { $$ } from '../utils.js';

export function bindCodeView() {
  $$('.code-view').forEach(view => {
    view.querySelectorAll('.code-line').forEach(line => {
      line.addEventListener('click', () => {
        view.querySelectorAll('.code-line').forEach(l => l.classList.remove('hl'));
        line.classList.add('hl');
      });
    });
  });

  $$('.tree-item').forEach(item => {
    item.addEventListener('click', () => {
      const parent = item.closest('.tree');
      if (!parent) return;
      parent.querySelectorAll('.tree-item').forEach(i => i.classList.remove('active'));
      item.classList.add('active');
    });
  });

  $$('.packet-row').forEach(row => {
    row.addEventListener('click', () => {
      const list = row.parentElement;
      list.querySelectorAll('.packet-row').forEach(r => r.classList.remove('active'));
      row.classList.add('active');
    });
  });
}
