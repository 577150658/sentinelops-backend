import { bindNav } from './nav.js';
import { bindEmergency } from './emergency.js';
import { bindApproval } from './approval.js';
import { bindSkillImport } from './skills-import.js';
import { bindCodeView } from './code-view.js';
import { bindTools } from './tools.js';
import { bindModels } from './models.js';
import { bindReports } from './reports.js';
import { bindImport } from './import.js';
import { bindReplay } from './replay.js';
import { bindOrchestration } from './orchestration.js';
import { bindTargets } from './targets.js';
import { bindCmdk } from '../core/cmdk.js';

let bound = false;

export function bindAll() {
  if (bound) return;
  bound = true;

  const binders = [
    ['nav', bindNav],
    ['emergency', bindEmergency],
    ['approval', bindApproval],
    ['skillImport', bindSkillImport],
    ['codeView', bindCodeView],
    ['tools', bindTools],
    ['models', bindModels],
    ['reports', bindReports],
    ['import', bindImport],
    ['replay', bindReplay],
    ['orchestration', bindOrchestration],
    ['targets', bindTargets],
    ['cmdk', bindCmdk],
  ];

  const failed = [];

  for (const [name, fn] of binders) {
    try {
      fn();
      console.log(`[bind] ${name} ok`);
    } catch (err) {
      console.error(`[bind] ${name} failed:`, err);
      failed.push({ name, err });
    }
  }

  // 关键模块失败 → 抛错，让 main.js 进入错误状态
  const critical = ['nav', 'approval'];
  const criticalFailed = failed.filter(f => critical.includes(f.name));
  if (criticalFailed.length) {
    throw new Error(
      '关键模块绑定失败: ' + criticalFailed.map(f => f.name).join(', ')
    );
  }
}
