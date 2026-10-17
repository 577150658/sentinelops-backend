export function renderKpis(state) {
  const map = {
    assets: state.kpis?.assets ?? 0,
    tasks: state.kpis?.tasks ?? 0,
    findings: state.kpis?.findings ?? 0,
    risk: state.kpis?.riskScore ?? 0,
  };
  Object.entries(map).forEach(([k, v]) => {
    const el = document.querySelector(`[data-kpi="${k}"]`);
    if (el) el.textContent = v;
  });
}

export function renderModelChips(state) {
  const chips = document.querySelectorAll('.model-chips .chip');
  if (chips[0]) {
    const meta = chips[0].querySelector('.chip-meta');
    if (meta) meta.textContent = `reasoner · ${state.models?.deepseek?.latency ?? 320}ms`;
  }
  if (chips[1]) {
    const meta = chips[1].querySelector('.chip-meta');
    if (meta) meta.textContent = `GPU ${state.models?.local?.gpu ?? 68}% · 队列 ${state.models?.local?.queue ?? 3}`;
  }
}
