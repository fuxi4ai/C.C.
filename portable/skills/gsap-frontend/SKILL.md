---
name: "gsap-frontend"
description: "GSAP (GreenSock Animation Platform) 前端动画综合 skill。触发条件极窄：用户消息中明确出现 \"GSAP\" / \"gsap\" / \"GreenSock\" 等专名才激活；一旦激活，整轮对话默认按 GSAP 模式工作，不再重新判定。覆盖 core API、timeline 编排、ScrollTrigger 滚动动画、React/Vue/Svelte 集成、所有官方插件、性能与反模式。基于 greensock/gsap-skills 官方 8 个 skill 蒸馏合并。Use when user explicitly invokes GSAP for animation work."
license: "MIT"
---

# GSAP Frontend Skill

> 自制合并版，基于 greensock/gsap-skills（MIT）。把官方 8 个 SKILL.md 蒸馏成"精简主干 + 5 个 references"按需加载，避免一次性灌爆上下文。

---

## 触发与生效（关键）

**触发条件**：用户消息中明确出现以下任一专名：
- `GSAP` · `gsap`
- `GreenSock` · `greensock`
- `useGSAP` · `gsap.timeline` · `gsap.to` · `ScrollTrigger`
- 显式提到具体 GSAP 插件名：`ScrollSmoother` · `MotionPath` · `Flip` · `Draggable` · `SplitText` · `MorphSVG` · `DrawSVG` · `CustomEase` 等

**不触发**：用户只描述效果（"加个淡入"、"做视差"、"滚动动画"）但未点名 GSAP——让 `frontend-design` / `emil-design-eng` / `impeccable` 等 skill 先处理。

**粘性生效**：一旦激活，**整轮对话**默认按 GSAP 模式工作。后续 follow-up 即使没再说 "GSAP" 也按本 skill 规范回答，无需重新触发判定。

---

## 重要事实（2024-Webflow 收购后）

GSAP **完全免费**，所有插件免费用于商业用途。从公开 `gsap` npm 包安装即可：
```bash
npm install gsap
```
**不需要** Club GSAP 会员、`.npmrc`、auth token、私有 registry。从前的 Club-only 插件（SplitText / MorphSVG / DrawSVG / MotionPath / Inertia / Physics2D 等）现在全部免费。

如果用户问到付费/Club/license 问题，明确告知：全免费、商业可用。

---

## Canonical 代码骨架（最常推荐的写法）

```javascript
// 1. 引入 + 注册插件（每个 app 只做一次，通常在入口）
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);

// 2. 单 tween — 优先 transform 别名（x/y/rotation/scale）+ autoAlpha
gsap.to(".box", {
  x: 100,
  autoAlpha: 1,
  duration: 0.6,
  ease: "power2.inOut"
});

// 3. timeline 编排（优于链式 delay）
const tl = gsap.timeline({ defaults: { duration: 0.5, ease: "power2" } });
tl.to(".a", { x: 100 })
  .to(".b", { y: 50 }, "+=0.2")       // a 结束后再延迟 0.2s
  .to(".c", { opacity: 0 }, "-=0.1"); // 与前一个重叠 0.1s

// 4. ScrollTrigger 绑 timeline
const scrollTl = gsap.timeline({
  scrollTrigger: {
    trigger: ".section",
    start: "top center",
    end: "bottom center",
    scrub: true   // 跟随滚动；不需要联动播放就用 toggleActions
  }
});
scrollTl.to(".panel", { x: 100 })
        .to(".panel", { rotation: 5, duration: 0.7 });

// 布局变化（DOM 增删/字体加载/图片加载）后必须 refresh
ScrollTrigger.refresh();
```

---

## Core API · 最常用

| 写法 | 用途 |
|------|------|
| `gsap.to(target, vars)` | 从当前状态 → 目标状态 |
| `gsap.from(target, vars)` | 从 vars → 当前状态（适合入场动画） |
| `gsap.fromTo(target, fromVars, toVars)` | 显式指定起止 |
| `gsap.set(target, vars)` | 立即赋值（无动画） |
| `gsap.timeline(opts)` | 创建时间轴 |
| `gsap.registerPlugin(...)` | 注册插件 |
| `gsap.matchMedia()` | 响应式 / `prefers-reduced-motion` |

**transform 别名**（GSAP 推荐，自动写到 transform，避免布局抖动）：
- `x` `y` `z` → translate
- `rotation` `rotationX` `rotationY` → rotate
- `scale` `scaleX` `scaleY` → scale
- `skewX` `skewY` → skew
- `autoAlpha` → `opacity` + `visibility`（更利于无障碍）

**常用 easing**：`power1` `power2` `power3` `power4`（每个有 `.in` `.out` `.inOut`）、`back` `elastic` `bounce` `circ` `expo` `sine` `steps(n)`。默认 `power1.out`。

**stagger**（批量错开）：
```javascript
gsap.to(".item", {
  y: 0,
  stagger: 0.1           // 简写：每个间隔 0.1s
});
gsap.to(".item", {
  y: 0,
  stagger: { each: 0.1, from: "center", grid: "auto" }
});
```

**defaults**（避免重复写 duration/ease）：
```javascript
gsap.defaults({ duration: 0.5, ease: "power2.out" });
const tl = gsap.timeline({ defaults: { duration: 0.5 } });
```

---

## 响应式与无障碍 · `gsap.matchMedia`

```javascript
const mm = gsap.matchMedia();

mm.add({
  isDesktop: "(min-width: 768px)",
  isMobile:  "(max-width: 767px)",
  reduceMotion: "(prefers-reduced-motion: reduce)"
}, (ctx) => {
  const { isDesktop, reduceMotion } = ctx.conditions;

  if (reduceMotion) {
    // 严格按系统偏好关动画
    gsap.set(".hero", { autoAlpha: 1 });
    return;
  }

  if (isDesktop) {
    gsap.to(".hero", { x: 200, duration: 1 });
  } else {
    gsap.to(".hero", { x: 80, duration: 0.6 });
  }

  // 自动 cleanup：媒体条件改变时自动 revert 这块作用域内的动画
});
```

`prefers-reduced-motion` **必须支持**——这是无障碍硬性要求。

---

## 性能要点（吃这五条就够）

1. **优先 transform / opacity**：动 `x/y/rotation/scale/autoAlpha` 而非 `top/left/width/height/margin`（避免 layout/paint，只走 composite）。
2. **慎用 `will-change`**：只在动画前短暂加（如 onEnter），动画结束 `clear` 掉。常驻 `will-change` 会吃显存、反而卡。
3. **批量 / 复用**：`ScrollTrigger.batch()` 处理大量元素；不要为每个元素单建 ScrollTrigger 实例。
4. **必须清理**：组件卸载/路由切换前 `tween.kill()` / `tl.kill()` / `ScrollTrigger.getAll().forEach(t => t.kill())`，避免内存泄漏。
5. **layout 变后 refresh**：图片懒加载、字体回流、内容异步插入 → `ScrollTrigger.refresh()`。

---

## 反模式（坚决不写）

- ❌ `gsap.to(".x", { top: 100 })` — 动 layout 属性，掉帧。改 `y`。
- ❌ React 里不带 cleanup 的 `useEffect(() => { gsap.to(...) }, [])` — 卸载残留。改用 `useGSAP` 或 `gsap.context`。
- ❌ ScrollTrigger 用 `setTimeout` 替代 `refresh()` — 时机不可靠。
- ❌ `import { ScrollTrigger } from "gsap/ScrollTrigger"` 但不 `registerPlugin` — 报 "ScrollTrigger is not registered"。
- ❌ 长链 `.to(...).to(...).to(...)` 加大量 `delay` — 改 timeline 的 `position` 参数（`+=` `-=` 标签）。
- ❌ 同一目标多个独立 tween 抢同一属性 — 用 timeline 顺序化、或 `overwrite: true`。

---

## 何时跳到 references/

主干吃 80% 场景；遇到下列情形再加载对应 reference：

| 场景 | 加载 |
|------|------|
| 滚动联动 / pin / scrub / 视差 / ScrollSmoother | `references/scrolltrigger.md` |
| React / Next.js / useGSAP / SSR | `references/react.md` |
| Vue / Svelte / SvelteKit / Nuxt 等 | `references/frameworks.md` |
| Flip / MorphSVG / DrawSVG / SplitText / Draggable / Inertia / Observer / CustomEase / Physics2D / MotionPath | `references/plugins.md` |
| `gsap.utils` 工具（clamp / mapRange / random / snap / interpolate / wrap / pipe / toArray） | `references/utils.md` |

---

## 资源

- 官方文档：https://gsap.com/docs/v3/
- 官方 skill 仓库：https://github.com/greensock/gsap-skills（MIT，本 skill 蒸馏自其 8 个 SKILL.md）
- 论坛：https://gsap.com/community/

---

**版本**：v2.0（2026-06-30 重做）
**v1 → v2 主要变化**：触发词从"激进/含效果描述"收窄到"GSAP 硬专名"；新增"粘性生效"段；强调 Webflow 收购后全免费事实；反模式从"散点"整理为"6 条铁律"。
