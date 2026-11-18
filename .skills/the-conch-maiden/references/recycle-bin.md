# conch · fuxi-station 回收站（文件健康审查及整理的删除条目共用）

> 自 SKILL.md 1.4.0「整理模式」流程第 3 步暂存条与第 4 步原样迁入（1.5.0 拆分），后附 2026-11-17 三批实操补充。

## 本机暂存

- 待删件先**挪进本机暂存** `<数据根>/backups/_to_delete_YYYYMMDD/`，同时写 `MANIFEST.tsv`（类别·原路径·SHA-256·字节）。挪动可逆，打包上 fuxi 前不删任何东西。

## 上传与登记

**回收站（fuxi-station）**：保留期口径见 `brain/permanent/Doctor协作偏好.md`「fuxi-station 归档细则」（回收站以实际进入时间计、**至少保留 15×24 小时**），落点口径见 `brain/references/备份策略-20260514.md`——`F:\Mac_Quarantine\` 是待删中转区，子目录 `_to_delete_YYYYMMDD\`（ASCII 名），期满清理只按精确名单、绝不用目录通配。**窗口截止日按远端实际入库日加 15 天计**，不按打包日。fuxi 的 ssh 默认 shell 是 **PowerShell 5.1**（经验库 `EXP-20260822-002-T`）：远端命令一律 PS 语法——建目录 `New-Item -ItemType Directory -Force -Path '<路径>' -ErrorAction Stop | Out-Null`，校验 `(Get-FileHash -Algorithm SHA256 '<文件>').Hash`；不要用 cmd 的 `if exist`、`mkdir` 条件式。沙箱连不到 fuxi：CC 打包 `tar.gz`＋`sha256`，贴命令给 Doctor 终端（scp 上传、远端 SHA 回读、追加 `INDEX.md` 一行：日期·件数·窗口截止日·来源项目）。Doctor 回报远端 SHA 与本地一致后，CC 才删本机暂存与包。

## 2026-11-17 三批实操补充（EAL 整理与 Financial 清理）

- **本机暂存核对按相对路径**，不按文件名：同名文件（多个 `README.md`）按文件名找会对错件。
- **往暂存挪文件的循环**：沙箱 Bash 是 zsh，`… | while read f` 的末段在当前 shell 执行，会覆盖外层同名变量（通用教训 G-X229 2026-11-17 追记：一次把整个备查区挪进了暂存）。循环变量取不与外层重名的名字，挪完按 `MANIFEST.tsv` 逐件核对件数与 SHA。
- **远端 `INDEX.md` 追加**：`Add-Content` 遇末尾无换行的文件会粘到上一行；追加前先判断是否以换行结尾，或用 `[IO.File]` 读写补换行。PS 5.1 的 `Get-Content` 读 UTF-8 中文要加 `-Encoding UTF8`。（以上两点见经验库 `EXP-20260822-002-T` 2026-11-17 追记。）远程传中文有乱码风险，INDEX 里需要手改的旧行请 Doctor 在 fuxi 本机改（2026-11-17 本场判断，见 `brain/TODO.md`「EAL 目录整理与 conch 1.4.0 收尾」条①，未实测乱码）。
- **沙箱删不掉的残留**（如 `.git/config`、`.git/hooks`）：报给 Doctor 在终端删，回读确认为 0。
- **独立核验进行中不删暂存**：先等核验子代理读完；已删的要当场告知它。
- **期满清理不归 CC**：在 `brain/TODO.md` 对应条写明窗口截止日与精确名单的位置。
