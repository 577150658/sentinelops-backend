#!/usr/bin/env python3
"""自动给 index.html 补 id 和 data-action"""
from pathlib import Path

ROOT = Path.cwd()
HTML = ROOT / "index.html"

if not HTML.exists():
    print("❌ 找不到 index.html")
    exit(1)

content = HTML.read_text(encoding="utf-8")

# 替换列表：(旧字符串, 新字符串)
replacements = [
    # 1. 工具管理表格
    (
        '<thead><tr><th>工具端点</th>',
        '<thead><tr><th>工具端点</th>'
    ),  # 占位，主要改下面的 tbody

    # 工具管理 tbody（谨慎替换：只替换工具表格里的）
    # 用工具表格特有的首行做锚点
    (
        '<tbody>\n        <tr><td>kali-mcp-server</td>',
        '<tbody id="tools-tbody">\n        <tr><td>kali-mcp-server</td>'
    ),

    # 2. 模型管理 grid
    (
        '<div class="grid-2" style="margin-bottom:16px">\n    <div class="model-card">\n      <div class="model-card-head"><span class="dot dot--on"></span><div><div class="model-card-name">DeepSeek-Reasoner</div>',
        '<div class="grid-2" id="models-grid" style="margin-bottom:16px"></div>\n    <div style="display:none"><div class="model-card">\n      <div class="model-card-head"><span class="dot dot--on"></span><div><div class="model-card-name">DeepSeek-Reasoner</div>'
    ),
    # 补一个关闭标签，把原静态的包起来
    (
        '<div class="form-row" style="padding-bottom:0"><div class="form-label">启用 LoRA 适配器</div><div class="toggle on" onclick="this.classList.toggle(\'on\')"></div></div>\n    </div>\n  </div>',
        '<div class="form-row" style="padding-bottom:0"><div class="form-label">启用 LoRA 适配器</div><div class="toggle on" onclick="this.classList.toggle(\'on\')"></div></div>\n    </div>\n  </div></div>'
    ),

    # 3. 模型添加按钮
    (
        '<button class="btn btn--primary">+ 添加模型</button>',
        '<button class="btn btn--primary" data-action="open-add-model">+ 添加模型</button>'
    ),

    # 4. 报告生成按钮
    (
        '<button class="btn btn--primary">+ 生成新报告</button>',
        '<button class="btn btn--primary" data-action="generate-report">+ 生成新报告</button>'
    ),

    # 5. 审计导出按钮
    (
        '<button class="btn">导出 CSV</button><button class="btn">导出 JSON</button>',
        '<button class="btn" data-action="export-audit-csv">导出 CSV</button><button class="btn" data-action="export-audit-json">导出 JSON</button>'
    ),

    # 6. 重放按钮
    (
        '<button class="btn btn--primary" style="flex:1;justify-content:center">重放</button>\n            <button class="btn" style="flex:1;justify-content:center">修改并重放</button>\n            <button class="btn" style="flex:1;justify-content:center">生成 PoC</button>',
        '<button class="btn btn--primary" style="flex:1;justify-content:center" data-action="replay-traffic" data-target="/v2/user/1001">重放</button>\n            <button class="btn" style="flex:1;justify-content:center" data-action="replay-modified" data-target="/v2/user/1001">修改并重放</button>\n            <button class="btn" style="flex:1;justify-content:center" data-action="generate-poc">生成 PoC</button>'
    ),

    # 7. 导入按钮
    (
        '<button class="btn">导入授权文件</button>',
        '<button class="btn" data-action="import-file" data-kind="auth" data-accept=".pdf,.png,.jpg">导入授权文件</button>'
    ),
    (
        '<button class="btn btn--primary">+ 导入 JS 文件</button>',
        '<button class="btn btn--primary" data-action="import-file" data-kind="js" data-accept=".js,.map">+ 导入 JS 文件</button>'
    ),
    (
        '<button class="btn btn--primary">+ 导入 wxapkg</button>',
        '<button class="btn btn--primary" data-action="import-file" data-kind="wxapkg" data-accept=".wxapkg,.zip">+ 导入 wxapkg</button>'
    ),
    (
        '<button class="btn btn--primary">+ 导入 APK / IPA</button>',
        '<button class="btn btn--primary" data-action="import-file" data-kind="apk" data-accept=".apk,.ipa">+ 导入 APK / IPA</button>'
    ),
    (
        '<button class="btn">导入 HAR</button>',
        '<button class="btn" data-action="import-file" data-kind="har" data-accept=".har">导入 HAR</button>'
    ),
]

count = 0
for old, new in replacements:
    if old in content:
        content = content.replace(old, new, 1)
        count += 1
        print(f"  ✓ 替换 {count}")
    else:
        print(f"  ⚠ 未找到: {old[:50]}...")

# 报告列表容器
# 找到历史报告的 <div> 容器，加 id
if '<div class="section-head"><span class="section-title">历史报告</span>' in content:
    idx = content.find('<div class="section-head"><span class="section-title">历史报告</span>')
    # 找它后面的第一个 <div> 开始
    after = content.find('<div>', idx)
    if after != -1:
        content = content[:after] + '<div id="reports-list">' + content[after + 5:]
        print(f"  ✓ 报告列表容器已加 id")
        count += 1

HTML.write_text(content, encoding="utf-8")
print()
print(f"✅ 完成，共修改 {count} 处")