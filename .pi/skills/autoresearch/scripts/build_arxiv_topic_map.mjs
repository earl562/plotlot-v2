#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

function parseArgs(argv) {
  const args = {
    input: "docs/research/arxiv-abstracts.json",
    output: "docs/research/arxiv-topic-map.md",
  };

  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--input") args.input = argv[++i];
    else if (a === "--output") args.output = argv[++i];
  }

  return args;
}

const TOPICS = [
  {
    key: "harness-engineering",
    label: "Harness engineering / agent runtimes",
    re: /harness|runtime|middleware|orchestrat|controller|agentic system|agent framework/i,
  },
  {
    key: "memory",
    label: "Memory / long-term state",
    re: /memory|episodic|long[- ]term|context store|retrieval|rag/i,
  },
  {
    key: "skills",
    label: "Skills / skill marketplaces / skill portability",
    re: /skill|toolbox|marketplace|capabilit(y|ies)|portable/i,
  },
  {
    key: "governance-security",
    label: "Governance / security / red-teaming",
    re: /security|jailbreak|red[- ]team|policy|permission|governance|least[- ]privilege|privacy/i,
  },
  {
    key: "evaluation",
    label: "Evaluation / benchmarks / tracing",
    re: /benchmark|evaluation|eval|metrics|judge|gold|dataset|trace/i,
  },
  {
    key: "multi-agent",
    label: "Multi-agent teams / delegation",
    re: /multi[- ]agent|team|delegat|collaboration|coordination|subagent/i,
  },
  {
    key: "context-engineering",
    label: "Context engineering / long-context",
    re: /context|long[- ]context|compression|summari(s|z)e|compaction|prompt/i,
  },
  {
    key: "terminal-cli",
    label: "Terminal / CLI / TUI agents",
    re: /terminal|cli|shell|tui/i,
  },
  {
    key: "geospatial-aec",
    label: "AEC / geospatial / earth observation",
    re: /geospatial|earth|satellite|remote sensing|construction|engineering|aec|building/i,
  },
];

function assignTopics(title, abstract) {
  const text = `${title || ""}\n${abstract || ""}`;
  const hits = [];
  for (const t of TOPICS) {
    if (t.re.test(text)) hits.push(t.key);
  }
  if (hits.length === 0) hits.push("uncategorized");
  return hits;
}

function mdLink(item) {
  const title = item.title || "(missing title)";
  const absUrl = item.absUrl || `https://arxiv.org/abs/${item.arxivId}`;
  return `- [${item.arxivId}](${absUrl}) — ${title}`;
}

const args = parseArgs(process.argv);
const payload = JSON.parse(fs.readFileSync(args.input, "utf-8"));
const items = (payload.items || []).filter((x) => x.status === "ok");

/** @type {Record<string, any[]>} */
const byTopic = {};
for (const i of items) {
  const topics = assignTopics(i.title, i.abstract);
  for (const t of topics) {
    byTopic[t] = byTopic[t] || [];
    byTopic[t].push(i);
  }
}

for (const k of Object.keys(byTopic)) {
  byTopic[k].sort((a, b) => (a.arxivId < b.arxivId ? -1 : a.arxivId > b.arxivId ? 1 : 0));
}

const lines = [];
lines.push("# arXiv Topic Map (from Obsidian vault)\n");
lines.push(`Generated from: \`${path.basename(args.input)}\``);
lines.push(`Count (ok): **${items.length}**`);
lines.push("");

for (const t of TOPICS) {
  const list = byTopic[t.key] || [];
  lines.push(`## ${t.label} (${list.length})\n`);
  for (const item of list) lines.push(mdLink(item));
  lines.push("");
}

const unc = byTopic["uncategorized"] || [];
lines.push(`## Uncategorized (${unc.length})\n`);
for (const item of unc) lines.push(mdLink(item));
lines.push("");

fs.mkdirSync(path.dirname(args.output), { recursive: true });
fs.writeFileSync(args.output, lines.join("\n") + "\n", "utf-8");

console.log(JSON.stringify({ output: args.output }, null, 2));
