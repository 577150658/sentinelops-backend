#!/usr/bin/env python3
"""
patch_add_tool.py
补全「注册工具」和「重新加载 MCP」功能
支持前后端分离目录

用法：
    python patch_add_tool.py <前端目录> <后端目录>
    
例如：
    python patch_add_tool.py D:\\sentinelops\\frontend D:\\sentinelops\\backend
"""

import sys
from pathlib import Path


def resolve_paths():
    """解析前端和后端目录"""
    if len(sys.argv) >= 3:
        front = Path(sys.argv[1]).resolve()
        back = Path(sys.argv[2]).resolve()
        return front, back

    # 交互式输入
    print("=" * 60)
    print("前后端分离目录补丁")
    print("=" * 60)
    print()
    print("请输入前端目录（包含 index.html 的文件夹）：")
    front_input = input("  前端路径: ").strip().strip('"').strip("'")
    print()
    print("请输入后端目录（包含 app/ 和 run.py 的文件夹）：")
    back_input = input("  后端路径: ").strip().strip('"').strip("'")
    print()

    return Path(front_input).resolve(), Path(back_input).resolve()


def validate(front: Path, back: Path) -> bool:
    ok = True

    if not (front / "index.html").exists():
        print(f"❌ 前端目录里没有 index.html: {front}")
        ok = False

    if not (front / "js" / "data" / "mock-api.js").exists():
        print(f"❌ 前端目录里没有 js/data/mock-api.js: {front}")
        ok = False

    if not (back / "app" / "routers" / "tools.py").exists():
        print(f"❌ 后端目录里没有 app/routers/tools.py: {back}")
        ok = False

    return ok


def main():
    front, back = resolve_paths()

    print(f"▶ 前端目录: {front}")
    print(f"▶ 后端目录: {back}")
    print()

    if not validate(front, back):
        print()
        print("目录不正确，请检查后重试。")
        sys.exit(1)

    # ============================================================
    # 1. 后端：在 tools.py 末尾追加 POST /tools
    # ============================================================
    tools_py = back / "app" / "routers" / "tools.py"
    content = tools_py.read_text(encoding="utf-8")

    if "create_tool" in content:
        print("  · 后端 tools.py 已有 create_tool，跳过")
    else:
        addition = '''

# ============================================================
# 注册工具接口
# ============================================================
from pydantic import BaseModel


class ToolCreate(BaseModel):
    endpoint: str
    tools: str = ""
    permission: str = "扫描"
    signature: str = "待校验"


@router.post("/tools")
def create_tool(body: ToolCreate, db: Session = Depends(get_db)):
    import time
    tid = "T-" + str(int(time.time()))[-4:]
    t = Tool(
        id=tid,
        endpoint=body.endpoint,
        tools=body.tools,
        permission=body.permission,
        signature=body.signature,
        last_call="—",
        enabled=False,
    )
    db.add(t)
    db.commit()
    return {
        "ok": True,
        "id": tid,
        "endpoint": t.endpoint,
        "enabled": t.enabled,
    }
'''
        tools_py.write_text(content.rstrip() + addition, encoding="utf-8")
        print("  ✓ 后端 app/routers/tools.py 已追加 POST /tools")

    # ============================================================
    # 2. 前端 index.html：加 data-action
    # ============================================================
    index_html = front / "index.html"
    html = index_html.read_text(encoding="utf-8")
    changed = False

    old_btn = '<button class="btn btn--primary">+ 注册工具</button>'
    new_btn = '<button class="btn btn--primary" data-action="open-add-tool">+ 注册工具</button>'
    if old_btn in html:
        html = html.replace(old_btn, new_btn, 1)
        print("  ✓ index.html：注册工具按钮已加 data-action")
        changed = True
    elif 'data-action="open-add-tool"' in html:
        print("  · index.html：注册工具按钮已有属性")
    else:
        print("  ⚠ index.html：没找到「+ 注册工具」按钮")

    old_reload = '<button class="btn">重新加载 MCP</button>'
    new_reload = '<button class="btn" data-action="reload-mcp">重新加载 MCP</button>'
    if old_reload in html:
        html = html.replace(old_reload, new_reload, 1)
        print("  ✓ index.html：重新加载 MCP 按钮已加 data-action")
        changed = True
    elif 'data-action="reload-mcp"' in html:
        print("  · index.html：重新加载 MCP 按钮已有属性")
    else:
        print("  ⚠ index.html：没找到「重新加载 MCP」按钮")

    if changed:
        index_html.write_text(html, encoding="utf-8")

    # ============================================================
    # 3. 前端 js/bindings/tools.js
    # ============================================================
    tools_js = front / "js" / "bindings" / "tools.js"
    tools_js.parent.mkdir(parents=True, exist_ok=True)

    tools_content = '''import { MockAPI } from '../data/mock-api.js';
import { Store } from '../core/store.js';
import { Toast } from '../core/toast.js';

export function bindTools() {
  document.addEventListener('click', async (e) => {
    const btn = e.target.closest('[data-action]');
    const toggle = e.target.closest('.toggle[data-tool-id]');

    // 1. toggle 开关
    if (toggle) {
      e.stopPropagation();
      const toolId = toggle.dataset.toolId;
      try {
        const r = await MockAPI.toggleTool(toolId);
        toggle.classList.toggle('on', r.enabled);
        Toast.show(`工具 ${toolId} 已${r.enabled ? '启用' : '禁用'}`, 'info');
        const tools = await MockAPI.fetchTools();
        Store.set({ tools });
      } catch (err) {
        Toast.show('切换失败：' + err.message, 'error');
      }
      return;
    }

    if (!btn) return;
    const action = btn.dataset.action;

    // 2. 注册工具
    if (action === 'open-add-tool') {
      const endpoint = prompt('工具端点（如 nmap-mcp-server）');
      if (!endpoint) return;

      const tools = prompt('封装工具（如 Nmap, Masscan）', '') || '';
      const permission = prompt('权限（扫描 / 利用 / 只读 / 后渗透）', '扫描') || '扫描';

      try {
        const r = await MockAPI.addTool({
          endpoint,
          tools,
          permission,
          signature: '待校验',
        });
        Toast.show(`已注册 ${r.id}：${r.endpoint}`, 'success');
        const list = await MockAPI.fetchTools();
        Store.set({ tools: list });
      } catch (err) {
        Toast.show('注册失败：' + err.message, 'error');
      }
      return;
    }

    // 3. 重新加载 MCP
    if (action === 'reload-mcp') {
      btn.disabled = true;
      const original = btn.textContent;
      btn.textContent = '加载中…';
      try {
        const tools = await MockAPI.fetchTools();
        Store.set({ tools });
        Toast.show(`已重新加载 ${tools.length} 个工具端点`, 'success');
      } catch (err) {
        Toast.show('加载失败：' + err.message, 'error');
      } finally {
        btn.disabled = false;
        btn.textContent = original;
      }
    }
  });
}
'''
    tools_js.write_text(tools_content, encoding="utf-8")
    print("  ✓ 前端 js/bindings/tools.js 已重写")

    # ============================================================
    # 4. 前端 js/data/mock-api.js：加 addTool
    # ============================================================
    mock_api = front / "js" / "data" / "mock-api.js"
    api_content = mock_api.read_text(encoding="utf-8")

    if "addTool" in api_content:
        print("  · 前端 mock-api.js 已有 addTool")
    else:
        needle = "toggleTool: (id) => request(`/api/tools/${id}/toggle`, { method: 'POST' }),"
        if needle in api_content:
            replacement = (
                needle + "\n"
                "  addTool: (data) => request('/api/tools', {\n"
                "    method: 'POST',\n"
                "    body: JSON.stringify(data),\n"
                "  }),"
            )
            api_content = api_content.replace(needle, replacement, 1)
            mock_api.write_text(api_content, encoding="utf-8")
            print("  ✓ 前端 js/data/mock-api.js 已加 addTool")
        else:
            print("  ⚠ mock-api.js 里没找到 toggleTool 那一行")
            print("    请手动加上 addTool 方法：")
            print("    addTool: (data) => request('/api/tools', {")
            print("      method: 'POST', body: JSON.stringify(data),")
            print("    }),")

    # ============================================================
    # 完成
    # ============================================================
    print()
    print("=" * 60)
    print("✅ 补丁完成！")
    print("=" * 60)
    print()
    print("下一步：")
    print()
    print("1. 重启后端：")
    print(f"   cd {back}")
    print("   .venv\\Scripts\\Activate.ps1")
    print("   python run.py")
    print()
    print("2. 验证后端接口：")
    print("   http://localhost:8089/docs")
    print("   搜 tools，应该看到 POST /api/tools")
    print()
    print("3. 刷新前端：")
    print("   Ctrl+Shift+R")
    print("   打开「工具管理」页，点「+ 注册工具」")
    print()


if __name__ == "__main__":
    main()