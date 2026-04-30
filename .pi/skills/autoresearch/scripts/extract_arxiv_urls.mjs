#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

function parseArgs(argv) {
  const args = { input: null, output: null };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--input") args.input = argv[++i];
    else if (a === "--output") args.output = argv[++i];
  }
  if (!args.input || !args.output) {
    console.error(
      "Usage: extract_arxiv_urls.mjs --input <file.md> --output <out.txt>"
    );
    process.exit(2);
  }
  return args;
}

function extractUrls(text) {
  const urlRe = /https?:\/\/[^\s)\]"']+/g;
  const matches = text.match(urlRe) || [];

  const urls = matches
    .map((u) => u.replace(/[,.;]+$/g, ""))
    .filter((u) => u.includes("arxiv.org"));

  // Normalize arXiv links a bit (strip trailing fragment)
  const norm = urls.map((u) => {
    try {
      const parsed = new URL(u);
      parsed.hash = "";
      // keep query because some versions include v1
      return parsed.toString();
    } catch {
      return u;
    }
  });

  return Array.from(new Set(norm)).sort();
}

const { input, output } = parseArgs(process.argv);
const raw = fs.readFileSync(input, "utf-8");
const urls = extractUrls(raw);

fs.mkdirSync(path.dirname(output), { recursive: true });
fs.writeFileSync(output, urls.join("\n") + (urls.length ? "\n" : ""), "utf-8");

console.log(JSON.stringify({ count: urls.length, output }, null, 2));
