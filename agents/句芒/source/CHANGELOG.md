# CHANGELOG

## [2026-06-03]
### Added
- 行情数据库一站式更新脚本 `scripts/update_market_data.py`（5 阶段自动化）
- 行情数据增量更新到 2026-06-02（+31,930 条个股记录，+38 个交易日）
- 9 个项目打包供交叉代码审查
- 核心文件审查优化（MEMORY.md 修正 5 处不一致、TODO.md 刷新、CHANGELOG.md 补全）

### Fixed
- MEMORY.md 头部版本号与底部不一致（v2.0 → v2.3）
- MEMORY.md 最后更新日期不一致（05-12 → 06-03）
- MEMORY.md 行情数据库信息过时（1514 天/202MB → 1218982 条/206.7MB）
- MEMORY.md AutoResearch 项目自引用无效描述
- MEMORY.md dream-state.json 状态标注过时（仍显示"文件不存在"但已修复）

## [2026-05-20 ~ 2026-05-31]
### Added
- 所有 27 个 PRD 整合交付标准（`## ✅ 交付标准` 章节）
- 97 个 .py 文件批量添加 logging
- Dream 静默日误判问题记录
- Cron 双重执行检测与修复

### Fixed
- Cron SessionKey 幽灵事件（`/new` 后旧 key 残留）
- Dream `dragon_dream_daily.py` 超时 + 重试 + logging
- Meditation 脚本配置校验 + 重试 + 超时
- 5 个 Tushare 脚本改用 retry_utils
- 3 个 mootdx 工具加重试配置
- dream-state.json 初始化（原缺失）

## [2026-05-07 ~ 2026-05-14]
### Added
- TOS 对象存储共享盘（5 Agent × 5 领域）
- 统一凭据管理 `~/.openclaw/credentials/`
- 行情数据库（843 只 A 股，SQLite）
- 海螺姑娘技能适配龙宫架构
- 证据契约（数据真实性规则）

### Changed
- Workspace 架构重构：取消 dragon-spirit/dragon-palace，提升热区到根目录
- 回收站保留期从 30 天缩短到 7 天
- 删除 AKShare / EASTMONEY 相关脚本

### Fixed
- Gateway 重启 API 回档问题
- BOOTSTRAP.md 删除 + 过期文档清理
- s3fs 不兼容火山 TOS → 改用 Python SDK
- 数据库被覆盖为空壳问题（健康检查发现）
- 密钥硬编码安全红线

## [2026-04-08 ~ 2026-04-30]
### Added
- 句芒 · 活泼俏皮版 初始化
- 四大核心系统（PRD / GOTCHAS / Conch / Dream）
- 量化 AutoResearch 项目（MACD v6 + 恐慌盘 v4.1）
- 数据库优化项目
- 百炼 coding-plan API 接入
