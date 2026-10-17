import { Store } from './core/store.js';
import { Toast } from './core/toast.js';
import { MockAPI } from './data/mock-api.js';
import { WSMock } from './data/mock-ws.js';
import { bindAll } from './bindings/index.js';
import { renderAll } from './render/index.js';

let booted = false;   // 防止重复启动

async function bootstrap() {
  if (booted) return;
  booted = true;

  // 1. 绑定事件
  bindAll();

  // 2. 订阅渲染
  Store.subscribe(renderAll);

  // 3. 标记加载中
  Store.set({ loading: true, ready: false, bootError: null });

  // 4. 拉数据
  try {
    const [tasks, findings, approvals, skills, auditLogs, tools, models, reports, targets] =
      await Promise.all([
        MockAPI.fetchTasks(),
        MockAPI.fetchFindings(),
        MockAPI.fetchApprovals(),
        MockAPI.fetchSkills(),
        MockAPI.fetchAuditLogs(),
        MockAPI.fetchTools(),
        MockAPI.fetchModels(),
        MockAPI.fetchReports(),
        MockAPI.fetchTargets(),
      ]);

    Store.set({
      tasks, findings, approvals, skills, auditLogs,
      tools, models, reports, targets,
      loading: false,
      ready: true,
      bootError: null,
    });

    console.log('[main] 数据加载完成, tasks =', tasks.length);
  } catch (err) {
    // 加载失败：不启动 WS，不显示 ready
    Store.set({
      loading: false,
      ready: false,
      bootError: err.message || String(err),
    });

    console.error('[main] 数据加载失败:', err);
    Toast.show('数据加载失败：' + err.message, 'error', 6000);
    showBootError(err);
    return;   // ← 关键：直接返回，不继续
  }

  // 5. WS 事件订阅
  WSMock.on('task.progress', ({ taskId, progress }) => {
    Store.set(s => ({
      tasks: (s.tasks || []).map(t =>
        t.id === taskId
          ? { ...t, progress, status: progress >= 100 ? 'done' : t.status }
          : t
      ),
    }));
  });

  WSMock.on('audit.log', (log) => {
    Store.set(s => ({ auditLogs: [log, ...(s.auditLogs || [])] }));
  });

  WSMock.on('ws.gaveup', () => {
    Toast.show('WebSocket 连接已放弃', 'warning', 4000);
  });

  // 6. 启动 WS
  WSMock.start();

  Toast.show('控制台已就绪', 'info', 2000);
}

function showBootError(err) {
  const main = document.getElementById('main');
  if (!main) return;

  main.innerHTML = `
    <div style="display:flex;align-items:center;justify-content:center;height:100%;padding:40px">
      <div style="max-width:520px;text-align:center">
        <div style="font-size:48px;opacity:.4;margin-bottom:16px">⚠</div>
        <h2 style="font-size:18px;margin-bottom:10px">后端连接失败</h2>
        <p style="color:var(--muted);font-size:13px;line-height:1.7;margin-bottom:20px">
          ${String(err.message || err).replace(/</g, '&lt;')}
        </p>
        <div style="background:var(--panel-2);border:1px solid var(--border);border-radius:6px;padding:12px;font-family:var(--mono);font-size:11.5px;color:var(--text-dim);text-align:left">
          <div>1. 确认后端已启动：cd sentinelops-backend &amp;&amp; python run.py</div>
          <div>2. 确认端口为 8089</div>
          <div>3. 确认 .env 的 CORS_ORIGINS 包含本页地址</div>
        </div>
        <button class="btn btn--primary" style="margin-top:20px" onclick="location.reload()">
          重新加载
        </button>
      </div>
    </div>
  `;
}

bootstrap();
