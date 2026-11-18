# GlobalPercent 归档回执

- 归档日期：2026-08-01
- 原路径：`/Users/lunarabbit/Documents/Claude/Projects/Financial/GlobalPercent`
- 备查路径：`/Users/lunarabbit/Documents/Claude/Projects/Financial/备查区/GlobalPercent`
- Git HEAD：`2ba33266556e10516cf73c20d6e03a270b396c71`
- Git 状态：归档前工作树干净，分支 `master` 与 `origin/master` 对齐
- 远端：`https://github.com/fuxi4ai/GlobalPercent.git`
- 归档方式：同卷完整目录迁移，保留 `.git`、源码、测试、历史文档和忽略文件
- 兼容入口：原路径仅保留相对软链接 `GlobalPercent -> 备查区/GlobalPercent`，避免改动 EventProb 冻结合同文档哈希；实体文件只存在于备查区
- 运行状态：`com.globalpercent.server` 已从 launchd `bootout`；plist 已改名为 `com.globalpercent.plist.disabled` 并移入本备查区
- 继任边界：EventProb 仅吸收经过重审的适配、失败语义、存储和快照经验；不加载 GlobalPercent 旧运行时

## 可恢复性

归档未删除项目数据。若未来决定恢复，先重新审计归档提交，再将项目目录移回原路径；LaunchAgent 不得在未更新虚拟环境、路径和发布凭证前重新注册。

Conch 归档前扫描识别到的唯一普通候选是空文件 `tests/__init__.py`。为保持仓库提交原貌，本次没有单独移除或改写它。
