#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

function parseArgs(argv) {
  const args = {
    input: "docs/research/arxiv-abstracts.json",
    output: "docs/research/arxiv-abstracts.md",
  };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--input") args.input = argv[++i];
    else if (a === "--output") args.output = argv[++i];
  }
  return args;
}

const args = parseArgs(process.argv);
const payload = JSON.parse(fs.readFileSync(args.input, "utf-8"));
const items = (payload.items || []).filter((x) => x.status === "ok");

const lines = [];
lines.push("# arXiv Abstracts (from Obsidian vault)\n");
lines.push(`Generated from: \`${path.basename(args.input)}\``);
lines.push(`Count: **${items.length}**`);
lines.push("");

for (const it of items) {
  const absUrl = it.absUrl || `https://arxiv.org/abs/${it.arxivId}`;
  lines.push(`## ${it.arxivId} — ${it.title || "(missing title)"}`);
  lines.push("");
  lines.push(`- URL: ${absUrl}`);
  if (it.primaryCategory) lines.push(`- Primary category: \`${it.primaryCategory}\``);
  if (it.publishedAt) lines.push(`- Published: ${it.publishedAt}`);
  lines.push("");
  lines.push("### Abstract");
  lines.push("");
  lines.push(it.abstract ? it.abstract.trim() : "(missing abstract)");
  lines.push("");
}

fs.mkdirSync(path.dirname(args.output), { recursive: true });
fs.writeFileSync(args.output, lines.join("\n") + "\n", "utf-8");

console.log(JSON.stringify({ output: args.output }, null, 2));
