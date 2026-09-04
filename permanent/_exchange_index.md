# CC 侧经验对侧索引（薄 · 供 VV 只读 · 可重建 · 非事实源）

> 生成：2026-09-04 04:17 · 生成器 brain/.tools/build_experience_index.py（v2）
> 正文真源在 CC 侧 canonical（brain/ 各项目 GOTCHAS.md + permanent/通用教训.md + permanent/经验库.md），本文件只含定位指针，供跨系统预警与复验。

## 摘要（639 条）
结构与 permanent/经验索引.md 相同（对侧对 brain 只读可直取）。

## 机器闸清单（六字段：路径/SHA/可见性/重放命令/预期通过/最近运行）

> 可见性统一为「Doctor 侧路径 · VV 可见范围外」——复验需经 Doctor 转达或受控镜像（正文不复制，保持 canonical 唯一）。

- Database/行业研究/rules/kg_promote.py
  - sha256[:16]=513af2bd06de40c8
  - 可见性: Doctor 侧路径 · VV 可见范围外
  - 重放: python3 rules/kg_promote.py <candidate> <base>（参数以 --help 为准）
  - 预期通过: 一键门全过：丢失 0/第 12 项 0%/双空 0/边 schema PASS/三元组 0
  - 最近运行: 2026-09-01 渊图入库场（日志实据·全绿） · ⚠用法未在本场实跑·复验方首跑时核 --help
- Database/行业研究/rules/check_desc_shrink.py
  - sha256[:16]=04bdb89d4002f4a6
  - 可见性: Doctor 侧路径 · VV 可见范围外
  - 重放: python3 rules/check_desc_shrink.py <base> <candidate>（参数以 --help 为准）
  - 预期通过: exit 0 = 无 desc 缩减；对未修 _v2 报出 15 处、对 canonical 报 0
  - 最近运行: 2026-09-01 渊图 QA 场（日志实据） · ⚠用法未在本场实跑
- Database/行业研究/rules/bare_alias_check.py
  - sha256[:16]=637af0c199997f23
  - 可见性: Doctor 侧路径 · VV 可见范围外
  - 重放: python3 rules/bare_alias_check.py（参数以 --help 为准）
  - 预期通过: 大小写重复/裸简称/近名兄弟簇清单；无新增违例
  - 最近运行: 2026-08 渊图入库 QA（日志实据） · ⚠用法未在本场实跑
- Database/行业研究/rules/check_id_consistency.py
  - sha256[:16]=ecfeb562d4bbc7ae
  - 可见性: Doctor 侧路径 · VV 可见范围外
  - 重放: python3 rules/check_id_consistency.py（参数以 --help 为准）
  - 预期通过: id 一致性 exit 0（187 条年份警告系存量噪音）
  - 最近运行: 2026-08-25 渊图批（日志实据） · ⚠用法未在本场实跑
- Database/行业研究/rules/name_code_consistency_check.py
  - sha256[:16]=5e32e13c7d357799
  - 可见性: Doctor 侧路径 · VV 可见范围外
  - 重放: python3 rules/name_code_consistency_check.py（参数以 --help 为准）
  - 预期通过: name↔code 无告警
  - 最近运行: 2026-09-01 渊图批（日志实据） · ⚠用法未在本场实跑
- Database/行业研究/consumers/龙鱼五力/check_ds_evidence.py
  - sha256[:16]=4066dfcf07c1209f
  - 可见性: Doctor 侧路径 · VV 可见范围外
  - 重放: python3 check_ds_evidence.py --date 2026-08-29
  - 预期通过: 有 ⚠ 即 exit 1（设计）；输出三档计数+锚出处
  - 最近运行: 2026-09-03 本场实跑（109 只 · ⚠69）
- Database/行业研究/consumers/龙鱼五力/test_check_ds_evidence.py
  - sha256[:16]=a3b9a508e11f4551
  - 可见性: Doctor 侧路径 · VV 可见范围外
  - 重放: python3 test_check_ds_evidence.py
  - 预期通过: 5/5 PASS · exit 0
  - 最近运行: 2026-09-03 本场 subagent 独立验收实跑（5/5 PASS）

## 对侧状态约定
- 未见（默认 -） / ⚑已预警 / ✓已复验
- 复验须带：命令 + 关键输出摘录 + 复验日期，回填至本地索引对应条目行（对侧列）。
