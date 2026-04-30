#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

function parseArgs(argv) {
  const args = {
    input: "docs/research/github-repos.json",
    outDir: "docs/research/github-notes",
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

function fileNameForRepo(repo) {
  return repo.replaceAll("/", "__") + ".md";
}

function stub(repoObj) {
  const repo = repoObj.repo;
  const url = repoObj.url;
  const alts = (repoObj.urls || []).slice(0, 10);

  return [
    "---",
    `repo: ${repo}`,
    `url: ${url}`,
    "status: stub",
    "---",
    "",
    `# ${repo}`,
    "",
    "## What it is (fill)",
    "",
    "- ",
    "",
    "## Key patterns / primitives worth copying (fill)",
    "",
    "- ",
    "",
    "## How it maps to PlotLot (fill)",
    "",
    "- ",
    "",
    "## Risks / gotchas (fill)",
    "",
    "- ",
    "",
    "## Source URLs",
    "",
    `- ${url}`,
    ...alts.filter((u) => u !== url).map((u) => `- ${u}`),
    "",
  ].join("\n");
}

const args = parseArgs(process.argv);
const payload = JSON.parse(fs.readFileSync(args.input, "utf-8"));
const repos = payload.repos || [];

fs.mkdirSync(args.outDir, { recursive: true });

let written = 0;
let skipped = 0;
for (const r of repos) {
  const outPath = path.join(args.outDir, fileNameForRepo(r.repo));
  if (!args.overwrite && fs.existsSync(outPath)) {
    skipped++;
    continue;
  }
  fs.writeFileSync(outPath, stub(r), "utf-8");
  written++;
}

console.log(JSON.stringify({ count: repos.length, written, skipped, outDir: args.outDir }, null, 2));
