# ScrollTrigger — 滚动驱动动画

> 加载条件：用户需要滚动联动、pin、scrub、视差、ScrollSmoother。

## 注册

```javascript
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);
```

## 两种触发模式（必须二选一）

### 模式 A · `toggleActions`（事件式 · 进退场播放）

适合普通入场动画。

```javascript
gsap.to(".card", {
  y: 0,
  autoAlpha: 1,
  scrollTrigger: {
    trigger: ".card",
    start: "top 80%",
    end: "bottom 20%",
    toggleActions: "play none none reverse"
    // 四个槽位：onEnter / onLeave / onEnterBack / onLeaveBack
    // 取值：play | pause | resume | reverse | restart | reset | complete | none
  }
});
```

### 模式 B · `scrub`（滚动驱动 · 进度跟随）

适合滚动联动、视差、长 hero。

```javascript
gsap.to(".section", {
  x: -1000,
  scrollTrigger: {
    trigger: ".section",
    start: "top top",
    end: "+=2000",         // 滚动 2000px 内播完
    scrub: true            // true=立即跟随；数字（如 1）=平滑滞后 1s
  }
});
```

**`scrub: true` vs `scrub: 1`**：前者强联动、抖动明显；后者有惯性、更优雅。复杂联动用 `1`。

## Pin（固定）

```javascript
gsap.to(".panel", {
  xPercent: -100,
  scrollTrigger: {
    trigger: ".section",
    pin: true,             // 固定 section 不滚
    start: "top top",
    end: "+=3000",
    scrub: true,
    anticipatePin: 1       // 解决某些浏览器 pin 抖动
  }
});
```

横滑 hero / 长 case study / 章节锁定 都用 pin + scrub 组合。

## 批量 · `ScrollTrigger.batch()`

替代为每个元素单建 ScrollTrigger（性能优）：

```javascript
ScrollTrigger.batch(".item", {
  onEnter: (elements) => {
    gsap.to(elements, { autoAlpha: 1, y: 0, stagger: 0.1 });
  },
  onLeaveBack: (elements) => {
    gsap.to(elements, { autoAlpha: 0, y: 30 });
  },
  start: "top 85%"
});
```

## 刷新 · `ScrollTrigger.refresh()`

**何时必须 refresh**：
- 图片懒加载完成（`img.onload`）
- 字体加载完成（`document.fonts.ready`）
- DOM 增删
- 路由切换后内容变化
- 折叠面板展开/收起

```javascript
document.fonts.ready.then(() => ScrollTrigger.refresh());

window.addEventListener("load", () => ScrollTrigger.refresh());
```

## 清理 · 必做

SPA / 路由切换前：
```javascript
ScrollTrigger.getAll().forEach(t => t.kill());
```

React / Vue / Svelte 里用 framework cleanup（见 `references/react.md` `references/frameworks.md`）。

## ScrollSmoother（平滑滚动 · 插件）

```javascript
import { ScrollSmoother } from "gsap/ScrollSmoother";
gsap.registerPlugin(ScrollTrigger, ScrollSmoother);

ScrollSmoother.create({
  wrapper: "#smooth-wrapper",
  content: "#smooth-content",
  smooth: 1.5,         // 平滑度（秒）
  effects: true,       // 允许 data-speed / data-lag 元素
  normalizeScroll: true
});
```

HTML：
```html
<div id="smooth-wrapper">
  <div id="smooth-content">
    <section data-speed="0.5">慢速视差</section>
    <section data-speed="1.5">快速视差</section>
  </div>
</div>
```

**注意**：ScrollSmoother 跟原生 `position: fixed` / `position: sticky` 有冲突，需要用其 `position-fixed` class 替代。

## 常用 start / end 写法

- `"top top"` · `"top center"` · `"top 80%"` · `"center center"` · `"bottom 100"` 等
- `"+=300"` · `"+=100%"`（相对，视口或元素高度的倍数）
- `() => "+=" + window.innerHeight`（动态）

## 反模式

- ❌ `setTimeout(() => ScrollTrigger.refresh(), 1000)` — 用 `document.fonts.ready` / `img.onload` 等真实事件。
- ❌ 1000 个 `.item` 各建 ScrollTrigger — 用 `batch()`。
- ❌ pin + scrub 时 trigger 元素本身设 `position: relative` 后又改 transform — 容易导致 pin 计算错乱，pin 容器要清爽。
- ❌ 忘了 `kill()` 导致 SPA 内残留滚动触发器，旧页面动画在新页面触发。

## 调试

```javascript
ScrollTrigger.create({
  trigger: ".x",
  start: "top center",
  end: "bottom center",
  markers: true          // 开发期开标记可视化
});
```

## 资源

- 官方 ScrollTrigger 文档：https://gsap.com/docs/v3/Plugins/ScrollTrigger/
