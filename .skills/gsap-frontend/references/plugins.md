# GSAP Plugins · 速查

> 加载条件：用户提到具体插件名（Flip / MorphSVG / SplitText / Draggable / Inertia / Observer / CustomEase / Physics2D / MotionPath / ScrollSmoother / ScrambleText / GSDevTools 等）。

## 重要事实

Webflow 收购 GSAP 后，**所有插件免费、商业可用**。从公开 `gsap` 包安装：

```bash
npm install gsap
```

不再需要 Club GSAP 会员 / `.npmrc` / auth token / 私有 registry。如果用户在网上看到旧文档说要付费/Club，明确告知**全免费**。

## 注册 · 通用模式

```javascript
import { gsap } from "gsap";
import { Flip } from "gsap/Flip";
import { MorphSVGPlugin } from "gsap/MorphSVGPlugin";
gsap.registerPlugin(Flip, MorphSVGPlugin);
```

---

## Flip · FLIP 技术做布局过渡

最适合"内容/容器变化后丝滑过渡"。

```javascript
import { Flip } from "gsap/Flip";

// 1. 记录初始状态
const state = Flip.getState(".item");

// 2. 改 DOM / class / 重排（如：网格 → 列表、过滤、排序）
container.classList.toggle("list-view");

// 3. 让 GSAP 推断差异并播放
Flip.from(state, {
  duration: 0.6,
  ease: "power2.inOut",
  absolute: true,         // 过渡期 position:absolute 避免 layout
  onEnter: el => gsap.from(el, { autoAlpha: 0 }),
  onLeave: el => gsap.to(el, { autoAlpha: 0 })
});
```

适用：tab 切换、网格列表过滤、详情页展开、图片放大对比。

---

## SplitText · 文本拆分

把文本拆 `chars` / `words` / `lines` 分别动。

```javascript
import { SplitText } from "gsap/SplitText";
gsap.registerPlugin(SplitText);

const split = new SplitText(".title", { type: "chars,words" });

gsap.from(split.chars, {
  y: 40,
  autoAlpha: 0,
  stagger: 0.02,
  duration: 0.6,
  ease: "power3.out"
});

// 动画完成后还原 DOM（无障碍 + SEO）
// split.revert();
```

**注意**：SplitText 会改 DOM 结构（每个字符一个 `<div>`），影响屏幕阅读器。动画结束调 `revert()` 或在 `gsap.matchMedia` 的 `prefers-reduced-motion` 分支里完全跳过。

---

## MorphSVG · SVG 形变

两个 SVG `<path>` 之间平滑变形。

```javascript
import { MorphSVGPlugin } from "gsap/MorphSVGPlugin";
gsap.registerPlugin(MorphSVGPlugin);

gsap.to("#shape", {
  morphSVG: "#targetShape",   // 目标 path 的 selector 或 d 字符串
  duration: 1.2,
  ease: "power2.inOut"
});
```

适用：logo 形变、图标过渡、有机形状动画。

## DrawSVG · 描边动画

```javascript
import { DrawSVGPlugin } from "gsap/DrawSVGPlugin";
gsap.registerPlugin(DrawSVGPlugin);

gsap.from("#line", {
  drawSVG: 0,                // 从 0% 长度到 100%
  duration: 1.5,
  ease: "power2.out"
});
```

---

## Draggable · 可拖拽

```javascript
import { Draggable } from "gsap/Draggable";
import { InertiaPlugin } from "gsap/InertiaPlugin";
gsap.registerPlugin(Draggable, InertiaPlugin);

Draggable.create(".card", {
  type: "x,y",              // 或 "rotation" / "scroll"
  bounds: ".container",
  inertia: true,            // 配合 InertiaPlugin，惯性滑行
  edgeResistance: 0.65,
  onDragStart() { /* ... */ },
  onDragEnd() { /* ... */ }
});
```

适用：卡片拖拽、滑动条、自定义滚动、画板。

## Inertia · 惯性

通常配合 Draggable / Observer 用。给松手后的滑动加自然减速。

```javascript
gsap.to(".x", {
  inertia: { x: { velocity: 800, end: [0, 200, 400] } }
});
```

---

## Observer · 统一手势/滚轮/触摸事件

```javascript
import { Observer } from "gsap/Observer";
gsap.registerPlugin(Observer);

Observer.create({
  target: window,
  type: "wheel,touch,pointer",
  onUp:   () => gotoSection(1),
  onDown: () => gotoSection(-1),
  tolerance: 10,
  preventDefault: true
});
```

适用：自定义全屏翻页、节流的滚动响应。

---

## ScrollSmoother · 平滑滚动

详见 `references/scrolltrigger.md`。

---

## ScrollToPlugin · 滚动到元素

```javascript
import { ScrollToPlugin } from "gsap/ScrollToPlugin";
gsap.registerPlugin(ScrollToPlugin);

gsap.to(window, { duration: 0.8, scrollTo: "#section-3", ease: "power2.inOut" });
gsap.to(window, { scrollTo: { y: 1500, offsetY: 80 }, duration: 0.5 });
```

---

## CustomEase · 自定义 easing

```javascript
import { CustomEase } from "gsap/CustomEase";
gsap.registerPlugin(CustomEase);

CustomEase.create("myEase", "M0,0 C0.4,0 0.2,1 1,1");   // 贝塞尔曲线 path

gsap.to(".x", { x: 100, ease: "myEase" });
```

或可视化创建：https://gsap.com/docs/v3/Eases#custom

## EasePack · 额外 easing

包含 `RoughEase` `SlowMo` `ExpoScaleEase`：

```javascript
import { RoughEase, SlowMo, ExpoScaleEase } from "gsap/EasePack";

gsap.to(".x", { x: 100, ease: RoughEase.ease.config({ template: "none.out", strength: 1, points: 20 }) });
gsap.to(".x", { x: 100, ease: "slow(0.7, 0.7, false)" });
```

---

## Physics2D / PhysicsProps · 物理

```javascript
import { Physics2DPlugin } from "gsap/Physics2DPlugin";
gsap.registerPlugin(Physics2DPlugin);

gsap.to(".ball", {
  duration: 3,
  physics2D: { velocity: 300, angle: -60, gravity: 600 }
});
```

适用：抛物线、烟花、粒子。

---

## MotionPath · 路径动画

```javascript
import { MotionPathPlugin } from "gsap/MotionPathPlugin";
gsap.registerPlugin(MotionPathPlugin);

gsap.to(".plane", {
  duration: 5,
  motionPath: {
    path: "#flight-path",     // SVG path selector
    align: "#flight-path",
    autoRotate: true,
    alignOrigin: [0.5, 0.5]
  }
});
```

适用：图标沿轨迹运动、地图飞线。

---

## GSDevTools · 开发调试

```javascript
import { GSDevTools } from "gsap/GSDevTools";
gsap.registerPlugin(GSDevTools);

GSDevTools.create();   // 屏幕底部出现时间轴控制条
```

只在开发环境用，生产移除。

---

## 反模式

- ❌ `import { Flip } from "gsap"` — 插件不在主包默认导出。改 `from "gsap/Flip"`。
- ❌ `gsap.to(".x", { morphSVG: ... })` 但没 `registerPlugin(MorphSVGPlugin)` — 报 "MorphSVGPlugin is not registered"。
- ❌ SplitText 动完不 `revert()` — DOM 仍是拆开的 `<div>` 们，影响 SEO 和无障碍。
- ❌ 在 SSR / Next.js Server Component 直接 import 插件 — 客户端 only，套 `useEffect` / dynamic import。
