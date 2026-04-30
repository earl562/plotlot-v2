#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

function parseArgs(argv) {
  const args = {
    input: "docs/research/obsidian-urls.json",
    output: "docs/research/obsidian-url-map.md",
  };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--input") args.input = argv[++i];
    else if (a === "--output") args.output = argv[++i];
  }
  return args;
}

function hostOf(url) {
  try {
    return new URL(url).host.toLowerCase();
  } catch {
    return "(invalid)";
  }
}

function bucket(url) {
  const host = hostOf(url);
  if (host === "(invalid)") return "invalid";

  if (host.endsWith("arxiv.org")) return "arxiv";
  if (host === "export.arxiv.org") return "arxiv";

  if (host === "github.com" || host.endsWith("github.com")) return "github";

  if (host === "x.com" || host === "twitter.com") return "x";

  if (
    host.endsWith("langchain.com") ||
    host.endsWith("openai.com") ||
    host.endsWith("anthropic.com") ||
    host.endsWith("badlogicgames.com")
  )
    return "vendor-blog";

  if (host.endsWith("ssrn.com")) return "ssrn";
  if (host.endsWith("ieee.org") || host.endsWith("ieeexplore.ieee.org")) return "ieee";
  if (host.endsWith("techrxiv.org")) return "techrxiv";

  if (host.endsWith("docs.langchain.com") || host.endsWith("documentation")) return "docs";

  return "other";
}

const args = parseArgs(process.argv);
const payload = JSON.parse(fs.readFileSync(args.input, "utf-8"));
const items = payload.items || [];

/** @type {Record<string, {url: string, sources: string[]}[]>} */
const byBucket = {};
/** @type {Record<string, number>} */
const byHost = {};

for (const it of items) {
  const b = bucket(it.url);
  byBucket[b] = byBucket[b] || [];
  byBucket[b].push(it);

  const h = hostOf(it.url);
  byHost[h] = (byHost[h] || 0) + 1;
}

for (const b of Object.keys(byBucket)) {
  byBucket[b].sort((a, b2) => (a.url < b2.url ? -1 : a.url > b2.url ? 1 : 0));
}

const hostRows = Object.entries(byHost)
  .sort((a, b2) => b2[1] - a[1])
  .slice(0, 25);

const lines = [];
lines.push("# Obsidian URL Map\n");
lines.push(`Generated from: \`${path.basename(args.input)}\``);
lines.push(`Total URLs: **${items.length}**`);
lines.push("");

lines.push("## Buckets\n");
for (const b of Object.keys(byBucket).sort()) {
  lines.push(`- **${b}**: ${byBucket[b].length}`);
}
lines.push("");

lines.push("## Top hosts\n");
for (const [h, n] of hostRows) {
  lines.push(`- ${h}: ${n}`);
}
lines.push("");

for (const b of Object.keys(byBucket).sort()) {
  lines.push(`## ${b} (${byBucket[b].length})\n`);
  for (const it of byBucket[b]) {
    const src = (it.sources || []).map((s) => path.basename(s)).join(", ");
    lines.push(`- ${it.url}${src ? `  _(sources: ${src})_` : ""}`);
  }
  lines.push("");
}

fs.mkdirSync(path.dirname(args.output), { recursive: true });
fs.writeFileSync(args.output, lines.join("\n") + "\n", "utf-8");

console.log(JSON.stringify({ output: args.output, buckets: Object.keys(byBucket).length }, null, 2));
