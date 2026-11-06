#!/usr/bin/env python3
"""resolve_log_path 自测：候选顺序、月目录推导、checkpoints 随月、不猜（MISSING）。"""
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from resolve_log_path import candidates, resolve
ok = fail = 0
def t(c, msg):
    global ok, fail
    ok += c; fail += (not c); print(("✓ " if c else "✗ ") + msg)
t(candidates("logs/2026-10-07-x.md") == ["logs/2026-10-07-x.md", "logs/2026-10/2026-10-07-x.md"], "普通日志候选顺序")
t(candidates("brain/logs/checkpoints/2026-10-03_y.md")[1] == "logs/2026-10/checkpoints/2026-10-03_y.md", "checkpoints 随月 + 去 brain/ 前缀")
t(candidates("logs/checkups/2026-09-29-z.md")[1] == "logs/2026-09/checkups/2026-09-29-z.md", "checkups 随月")
t(candidates("permanent/x.md") == ["permanent/x.md"], "非 logs 路径不加候选")
t(candidates("logs/README.md") == ["logs/README.md"], "无日期不推导")
with tempfile.TemporaryDirectory() as d:
    os.makedirs(f"{d}/logs/2026-10/checkpoints"); open(f"{d}/logs/2026-10/2026-10-07-x.md", "w").close()
    open(f"{d}/logs/2026-10/checkpoints/2026-10-03_y.md", "w").close(); open(f"{d}/logs/2026-11-02-w.md", "w").close()
    t(resolve("logs/2026-10-07-x.md", d) == f"{d}/logs/2026-10/2026-10-07-x.md", "折叠后按月目录命中")
    t(resolve("logs/checkpoints/2026-10-03_y.md", d) == f"{d}/logs/2026-10/checkpoints/2026-10-03_y.md", "checkpoints 折叠命中")
    t(resolve("logs/2026-11-02-w.md", d) == f"{d}/logs/2026-11-02-w.md", "未折叠的根目录优先")
    t(resolve("logs/2026-08-01-nope.md", d) is None, "都不在 → None 不猜")
print(f"\n{ok}/{ok+fail} 通过"); sys.exit(1 if fail else 0)
