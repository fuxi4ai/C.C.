# TODO.md

> 最后更新：2026-06-03

---

## ✅ 已完成

- [x] Project Review skill v2.1 创建并安装
- [x] 14 个项目审核完成
- [x] 高优：dream/ 加重试 + 超时 + 执行日志
- [x] 高优：meditation/ 加 logging + 重试 + 超时 + 配置校验
- [x] scripts/ 5 个 Tushare 文件改用 retry_utils 重试模块
- [x] tools/ 3 个 mootdx 文件加重试配置
- [x] 97 个 .py 文件批量添加 logging
- [x] 交付标准整合到所有 27 个 PRD（AGENTS.md 新增强制规则）
- [x] 行情数据库增量更新脚本（`scripts/update_market_data.py`，2026-06-03）
- [x] 行情数据补到 2026-06-02 + TOS 同步
- [x] 9 个项目打包供交叉代码审查（2026-06-03）
- [x] 核心文件审查优化（2026-06-03）

---

## 📝 需哥哥决策

### 1. PRD 模板功能字段为空
**影响**：6 个项目 L1 覆盖率为 0%
**项目**：`strategies/`、`tushare-pro/`、`docx/`、`xlsx/`、`buddy/`、`co_action_detection/`
**问题**：PRD.md 中 `## 📝 功能实现` 和 `需求` 字段标记为 `[待填写]`
**建议**：逐个填写真实功能描述后重跑 L1 审核

### 2. 全项目零测试覆盖
**影响**：99 个代码文件，21,802 行代码
**现状**：仅 `skills/tests/` 目录存在但无实际测试文件
**建议方案**：
- 先为核心模块写单元测试（dream、meditation、retry_utils）
- 再为数据脚本写集成测试
- 最后覆盖业务逻辑

### 3. Dream 静默日误判（bug）
**影响**：每天 02:00 Dream 可能把"当天有交互但还没写日记"的情况误判为静默日
**根因**：Dream 只看 memory 文件，不查活跃 session
**场景**：哥哥 22:07 上线聊到凌晨 02:00+，Dream 02:00 跑的时候对话还没写入日记，就被判定为静默日
**修复方案**：Dream 判断前先 `sessions_list` 查活跃 session

### 4. 交叉代码审查反馈（进行中）
**状态**：9 个项目已打包发送，等待哥哥审查
**包清单**：scripts / tools / auto_research_deep / co_action_detection / dream / meditation / project-review / conch / tushare-pro

---

## 🔧 待办（低优先级）

- [ ] Conch 周扫 consecutiveErrors=2 需手动排查（2026-05-31 发现）
- [ ] 清理 `update_800_stocks_full.py` / `update_800_stocks_optimized.py` 历史脚本（已被 `update_market_data.py` 替代）
- [ ] `quant_research/auto_research_deep/` 下大量优化迭代 JSON 可归档清理
- [ ] `build_market_db.py` 仍引用旧路径 `dragon-palace/`（已废弃，功能被 `update_market_data.py` 替代）

---

*句芒 · 2026-06-03*
