export const initialState = {};
export const seed = {};

// 任务编排演示数据（供前端渲染使用）
export const pipelineTasks = [
  { id: '0347', title: '子域枚举 acme.com',           phase: '侦察', status: 'done',    risk: 'low',      agent: 'recon-01',   progress: 100, source: 'template', depends_on: [] },
  { id: '0348', title: 'HTTP 响应指纹采集',           phase: '侦察', status: 'done',    risk: 'low',      agent: 'recon-01',   progress: 100, source: 'template', depends_on: [] },
  { id: '0341', title: 'Nmap 全端口扫描 10.0.3.0/24', phase: '扫描', status: 'running', risk: 'low',      agent: 'recon-02',   progress: 72,  source: 'planner',  depends_on: ['0347'] },
  { id: '0344', title: 'Nuclei 模板扫描 api.acme.com', phase: '扫描', status: 'done',    risk: 'low',      agent: 'scan-03',    progress: 100, source: 'planner',  depends_on: ['0347'] },
  { id: '0345', title: '目录爆破 /admin 路径',         phase: '枚举', status: 'done',    risk: 'medium',   agent: 'fuzz-01',    progress: 100, source: 'planner',  depends_on: ['0347'] },
  { id: '0342', title: 'Redis 未授权访问验证',         phase: '利用', status: 'blocked', risk: 'critical', agent: 'exploit-01', progress: 0,   source: 'planner',  depends_on: ['0341'], command: 'redis-cli -h 10.0.3.44 -p 6379 INFO keyspace' },
  { id: '0343', title: 'SSH 弱口令爆破 10.0.5.12',     phase: '利用', status: 'blocked', risk: 'high',     agent: 'exploit-01', progress: 0,   source: 'planner',  depends_on: ['0341'], command: 'hydra -l admin -P top1k.txt 10.0.5.12 ssh' },
  { id: '0346', title: 'API 端点 SQL 注入验证',         phase: '利用', status: 'done',    risk: 'critical', agent: 'exploit-02', progress: 100, source: 'planner',  depends_on: ['0344', '0345'], command: 'sqlmap -u https://api.acme.com/v1/search?q=1 --batch' },
];
