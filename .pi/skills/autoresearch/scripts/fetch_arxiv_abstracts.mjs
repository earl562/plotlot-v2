#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

function parseArgs(argv) {
  const args = {
    input: null,
    output: "docs/research/arxiv-abstracts.json",
    concurrency: 4,
    sleepMs: 150,
    max: null,
  };

  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--input") args.input = argv[++i];
    else if (a === "--output") args.output = argv[++i];
    else if (a === "--concurrency") args.concurrency = Number(argv[++i] || 4);
    else if (a === "--sleep-ms") args.sleepMs = Number(argv[++i] || 0);
    else if (a === "--max") args.max = Number(argv[++i]);
  }

  if (!args.input) {
    console.error(
      "Usage: fetch_arxiv_abstracts.mjs --input <arxiv-urls.txt> [--output <out.json>] [--concurrency N] [--max N]"
    );
    process.exit(2);
  }
  if (!Number.isFinite(args.concurrency) || args.concurrency < 1) args.concurrency = 1;
  return args;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function parseArxivId(url) {
  let u;
  try {
    u = new URL(url);
  } catch {
    return null;
  }
  const parts = u.pathname.split("/").filter(Boolean);
  const idx = parts.findIndex((p) => p === "abs" || p === "pdf" || p === "html");
  if (idx === -1) return null;
  const idPath = parts.slice(idx + 1).join("/");
  if (!idPath) return null;
  return idPath.replace(/\.pdf$/i, "");
}

function absUrlForId(arxivId) {
  return `https://arxiv.org/abs/${arxivId}`;
}

function parseJinaAbs(markdown) {
  // Jina output starts with:
  // Title: ...
  // URL Source: ...
  // Published Time: ...
  // ...
  // and contains a line starting with "> Abstract:".

  const lines = markdown.split(/\r?\n/);
  const titleLine = lines.find((l) => l.startsWith("Title:"));
  const publishedLine = lines.find((l) => l.startsWith("Published Time:"));

  const title = titleLine ? titleLine.replace(/^Title:\s*/, "").trim() : null;
  const publishedTime = publishedLine
    ? publishedLine.replace(/^Published Time:\s*/, "").trim()
    : null;

  let abstract = null;
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    if (l && l.startsWith("> Abstract:")) {
      abstract = l.replace(/^> Abstract:/, "").trim();
      // Some pages may wrap abstract across multiple blockquote lines.
      for (let j = i + 1; j < lines.length; j++) {
        const nxt = lines[j];
        if (!nxt.startsWith(">")) break;
        const chunk = nxt.replace(/^>\s?/, "").trim();
        if (chunk) abstract += " " + chunk;
      }
      break;
    }
  }

  return { title, publishedTime, abstract };
}

async function fetchAbs(arxivId) {
  const absUrl = absUrlForId(arxivId);
  const jinaUrl = `https://r.jina.ai/${absUrl}`;
  const res = await fetch(jinaUrl, {
    headers: {
      "User-Agent": "plotlot-autoresearch/0.1",
      Accept: "text/plain",
    },
  });
  if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText}`);
  const text = await res.text();
  const parsed = parseJinaAbs(text);
  return {
    arxivId,
    absUrl,
    title: parsed.title,
    abstract: parsed.abstract,
    publishedTime: parsed.publishedTime,
  };
}

async function worker(queue, out, sleepMs) {
  while (true) {
    const item = queue.pop();
    if (!item) return;
    const { arxivId, sourceUrl } = item;

    try {
      const meta = await fetchAbs(arxivId);
      out.push({ ...meta, sourceUrl, status: "ok" });
      process.stderr.write(`ok  ${arxivId}\n`);
    } catch (err) {
      out.push({
        arxivId,
        absUrl: absUrlForId(arxivId),
        sourceUrl,
        title: null,
        abstract: null,
        publishedTime: null,
        status: "error",
        error: err instanceof Error ? err.message : String(err),
      });
      process.stderr.write(
        `ERR ${arxivId}: ${err instanceof Error ? err.message : String(err)}\n`
      );
    }

    if (sleepMs) await sleep(sleepMs);
  }
}

const args = parseArgs(process.argv);

const rawUrls = fs
  .readFileSync(args.input, "utf-8")
  .split(/\r?\n/)
  .map((l) => l.trim())
  .filter(Boolean);

/** @type {Map<string, { arxivId: string, sourceUrl: string }>} */
const byId = new Map();
for (const u of rawUrls) {
  const id = parseArxivId(u);
  if (!id) continue;
  if (!byId.has(id)) byId.set(id, { arxivId: id, sourceUrl: u });
}

let items = Array.from(byId.values());
if (Number.isFinite(args.max) && args.max > 0) items = items.slice(0, args.max);

const queue = items.slice().reverse();
const out = [];

const workers = [];
for (let i = 0; i < args.concurrency; i++) {
  workers.push(worker(queue, out, args.sleepMs));
}

await Promise.all(workers);

out.sort((a, b) => (a.arxivId < b.arxivId ? -1 : a.arxivId > b.arxivId ? 1 : 0));

fs.mkdirSync(path.dirname(args.output), { recursive: true });
fs.writeFileSync(
  args.output,
  JSON.stringify(
    {
      retrievedAt: new Date().toISOString(),
      count: out.length,
      items: out,
    },
    null,
    2
  ) + "\n",
  "utf-8"
);

console.log(JSON.stringify({ uniqueIds: items.length, output: args.output }, null, 2));
