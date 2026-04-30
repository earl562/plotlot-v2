#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

function parseArgs(argv) {
  const args = {
    input: "docs/research/arxiv-abstracts.json",
    outDir: "docs/research/arxiv-notes",
    overwrite: false,
  };

  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--input") args.input = argv[++i];
    else if (a === "--out-dir") args.outDir = argv[++i];
    else if (a === "--overwrite") args.overwrite = true;
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

function mdEscape(s) {
  return (s || "").replace(/\r?\n/g, " ").trim();
}

function noteTemplate(item, topics) {
  const absUrl = item.absUrl || `https://arxiv.org/abs/${item.arxivId}`;
  const pdfUrl = item.pdfUrl || `https://arxiv.org/pdf/${item.arxivId}.pdf`;
  const title = item.title || "(missing title)";

  const cacheTxt = `docs/research/_cache/arxiv/${item.arxivId}.txt`;

  return [
    "---",
    `arxiv_id: ${mdEscape(item.arxivId)}`,
    `title: ${JSON.stringify(mdEscape(title))}`,
    `abs_url: ${mdEscape(absUrl)}`,
    `pdf_url: ${mdEscape(pdfUrl)}`,
    item.primaryCategory ? `primary_category: ${mdEscape(item.primaryCategory)}` : null,
    item.publishedAt ? `published_at: ${mdEscape(item.publishedAt)}` : null,
    item.updatedAt ? `updated_at: ${mdEscape(item.updatedAt)}` : null,
    topics.length ? `topics: [${topics.map((t) => JSON.stringify(t)).join(", ")}]` : null,
    "status: stub",
    "---",
    "",
    `# ${item.arxivId} — ${title}`,
    "",
    "## Abstract",
    "",
    item.abstract ? item.abstract.trim() : "(missing abstract)",
    "",
    "## Key primitives / claims (fill)",
    "",
    "- ",
    "",
    "## Harness implications for PlotLot (fill)",
    "",
    "- ",
    "",
    "## Evaluation ideas (fill)",
    "",
    "- ",
    "",
    "## Relevant quotes (optional)",
    "",
    "> ",
    "",
    "## Local cache",
    "",
    `- Extracted text: \`${cacheTxt}\` (gitignored; regenerate via download script)`,

    "",
  ]
    .filter((x) => x !== null)
    .join("\n");
}

const args = parseArgs(process.argv);
const payload = JSON.parse(fs.readFileSync(args.input, "utf-8"));
const items = (payload.items || []).filter((x) => x.status === "ok");

fs.mkdirSync(args.outDir, { recursive: true });

let written = 0;
let skipped = 0;
for (const item of items) {
  const topics = assignTopics(item.title, item.abstract);
  const fileName = `${item.arxivId}.md`;
  const outPath = path.join(args.outDir, fileName);

  if (!args.overwrite && fs.existsSync(outPath)) {
    skipped++;
    continue;
  }

  fs.writeFileSync(outPath, noteTemplate(item, topics), "utf-8");
  written++;
}

console.log(JSON.stringify({ count: items.length, written, skipped, outDir: args.outDir }, null, 2));
