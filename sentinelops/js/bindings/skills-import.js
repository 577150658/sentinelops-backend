import { $$ } from '../utils.js';
import { Toast } from '../core/toast.js';

let importStep = 1;
let importConfirmed = false;

export function bindSkillImport() {
  const overlay = document.getElementById('skillOverlay');
  if (!overlay) return;

  const stepEls = $$('#skillOverlay .step[data-step]');
  const lineEls = $$('#skillOverlay .step-line[data-line]');
  const paneEls = $$('#skillOverlay .import-pane');

  function openSkillImport() {
    overlay.classList.add('show');
    importConfirmed = false;
    const cb = overlay.querySelector('.checkbox');
    if (cb) cb.classList.remove('on');
    const fileChip = document.getElementById('dropzoneFile');
    if (fileChip) fileChip.hidden = true;
    setImportStep(1);
  }

  function closeSkillImport() { overlay.classList.remove('show'); }

  function setImportStep(n) {
    n = Math.min(3, Math.max(1, n));
    importStep = n;

    stepEls.forEach(s => {
      const sn = +s.dataset.step;
      s.classList.toggle('active', sn === n);
      s.classList.toggle('done', sn < n);
    });
    lineEls.forEach(l => l.classList.toggle('done', +l.dataset.line < n));
    paneEls.forEach(p => { p.hidden = (+p.dataset.pane !== n); });

    const prev = document.getElementById('prevBtn');
    const next = document.getElementById('nextBtn');
    prev.hidden = (n === 1);
    next.textContent = (n === 3) ? '确认导入' : '下一步';
    next.disabled = (n === 3 && !importConfirmed);
    if (n === 2) runValidation();
  }

  function nextImportStep() {
    if (importStep < 3) { setImportStep(importStep + 1); return; }
    const btn = document.getElementById('nextBtn');
    const original = btn.textContent;
    btn.textContent = '导入中…';
    btn.disabled = true;
    setTimeout(() => {
      closeSkillImport();
      btn.textContent = original;
      btn.disabled = false;
      Toast.show('Skill 导入成功，已注册到 MCP 工具层', 'success');
    }, 900);
  }

  function runValidation() {
    $$('#validateList .check-item').forEach((it, i) => {
      it.style.opacity = '.25';
      setTimeout(() => { it.style.opacity = '1'; }, 130 * i);
    });
  }

  function toggleConfirm(el) {
    const cb = el.querySelector('.checkbox');
    cb.classList.toggle('on');
    importConfirmed = cb.classList.contains('on');
    const next = document.getElementById('nextBtn');
    if (importStep === 3) next.disabled = !importConfirmed;
  }

  (function initDropzone() {
    const dz = document.getElementById('dropzone');
    if (!dz) return;
    dz.addEventListener('dragover', e => { e.preventDefault(); dz.classList.add('drag'); });
    dz.addEventListener('dragleave', () => dz.classList.remove('drag'));
    dz.addEventListener('drop', e => {
      e.preventDefault();
      dz.classList.remove('drag');
      if (e.dataTransfer.files.length) showPickedFile(e.dataTransfer.files[0]);
    });
    dz.addEventListener('click', () => {
      const inp = document.createElement('input');
      inp.type = 'file';
      inp.accept = '.json,.yaml,.yml,.zip,.skill';
      inp.onchange = () => { if (inp.files[0]) showPickedFile(inp.files[0]); };
      inp.click();
    });
  })();

  function showPickedFile(file) {
    const box = document.getElementById('dropzoneFile');
    box.hidden = false;
    box.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></svg><span>${file.name}</span><span style="color:var(--muted);font-family:var(--mono);font-size:10.5px">${(file.size/1024).toFixed(1)} KB</span>`;
  }

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeSkillImport();
  });

  window.openSkillImport  = openSkillImport;
  window.closeSkillImport = closeSkillImport;
  window.setImportStep    = setImportStep;
  window.nextImportStep   = nextImportStep;
  window.toggleConfirm    = toggleConfirm;
}
