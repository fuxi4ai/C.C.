# GSAP in Vue / Svelte / 其他框架

> 加载条件：用户在 Vue（Composition / Options） / Svelte / SvelteKit / Nuxt 等框架里写 GSAP。

## Vue 3 · Composition API（推荐）

```vue
<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);

const container = ref(null);
let ctx;

onMounted(() => {
  ctx = gsap.context(() => {
    gsap.from(".title", { y: 30, autoAlpha: 0 });
    gsap.to(".panel", {
      x: -500,
      scrollTrigger: { trigger: ".panel", scrub: true }
    });
  }, container.value);   // scope
});

onUnmounted(() => {
  ctx?.revert();         // 必须 cleanup
});
</script>

<template>
  <section ref="container">
    <h1 class="title">Hi</h1>
    <div class="panel"></div>
  </section>
</template>
```

**核心模式**：`onMounted` 创建 `gsap.context`，`onUnmounted` 调 `ctx.revert()`。

## Vue 3 · Options API

```vue
<script>
import gsap from "gsap";

export default {
  mounted() {
    this.ctx = gsap.context(() => {
      gsap.to(".x", { x: 100 });
    }, this.$el);
  },
  beforeUnmount() {
    this.ctx?.revert();
  }
};
</script>
```

## Nuxt 3

GSAP 是浏览器侧库，需要 client-only：

```vue
<ClientOnly>
  <MyAnimatedHero />
</ClientOnly>
```

或在 plugin 注册（`plugins/gsap.client.ts`，`.client` 后缀表示仅客户端）：
```typescript
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

export default defineNuxtPlugin(() => {
  gsap.registerPlugin(ScrollTrigger);
  return { provide: { gsap } };
});
```

## Svelte / SvelteKit

```svelte
<script>
  import { onMount, onDestroy } from "svelte";
  import gsap from "gsap";
  import { ScrollTrigger } from "gsap/ScrollTrigger";
  gsap.registerPlugin(ScrollTrigger);

  let container;
  let ctx;

  onMount(() => {
    ctx = gsap.context(() => {
      gsap.from(".title", { y: 30, autoAlpha: 0 });
    }, container);
  });

  onDestroy(() => ctx?.revert());
</script>

<section bind:this={container}>
  <h1 class="title">Hi</h1>
</section>
```

### SvelteKit SSR

GSAP 要走 client，需要：
```javascript
// +layout.svelte / +page.svelte
import { browser } from "$app/environment";
import { onMount } from "svelte";

onMount(async () => {
  if (browser) {
    const { default: gsap } = await import("gsap");
    // ...
  }
});
```

或者在 `+page.ts` 设 `export const ssr = false`（不推荐全关 SSR）。

## Solid · Qwik · Astro

| 框架 | 关键点 |
|------|--------|
| **Solid** | `onMount` + `onCleanup`；用 `ref` 取元素；`gsap.context` 一样工作 |
| **Qwik** | `useVisibleTask$(() => {...})` 替代 `useEffect`（client only） |
| **Astro** | 默认静态、JS 不跑；用 `client:load` / `client:visible` directive 让组件水合（hydrate） |

## 通用三原则

1. **GSAP 代码只在客户端生命周期跑**：`onMounted` / `onMount` / `useEffect` / `useVisibleTask$` 等。
2. **必带 cleanup**：`ctx.revert()` 或 `tween.kill()` + `ScrollTrigger.getAll().forEach(t => t.kill())`。
3. **scope 限定选择器**：`gsap.context(() => {...}, scopeEl)` 把 `.x` 锁在 `scopeEl` 内，避免跨组件污染。

## 反模式

- ❌ Nuxt / SvelteKit / Next 顶层直接 `import gsap` 然后 `gsap.to(...)` — SSR 报错。改 client-only。
- ❌ 没 cleanup 的 framework 组件 — 路由切换累积 ScrollTrigger，卡死。
- ❌ Vue 用 `watch` 跑 GSAP 但不清理上一次的 tween — 改 `gsap.to(target, { overwrite: true, ... })` 或显式 `tween.kill()`。
- ❌ Svelte 反应式块（`$:`）里裸 `gsap.to` — 反应式触发太频繁，每次都新建 tween。改 `tween.invalidate().restart()` 或封装。

## 资源

- 官方 React 集成：https://gsap.com/resources/React/
- 官方 Vue：https://gsap.com/resources/Vue/
- Svelte（社区）：https://github.com/Wykks/svelte-gsap
