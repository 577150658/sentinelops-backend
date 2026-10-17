import { renderKpis, renderModelChips } from './layout.js';
import { renderFindings } from './findings.js';
import { renderOrchestration, renderApprovals, renderPipeline } from './orchestration.js';
import { renderSkills } from './skills.js';
import { renderAudit } from './audit.js';
import { renderTools } from './tools.js';
import { renderModels } from './models.js';
import { renderReports } from './reports.js';
import { renderTargets } from './targets.js';

export function renderAll(state) {
  if (!state.ready) return;

  renderKpis(state);
  renderModelChips(state);
  renderFindings(state);
  renderOrchestration(state);
  renderPipeline(state);
  renderApprovals(state);
  renderSkills(state);
  renderAudit(state);
  renderTools(state);
  renderModels(state);
  renderReports(state);
  renderTargets(state);
}
