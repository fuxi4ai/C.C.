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

## 远端 `INDEX.md` 登记（2.3.0 · 幂等模板）

> Financial 首例（2026-11-18）：CC 给的追加命令没先读 INDEX 格式（写成表格行，旧行是列表式），且与 `git commit` 拼在一起；旧命令被重跑后 INDEX 出现两行重复登记，修了约 4 轮（通用教训 G-X120 第四次复发）。

1. **先回读末尾几行对齐格式**：`ssh fuxi-station "Get-Content -Tail 3 'F:\Mac_Quarantine\INDEX.md'"`。现行格式（2026-11-18 实读）：`- YYYY-MM-DD _to_delete_YYYYMMDD\<包名>.tar.gz  <N> files, <说明>, sha256 <全长小写>, keep until YYYY-MM-DD`，ASCII。
2. **幂等写法：先删同键行，再写一行**，重跑多少次结果都只有一行。同键＝`暂存目录名\包名.tar.gz`，不能只用目录名（也不要省掉 `.tar.gz`，否则包名互为前缀时同样误删）：`*_to_delete_20261117*` 会把已有的 `_to_delete_20261117b`、`…c` 两行一起删掉（2.3.0 独立核验指出）。PowerShell 的 `-like` 把 `\` 当普通字符：

```bash
ssh fuxi-station "\$p='F:\Mac_Quarantine\INDEX.md'; \$l=@([IO.File]::ReadAllLines(\$p) | Where-Object { \$_ -notlike '*_to_delete_YYYYMMDD\<包名>.tar.gz*' }); \$l+='- YYYY-MM-DD _to_delete_YYYYMMDD\<包名>.tar.gz  N files, <说明>, sha256 <全长>, keep until YYYY-MM-DD'; [IO.File]::WriteAllLines(\$p,\$l); Get-Content -Tail 3 \$p"
```

3. **单独成块**（全局偏好「无先后依赖的命令合并成一条」的例外，依据 G-X120）：登记命令不与上传、本地 `git commit` 或任何别的命令拼在同一条里；Doctor 会重跑旧命令，拼在一起的非幂等步骤会被重复执行。
4. 这条命令重写整个文件（`WriteAllLines` 按 UTF-8 写）；INDEX 若混有非 UTF-8 的中文行可能被改坏，登记行一律只写 ASCII。
