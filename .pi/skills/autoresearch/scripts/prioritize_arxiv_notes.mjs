#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

function parseArgs(argv) {
  const args = {
    abstracts: "docs/research/arxiv-abstracts.json",
    notesDir: "docs/research/arxiv-notes",
    output: "docs/research/arxiv-topdown-queue.md",
    limit: 60,
  };

  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--abstracts") args.abstracts = argv[++i];
    else if (a === "--notes-dir") args.notesDir = argv[++i];
    else if (a === "--output") args.output = argv[++i];
    else if (a === "--limit") args.limit = Number(argv[++i] || args.limit);
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

function keywordScore(text) {
  const t = (text || "").toLowerCase();
  const rules = [
    ["runtime governance", 12],
    ["governance", 10],
    ["policy", 8],
    ["permission", 8],
    ["sandbox", 8],
    ["security", 10],
    ["red-team", 9],
    ["jailbreak", 9],
    ["privacy", 7],
    ["least-privilege", 10],
    ["alara", 10],
    ["protocol", 8],
    ["mcp", 8],
    ["agent control", 10],
    ["admission control", 10],
    ["harness", 9],
    ["agent harness", 10],
    ["skill", 6],
    ["skills", 6],
    ["memory", 6],
    ["long-term", 5],
    ["benchmark", 5],
    ["evaluation", 5],
    ["trace", 5],
    ["observability", 7],
    ["multi-agent", 4],
  ];

  let score = 0;
  for (const [kw, w] of rules) {
    if (t.includes(kw)) score += w;
  }
  return score;
}

function tier(item) {
  const title = (item.title || "").toLowerCase();
  const abs = (item.abstract || "").toLowerCase();
  const text = `${title}\n${abs}`;

  // P0: governance/security + harness runtime infrastructure
  if (
    /governance|policy|permission|sandbox|security|jailbreak|red-team|least-privilege|admission control|agent control/.test(
      text
    )
  )
    return "P0";

  // P1: memory + context engineering
  if (/memory|long-context|compaction|retrieval|rag|episodic/.test(text)) return "P1";

  // P2: evaluation + benchmarks
  if (/benchmark|evaluation|eval|dataset|trace|in production/.test(text)) return "P2";

  // P3: skills + protocols
  if (/skill|mcp|protocol|agent communication/.test(text)) return "P3";

  return "P4";
}

function mdRow(item, notePath, status, score, p) {
  const relNote = notePath ? path.relative(process.cwd(), notePath) : null;
  const noteLink = relNote ? `[note](${relNote})` : "(missing note)";
  const absUrl = item.absUrl || `https://arxiv.org/abs/${item.arxivId}`;
  const title = item.title || "(missing title)";

  return `- **${p}** (${score}) [${item.arxivId}](${absUrl}) — ${title}  — ${noteLink} — _${status}_`;
}

const args = parseArgs(process.argv);
const abstracts = JSON.parse(fs.readFileSync(args.abstracts, "utf-8"));

// Dedupe by arXiv ID (some sources contain repeated URLs/entries)
const rawItems = (abstracts.items || []).filter((x) => x.status === "ok");
const items = [];
const seenIds = new Set();
for (const it of rawItems) {
  const id = it.arxivId;
  if (!id) continue;
  if (seenIds.has(id)) continue;
  seenIds.add(id);
  items.push(it);
}
const dupesDropped = rawItems.length - items.length;

// Map arxivId -> note status
const noteFiles = fs
  .readdirSync(args.notesDir)
  .filter((f) => f.endsWith(".md"))
  .map((f) => path.join(args.notesDir, f));

/** @type {Map<string, {path: string, status: string}>} */
const noteById = new Map();
for (const f of noteFiles) {
  const md = fs.readFileSync(f, "utf-8");
  const fm = readFrontmatter(md);
  const id = (fm.arxiv_id || path.basename(f, ".md")).replace(/"/g, "");
  const status = (fm.status || "unknown").replace(/"/g, "");
  noteById.set(id, { path: f, status });
}

const enriched = items.map((it) => {
  const note = noteById.get(it.arxivId);
  const status = note?.status || "missing";
  const score = keywordScore(`${it.title}\n${it.abstract}`);
  const p = tier(it);
  return {
    ...it,
    notePath: note?.path || null,
    noteStatus: status,
    score,
    priority: p,
  };
});

const reviewed = enriched.filter((x) => x.noteStatus === "reviewed");
const stubs = enriched.filter((x) => x.noteStatus !== "reviewed");

stubs.sort((a, b) => {
  const pOrder = (p) => (p === "P0" ? 0 : p === "P1" ? 1 : p === "P2" ? 2 : p === "P3" ? 3 : 4);
  const d = pOrder(a.priority) - pOrder(b.priority);
  if (d !== 0) return d;
  const ds = b.score - a.score;
  if (ds !== 0) return ds;
  return a.arxivId.localeCompare(b.arxivId);
});

const lines = [];
lines.push("# arXiv Top-Down Review Queue\n");
lines.push(`Generated from: \`${path.basename(args.abstracts)}\``);
lines.push(`Total papers: **${items.length}**`);
if (dupesDropped > 0) lines.push(`Duplicates dropped: **${dupesDropped}**`);
lines.push(`Reviewed: **${reviewed.length}**`);
lines.push(`Remaining: **${stubs.length}**`);
lines.push("");
lines.push("Priority tiers:");
lines.push("- **P0**: governance/security/permissions/sandbox/protocol control");
lines.push("- **P1**: memory/context engineering");
lines.push("- **P2**: evaluation/benchmarks/tracing");
lines.push("- **P3**: skills/protocol ecosystems");
lines.push("- **P4**: other");
lines.push("");

lines.push("## Next up (highest priority stubs)\n");
for (const it of stubs.slice(0, args.limit)) {
  lines.push(mdRow(it, it.notePath, it.noteStatus, it.score, it.priority));
}
lines.push("");

lines.push("## Already reviewed\n");
reviewed
  .slice()
  .sort((a, b) => a.arxivId.localeCompare(b.arxivId))
  .forEach((it) => {
    lines.push(mdRow(it, it.notePath, it.noteStatus, it.score, "✅"));
  });
lines.push("");

fs.mkdirSync(path.dirname(args.output), { recursive: true });
fs.writeFileSync(args.output, lines.join("\n") + "\n", "utf-8");

console.log(JSON.stringify({ output: args.output, reviewed: reviewed.length, remaining: stubs.length }, null, 2));
