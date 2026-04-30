#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

function parseArgs(argv) {
  const args = {
    input: "docs/research/obsidian-urls.json",
    outputJson: "docs/research/github-repos.json",
    outputTxt: "docs/research/github-repos.txt",
  };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--input") args.input = argv[++i];
    else if (a === "--output-json") args.outputJson = argv[++i];
    else if (a === "--output-txt") args.outputTxt = argv[++i];
  }
  return args;
}

function hostOf(url) {
  try {
    return new URL(url).host.toLowerCase();
  } catch {
    return null;
  }
}

function repoFromUrl(url) {
  let u;
  try {
    u = new URL(url);
  } catch {
    return null;
  }
  if (u.host.toLowerCase() !== "github.com") return null;
  const parts = u.pathname.split("/").filter(Boolean);
  if (parts.length < 2) return null;

  const owner = parts[0];
  const repo = parts[1].replace(/\.git$/i, "");

  const skipOwners = new Set([
    "features",
    "solutions",
    "security",
    "marketplace",
    "why-github",
    "team",
    "enterprise",
    "login",
    "s",
  ]);
  if (skipOwners.has(owner)) return null;

  // Basic validation: avoid capturing GitHub navigation junk
  if (!/^[A-Za-z0-9_.-]+$/.test(owner)) return null;
  if (!/^[A-Za-z0-9_.-]+$/.test(repo)) return null;

  return `${owner}/${repo}`;
}

const args = parseArgs(process.argv);
const payload = JSON.parse(fs.readFileSync(args.input, "utf-8"));
const items = payload.items || [];

/** @type {Map<string, Set<string>>} */
const repoToUrls = new Map();
for (const it of items) {
  if (hostOf(it.url) !== "github.com") continue;
  const repo = repoFromUrl(it.url);
  if (!repo) continue;
  if (!repoToUrls.has(repo)) repoToUrls.set(repo, new Set());
  repoToUrls.get(repo).add(it.url);
}

const repos = Array.from(repoToUrls.entries())
  .map(([repo, urls]) => ({ repo, url: `https://github.com/${repo}`, urls: Array.from(urls).sort() }))
  .sort((a, b) => a.repo.localeCompare(b.repo));

fs.mkdirSync(path.dirname(args.outputJson), { recursive: true });
fs.writeFileSync(
  args.outputJson,
  JSON.stringify({ extractedAt: new Date().toISOString(), count: repos.length, repos }, null, 2) + "\n",
  "utf-8"
);

fs.writeFileSync(args.outputTxt, repos.map((r) => r.repo).join("\n") + (repos.length ? "\n" : ""), "utf-8");

console.log(JSON.stringify({ count: repos.length, outputJson: args.outputJson, outputTxt: args.outputTxt }, null, 2));
