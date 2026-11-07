# `gsap.utils` · 工具函数速查

> 加载条件：用户用到 `clamp` / `mapRange` / `random` / `snap` / `interpolate` / `wrap` / `pipe` / `toArray` / `normalize` 等工具。

`gsap.utils` 是一组**框架无关的纯函数**，跟动画无直接关系但配合很顺手。可单独 import：

```javascript
import { gsap } from "gsap";
const { clamp, mapRange, random, snap, toArray, wrap, pipe, interpolate } = gsap.utils;
```

或直接 `gsap.utils.clamp(...)` 用。

---

## 数值映射

### `clamp(min, max, value?)` · 限幅

```javascript
gsap.utils.clamp(0, 100, 150);    // 100
gsap.utils.clamp(0, 100, -5);     // 0

const clamper = gsap.utils.clamp(0, 100);  // 柯里化
clamper(120);                              // 100
```

### `mapRange(inMin, inMax, outMin, outMax, value?)` · 区间映射

```javascript
gsap.utils.mapRange(0, 100, 0, 1, 50);    // 0.5

// 鼠标 x（0~window.innerWidth）→ 旋转角（-30~30）
const mouseToRot = gsap.utils.mapRange(0, window.innerWidth, -30, 30);
gsap.to(".x", { rotation: mouseToRot(event.clientX) });
```

### `normalize(min, max, value?)` · 归一化到 0~1

```javascript
gsap.utils.normalize(100, 500, 300);   // 0.5
```

### `interpolate(start, end, progress)` · 插值

```javascript
gsap.utils.interpolate(0, 100, 0.5);      // 50
gsap.utils.interpolate("#ff0000", "#0000ff", 0.5);   // 颜色插值
gsap.utils.interpolate([0, 10, 100], 0.5);            // 在数组里插
```

---

## 随机

### `random(min, max, increment?, returnFunction?)`

```javascript
gsap.utils.random(0, 100);              // 0~100 浮点
gsap.utils.random(0, 100, 10);          // 0,10,20,...,100
gsap.utils.random(-50, 50, 1, true);    // 返回**函数**，每次调用产生新随机数
gsap.utils.random(["red", "blue", "green"]);   // 数组随机选一

// 配合 stagger：每个元素随机 y
gsap.from(".item", { y: () => gsap.utils.random(-100, 100), stagger: 0.05 });
```

---

## 离散化

### `snap(increment, value?)`

```javascript
gsap.utils.snap(10, 23);          // 20（snap 到 10 的倍数）
gsap.utils.snap(0.5, 1.7);        // 1.5

gsap.utils.snap([0, 50, 100, 200], 80);   // 100（snap 到给定数组）

// ScrollTrigger 中用 snap
ScrollTrigger.create({
  snap: { snapTo: 1 / 10, duration: 0.3 }   // snap 到每 10% 位置
});
```

---

## 循环

### `wrap(min, max, value?)` · 取模循环

```javascript
gsap.utils.wrap(0, 360, 380);     // 20（角度循环）
gsap.utils.wrap(0, 10, -3);       // 7

// 颜色数组循环
const colors = ["red", "green", "blue"];
gsap.utils.wrap(colors)(5);       // "green"（5 % 3 = 2 → colors[2] = "blue"...）
```

### `wrapYoyo(min, max, value?)` · 来回

```javascript
gsap.utils.wrapYoyo(0, 100, 150);   // 50（超过 100 后反向）
```

---

## 组合 / 管道

### `pipe(fn1, fn2, ...)` · 函数串联

```javascript
const clamp = gsap.utils.clamp(0, 100);
const snap  = gsap.utils.snap(10);
const process = gsap.utils.pipe(clamp, snap);

process(123);   // clamp → 100, snap → 100
process(47);    // 47 → 50
```

适合配合 `mapRange` + `clamp` + `snap` 链式处理输入。

---

## DOM 工具

### `toArray(target)` · 选择器 / NodeList / 单元素 → 数组

```javascript
gsap.utils.toArray(".item");                 // [el, el, el]
gsap.utils.toArray(document.querySelectorAll("p"));   // [...]
gsap.utils.toArray(singleEl);                // [singleEl]

// 然后可以 forEach / map
gsap.utils.toArray(".card").forEach((card, i) => {
  gsap.from(card, { y: 50, delay: i * 0.1 });
});
```

### `selector(scope)` · 限定 scope 的选择器

```javascript
const q = gsap.utils.selector(containerRef);
gsap.to(q(".inside"), { x: 100 });   // 只选 containerRef 内的 .inside
```

---

## 单位 / 字符串

### `unitize(fn, unit)` · 给函数返回值加单位

```javascript
const toPx = gsap.utils.unitize(gsap.utils.clamp(0, 100), "px");
toPx(50);   // "50px"
```

### `splitColor(value)` · 拆 RGB

```javascript
gsap.utils.splitColor("#ff0000");        // [255, 0, 0]
gsap.utils.splitColor("rgb(255,0,0)");   // [255, 0, 0]
```

---

## 常用搭配模式

### 鼠标驱动 → 限幅 + 映射 + snap

```javascript
const card = document.querySelector(".card");
const mapX = gsap.utils.mapRange(-200, 200, -15, 15);
const clamp = gsap.utils.clamp(-15, 15);
const snap = gsap.utils.snap(0.5);
const process = gsap.utils.pipe(mapX, clamp, snap);

card.addEventListener("mousemove", e => {
  const rect = card.getBoundingClientRect();
  const x = e.clientX - rect.left - rect.width / 2;
  gsap.to(card, { rotationY: process(x), duration: 0.3 });
});
```

### 批量随机入场

```javascript
gsap.from(".particle", {
  x: () => gsap.utils.random(-200, 200),
  y: () => gsap.utils.random(-200, 200),
  rotation: () => gsap.utils.random(-180, 180),
  duration: () => gsap.utils.random(0.6, 1.2),
  stagger: 0.02,
  ease: "power2.out"
});
```

---

## 反模式

- ❌ 自己手写 `Math.max(min, Math.min(max, v))` — 用 `gsap.utils.clamp` 更清晰。
- ❌ 自己造伪随机 — `gsap.utils.random` 支持 increment/数组随机/可重复函数。
- ❌ `Array.from(document.querySelectorAll(...))` — 用 `gsap.utils.toArray` 更简短，且接受多种输入。
