#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

function parseArgs(argv) {
  const args = {
    notesDir: "docs/research/github-notes",
    output: "docs/research/github-notes-status.md",
  };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--notes-dir") args.notesDir = argv[++i];
    else if (a === "--output") args.output = argv[++i];
  }
  return args;
}

function readFrontmatter(md) {
  if (!md.startsWith("---")) return {};
  const end = md.indexOf("\n---", 3);
  if (end === -1) return {};
  const block = md.slice(3, end).trim();
  const out = {};
  for (const line of block.split(/\r?\n/)) {
    const m = line.match(/^([a-zA-Z0-9_\-]+):\s*(.*)$/);
    if (!m) continue;
    out[m[1]] = m[2];
  }
  return out;
}

const args = parseArgs(process.argv);
const files = fs
  .readdirSync(args.notesDir)
  .filter((f) => f.endsWith(".md"))
  .map((f) => path.join(args.notesDir, f));

const rows = [];
for (const f of files) {
  const md = fs.readFileSync(f, "utf-8");
  const fm = readFrontmatter(md);
  const status = (fm.status || "unknown").replace(/"/g, "");
  const repo = (fm.repo || path.basename(f, ".md")).replace(/"/g, "");
  rows.push({ repo, status, file: f });
}

rows.sort((a, b) => (a.status < b.status ? -1 : a.status > b.status ? 1 : a.repo.localeCompare(b.repo)));

const reviewed = rows.filter((r) => r.status === "reviewed");
const stub = rows.filter((r) => r.status === "stub");

const lines = [];
lines.push("# GitHub Notes Status\n");
lines.push(`Total: **${rows.length}**`);
lines.push(`Reviewed: **${reviewed.length}**`);
lines.push(`Stub: **${stub.length}**`);
lines.push("");

lines.push("## Reviewed\n");
for (const r of reviewed) {
  const rel = path.relative(process.cwd(), r.file);
  lines.push(`- [${r.repo}](${rel})`);
}
lines.push("");

lines.push("## Stubs (to review)\n");
for (const r of stub) {
  const rel = path.relative(process.cwd(), r.file);
  lines.push(`- [${r.repo}](${rel})`);
}
lines.push("");

fs.mkdirSync(path.dirname(args.output), { recursive: true });
fs.writeFileSync(args.output, lines.join("\n") + "\n", "utf-8");

console.log(JSON.stringify({ output: args.output, reviewed: reviewed.length, stub: stub.length }, null, 2));
