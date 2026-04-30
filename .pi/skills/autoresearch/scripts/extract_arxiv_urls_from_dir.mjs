#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

function parseArgs(argv) {
  const args = { root: null, output: null, exts: [".md", ".txt", ".json"] };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--root") args.root = argv[++i];
    else if (a === "--output") args.output = argv[++i];
    else if (a === "--exts") args.exts = (argv[++i] || "").split(",").map((s) => s.trim());
  }

  if (!args.root || !args.output) {
    console.error(
      "Usage: extract_arxiv_urls_from_dir.mjs --root <dir> --output <out.txt> [--exts .md,.txt,.json]"
    );
    process.exit(2);
  }
  return args;
}

function walkFiles(root, exts) {
  /** @type {string[]} */
  const out = [];
  /** @type {string[]} */
  const stack = [root];
  while (stack.length) {
    const dir = stack.pop();
    if (!dir) continue;
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      continue;
    }

    for (const e of entries) {
      // Skip heavy/system dirs
      if (e.isDirectory()) {
        if (
          e.name === "node_modules" ||
          e.name === ".git" ||
          e.name === ".obsidian" ||
          e.name === ".trash" ||
          e.name === ".DS_Store"
        ) {
          continue;
        }
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

function extractArxivUrls(text) {
  const urlRe = /https?:\/\/[^\s)\]<>\"']+/g;
  const matches = text.match(urlRe) || [];
  return matches
    .map((u) => u.replace(/[,.;:]+$/g, ""))
    .filter((u) => u.includes("arxiv.org"));
}

const { root, output, exts } = parseArgs(process.argv);
const files = walkFiles(root, exts);

/** @type {Set<string>} */
const urls = new Set();

for (const f of files) {
  let raw;
  try {
    raw = fs.readFileSync(f, "utf-8");
  } catch {
    continue;
  }
  for (const u of extractArxivUrls(raw)) urls.add(u);
}

const sorted = Array.from(urls).sort();
fs.mkdirSync(path.dirname(output), { recursive: true });
fs.writeFileSync(output, sorted.join("\n") + (sorted.length ? "\n" : ""), "utf-8");

console.log(JSON.stringify({ filesScanned: files.length, urlCount: sorted.length, output }, null, 2));
