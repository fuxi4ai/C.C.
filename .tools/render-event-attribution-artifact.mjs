#!/usr/bin/env node
/**
 * Rebuild the Event Attribution Ledger's local HTML mirror from its canonical
 * Markdown source.  It intentionally does not calculate market data or edit
 * the ledger: publishing is a pure, reviewable rendering step.
 *
 * ⚠ 非生产渲染器（2026-08-17 VV 二轮终验）：EAL 生产页唯一渲染器＝值守班三时段富版模板
 *   （剑酒青丘/frameworks/eal-三时段图-渲染器.html · 按 event-attribution-watch SKILL 规范组装）。
 *   本通用 renderer 不再直接发布生产页；cells() 哨兵修复保留（转义管道拆列）。
 */
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";

const brain = resolve(import.meta.dirname, "..");
const source = resolve(brain, "剑酒青丘/frameworks/事件归因台账.md");
const destination = resolve(brain, "references/scheduled-live-mirror/artifacts/event-attribution-ledger/index.html");
const write = process.argv.includes("--write");
const previewArg = process.argv.indexOf("--preview");
const previewPath = previewArg >= 0 ? process.argv[previewArg + 1] : null;

function escape(value) {
  return value.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
}

function inline(value) {
  return escape(value)
    .replace(/`([^`]+)`/gu, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/gu, "<strong>$1</strong>")
    .replace(/~~([^~]+)~~/gu, "<s>$1</s>")
    .replace(/\[([^\]]+)\]\((https?:\/\/[^)]+)\)/gu, '<a href="$2" rel="noreferrer">$1</a>');
}

function cells(line) {
  const marker = "";
  return line
    .trim()
    .replace(/^\||\|$/gu, "")
    .replaceAll("\\|", marker)
    .split("|")
    .map((cell) => inline(cell.replaceAll(marker, "|").trim()));
}

function table(lines) {
  const head = cells(lines[0]);
  const body = lines.slice(2).map(cells);
  return `<div class="table-wrap"><table><thead><tr>${head.map((cell) => `<th>${cell}</th>`).join("")}</tr></thead><tbody>${body.map((row) => `<tr>${row.map((cell) => `<td>${cell}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
}

function markdown(markdown) {
  const lines = markdown.replace(/\r/g, "").split("\n");
  const output = [];
  let index = 0;
  let paragraph = [];
  const flush = () => {
    if (paragraph.length) output.push(`<p>${inline(paragraph.join(" "))}</p>`);
    paragraph = [];
  };
  while (index < lines.length) {
    const line = lines[index];
    if (/^```/u.test(line)) {
      flush();
      const code = [];
      index += 1;
      while (index < lines.length && !/^```/u.test(lines[index])) code.push(lines[index++]);
      output.push(`<pre><code>${escape(code.join("\n"))}</code></pre>`);
    } else if (/^\|.*\|$/u.test(line) && /^\|?\s*:?-{3,}/u.test(lines[index + 1] ?? "")) {
      flush();
      const rows = [line, lines[++index]];
      while (/^\|.*\|$/u.test(lines[index + 1] ?? "")) rows.push(lines[++index]);
      output.push(table(rows));
    } else if (/^(#{1,3})\s+(.+)$/u.test(line)) {
      flush();
      const [, marks, title] = line.match(/^(#{1,3})\s+(.+)$/u);
      output.push(`<h${marks.length}>${inline(title)}</h${marks.length}>`);
    } else if (/^>\s?/u.test(line)) {
      flush();
      output.push(`<blockquote>${inline(line.replace(/^>\s?/u, ""))}</blockquote>`);
    } else if (/^[-*]\s+/u.test(line)) {
      flush();
      const entries = [];
      while (/^[-*]\s+/u.test(lines[index] ?? "")) entries.push(`<li>${inline(lines[index++].replace(/^[-*]\s+/u, ""))}</li>`);
      index -= 1;
      output.push(`<ul>${entries.join("")}</ul>`);
    } else if (/^---+\s*$/u.test(line)) {
      flush();
      output.push("<hr>");
    } else if (line.trim() === "") {
      flush();
    } else {
      paragraph.push(line.trim());
    }
    index += 1;
  }
  flush();
  return output.join("\n");
}

const input = readFileSync(source, "utf8");
const frontmatter = input.match(/^---\n([\s\S]*?)\n---\n/u)?.[1] ?? "";
const body = input.replace(/^---\n[\s\S]*?\n---\n/u, "");
const title = frontmatter.match(/^title:\s*(.+)$/mu)?.[1] ?? "事件归因台账";
const updated = frontmatter.match(/^updated:\s*(\d{4}-\d{2}-\d{2})$/mu)?.[1] ?? "未知";
const snapshot = frontmatter.match(/^artifact_snapshot:\s*(\d{4}-\d{2}-\d{2}[^\n]*)$/mu)?.[1] ?? `截至 ${updated}`;
const renderedAt = new Date().toISOString();
const html = `<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${escape(title)}</title><meta name="description" content="剑酒青丘事件归因台账的可追溯发布快照。">
<style>
:root{color-scheme:light;--paper:#f6efe0;--ink:#3a3126;--red:#b23b2e;--jade:#2e7d6e;--camel:#a3763f;--line:#e6dbc4}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.75 "Source Han Serif SC","Noto Serif CJK SC","Songti SC",Georgia,serif}main{max-width:1180px;margin:auto;padding:40px 28px 72px}.mast{border-block:2px solid var(--ink);padding:24px 0 20px;margin-bottom:36px}.eyebrow{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--camel)}h1,h2,h3{line-height:1.25;margin:1.7em 0 .55em;font-weight:700}h1{font-size:clamp(30px,5vw,54px);margin:.2em 0}h2{font-size:28px;border-bottom:1px solid var(--line);padding-bottom:.35em}h3{font-size:21px}.meta{display:flex;flex-wrap:wrap;gap:10px;font-size:14px;color:#62584b}.chip{border:1px solid var(--line);padding:3px 9px;border-radius:999px;background:#fbf6eb}p{margin:0 0 1em}blockquote{margin:1.2em 0;padding:13px 18px;border-left:4px solid var(--camel);background:#f0e5d1}code{font:13px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;background:#eee3cf;padding:.1em .3em;border-radius:3px}pre{overflow:auto;background:#302a23;color:#f7efdf;padding:16px;border-radius:6px}pre code{background:none;padding:0}.table-wrap{overflow:auto;margin:1.25em 0}table{width:100%;border-collapse:collapse;font-size:14px}th,td{padding:9px 10px;border:1px solid var(--line);vertical-align:top}th{background:#eadcc4;text-align:left}tr:nth-child(even){background:#fbf6eb}a{color:var(--jade)}hr{border:0;border-top:1px solid var(--line);margin:2em 0}footer{margin-top:54px;padding-top:16px;border-top:1px solid var(--line);font-size:13px;color:#62584b}@media(max-width:650px){main{padding:24px 15px}table{font-size:12px}}
</style></head><body><main><header class="mast"><div class="eyebrow">剑酒青丘 · 解释层 overlay · 非预警器</div><h1>${escape(title)}</h1><div class="meta"><span class="chip">快照 <strong>${escape(snapshot)}</strong></span><span class="chip">规则书更新 <strong>${escape(updated)}</strong></span><span class="chip">本次渲染 ${escape(renderedAt)}</span></div></header>${markdown(body)}<footer>发布器：canonical Markdown → self-contained HTML。此发布不改变规则书、量级带或数据库。</footer></main></body></html>\n`;

if (write) {
  console.error("非生产渲染器保险丝（2026-08-17 VV 三轮终验）：--write 已禁用，禁止覆盖正式 mirror。生产页唯一渲染器＝值守班三时段富版模板（剑酒青丘/frameworks/eal-三时段图-渲染器.html）；本地预览请用 --preview <path> 写独立路径。");
  process.exit(1);
}
if (previewPath) {
  const out = resolve(previewPath);
  mkdirSync(dirname(out), { recursive: true, mode: 0o700 });
  writeFileSync(out, html, { encoding: "utf8", mode: 0o600 });
}
process.stdout.write(`${JSON.stringify({ source, destination, rendered_at: renderedAt, snapshot, wrote: false, preview: previewPath ? resolve(previewPath) : null, bytes: Buffer.byteLength(html) })}\n`);
