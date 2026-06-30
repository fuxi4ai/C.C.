# GSAP in React / Next.js

> 加载条件：用户在 React / Next.js 项目里写 GSAP，或问 useGSAP / SSR / cleanup。

## 安装

```bash
npm install gsap @gsap/react
```

`@gsap/react` 提供官方 `useGSAP` hook。**强烈推荐**用它而非裸 `useEffect`。

## 标准写法 · `useGSAP`

```jsx
import { useRef } from "react";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(useGSAP);   // 注册一次

export function Hero() {
  const container = useRef(null);

  useGSAP(() => {
    // 所有选择器自动作用域到 container 内
    gsap.from(".title", { y: 50, autoAlpha: 0, duration: 0.8 });
    gsap.from(".cta",   { y: 30, autoAlpha: 0, delay: 0.3 });
  }, { scope: container });
  // 卸载时自动 revert（清理 tween + 还原 inline style）

  return (
    <section ref={container}>
      <h1 className="title">Welcome</h1>
      <button className="cta">Start</button>
    </section>
  );
}
```

`useGSAP` 的好处：
- 自动 cleanup（组件卸载时调用 `ctx.revert()`）
- `scope` 限定选择器范围（避免选到组件外元素）
- 适配 React Strict Mode（双调用不会重复创建动画）

## 依赖与重跑

```jsx
useGSAP(() => {
  gsap.to(".bar", { width: `${progress}%` });
}, { scope: containerRef, dependencies: [progress] });
// progress 变化时重跑（类似 useEffect deps）
```

## 直接操作 ref（无选择器）

```jsx
const boxRef = useRef(null);

useGSAP(() => {
  gsap.to(boxRef.current, { x: 100 });
}, { scope: containerRef });
```

## ScrollTrigger in React

```jsx
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(useGSAP, ScrollTrigger);

export function ScrollSection() {
  const container = useRef(null);

  useGSAP(() => {
    gsap.to(".panel", {
      x: -1000,
      scrollTrigger: {
        trigger: ".panel",
        start: "top top",
        end: "+=2000",
        scrub: true
      }
    });
  }, { scope: container });
  // 卸载自动 kill ScrollTrigger

  return <section ref={container}><div className="panel" /></section>;
}
```

## 备选：`gsap.context`（旧版 React API）

如果不想用 `@gsap/react` 包：

```jsx
import { useEffect, useRef } from "react";
import gsap from "gsap";

export function Foo() {
  const container = useRef(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.to(".x", { x: 100 });
    }, container);  // scope

    return () => ctx.revert();  // 卸载清理
  }, []);

  return <div ref={container}><div className="x" /></div>;
}
```

`useGSAP` 本质是对 `gsap.context` 的薄封装，推荐前者。

## Next.js / SSR 注意

GSAP 是浏览器端库，在 SSR 时不能直接跑动画代码：

```jsx
// app/components/Hero.tsx
"use client";   // App Router 必须

import { useRef } from "react";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";

// ...
```

**Pages Router**：组件用 `dynamic` 动态加载 `{ ssr: false }`：
```jsx
import dynamic from "next/dynamic";
const Hero = dynamic(() => import("../components/Hero"), { ssr: false });
```

注册插件可以放 client 侧入口（如 `app/providers.tsx`）：
```jsx
"use client";
import { useEffect } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

export function GsapProvider({ children }) {
  useEffect(() => {
    gsap.registerPlugin(ScrollTrigger);
  }, []);
  return <>{children}</>;
}
```

## 反模式

- ❌ `useEffect(() => { gsap.to(".x", {...}) }, [])` 没 cleanup — 卸载残留、Strict Mode 双跑。改 `useGSAP`。
- ❌ 在 `useGSAP` callback 外裸调 `gsap.to` — 不被 context 管，卸载不清理。
- ❌ 没设 `scope` 的 `useGSAP` 用 `".x"` 选择器 — 全局抓元素，组件复用时互相干扰。
- ❌ Next.js App Router 忘加 `"use client"` — Server Component 跑 GSAP 报错。
- ❌ SSR 阶段访问 `window` / `document` — 包 `if (typeof window !== "undefined")` 或用 `useEffect`。

## 资源

- 官方 `@gsap/react` 文档：https://gsap.com/resources/React/
- `useGSAP` hook：https://gsap.com/docs/v3/GSAP/UsegsapReactJS/
