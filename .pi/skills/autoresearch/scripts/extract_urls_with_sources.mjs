#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

function parseArgs(argv) {
  const args = {
    root: null,
    outputJson: "docs/research/obsidian-urls.json",
    outputTxt: "docs/research/obsidian-urls.txt",
    exts: [".md", ".txt", ".json"],
    maxFiles: 5000,
  };

  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--root") args.root = argv[++i];
    else if (a === "--output-json") args.outputJson = argv[++i];
    else if (a === "--output-txt") args.outputTxt = argv[++i];
    else if (a === "--exts") args.exts = (argv[++i] || "").split(",").map((s) => s.trim());
    else if (a === "--max-files") args.maxFiles = Number(argv[++i] || args.maxFiles);
  }

  if (!args.root) {
    console.error(
      "Usage: extract_urls_with_sources.mjs --root <dir> [--output-json <out.json>] [--output-txt <out.txt>]"
    );
    process.exit(2);
  }

  return args;
}

function walkFiles(root, exts, maxFiles) {
  const out = [];
  const stack = [root];

  while (stack.length && out.length < maxFiles) {
    const dir = stack.pop();
    if (!dir) continue;

    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      continue;
    }

    for (const e of entries) {
      if (e.isDirectory()) {
        if (e.name === "node_modules" || e.name === ".git" || e.name === ".obsidian") continue;
        stack.push(path.join(dir, e.name));
      } else if (e.isFile()) {
        const p = path.join(dir, e.name);
        const ext = path.extname(e.name);
        if (exts.includes(ext)) out.push(p);
      }
    }
  }

  return out;
}

function extractUrls(text) {
  const urlRe = /https?:\/\/[^\s)\]<>\"']+/g;
  const matches = text.match(urlRe) || [];
  return matches.map((u) => u.replace(/[,.;:]+$/g, ""));
}

const args = parseArgs(process.argv);
const files = walkFiles(args.root, args.exts, args.maxFiles);

/** @type {Map<string, Set<string>>} */
const urlToSources = new Map();

for (const f of files) {
  let raw;
  try {
    raw = fs.readFileSync(f, "utf-8");
  } catch {
    continue;
  }
  for (const u of extractUrls(raw)) {
    if (!urlToSources.has(u)) urlToSources.set(u, new Set());
    urlToSources.get(u).add(f);
  }
}

const items = Array.from(urlToSources.entries())
  .map(([url, sources]) => ({ url, sources: Array.from(sources).sort() }))
  .sort((a, b) => (a.url < b.url ? -1 : a.url > b.url ? 1 : 0));

fs.mkdirSync(path.dirname(args.outputJson), { recursive: true });
fs.writeFileSync(
  args.outputJson,
  JSON.stringify({ extractedAt: new Date().toISOString(), fileCount: files.length, urlCount: items.length, items }, null, 2) +
    "\n",
  "utf-8"
);

fs.writeFileSync(
  args.outputTxt,
  items.map((i) => i.url).join("\n") + (items.length ? "\n" : ""),
  "utf-8"
);

console.log(
  JSON.stringify(
    {
      fileCount: files.length,
      urlCount: items.length,
      outputJson: args.outputJson,
      outputTxt: args.outputTxt,
    },
    null,
    2
  )
);
