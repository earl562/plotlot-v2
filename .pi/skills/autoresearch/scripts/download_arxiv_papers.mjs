#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { pipeline } from "node:stream/promises";
import { Readable } from "node:stream";

function parseArgs(argv) {
  const args = {
    input: null,
    outDir: "docs/research/_cache/arxiv",
    concurrency: 2,
    force: false,
    max: null,
    sleepMs: 250,
  };

  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--input") args.input = argv[++i];
    else if (a === "--out-dir") args.outDir = argv[++i];
    else if (a === "--concurrency") args.concurrency = Number(argv[++i] || 2);
    else if (a === "--force") args.force = true;
    else if (a === "--max") args.max = Number(argv[++i]);
    else if (a === "--sleep-ms") args.sleepMs = Number(argv[++i] || 0);
  }

  if (!args.input) {
    console.error(
      "Usage: download_arxiv_papers.mjs --input <arxiv-urls.txt> [--out-dir <dir>] [--concurrency N] [--force] [--max N]"
    );
    process.exit(2);
  }
  if (!Number.isFinite(args.concurrency) || args.concurrency < 1) args.concurrency = 1;
  return args;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function safeFileName(arxivId) {
  return arxivId.replaceAll("/", "_");
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

function pdfUrlForId(arxivId) {
  // arXiv accepts both new-style and old-style ids here.
  return `https://arxiv.org/pdf/${arxivId}.pdf`;
}

async function downloadToFile(url, destPath) {
  const res = await fetch(url, {
    headers: {
      "User-Agent": "plotlot-autoresearch/0.1",
      Accept: "application/pdf",
    },
  });
  if (!res.ok) {
    throw new Error(`HTTP ${res.status} ${res.statusText}`);
  }
  if (!res.body) {
    throw new Error("No response body");
  }

  await pipeline(Readable.fromWeb(res.body), fs.createWriteStream(destPath));
}

function runPdfToText(pdfPath, txtPath) {
  const r = spawnSync("pdftotext", ["-layout", pdfPath, txtPath], {
    encoding: "utf-8",
  });
  if (r.status !== 0) {
    const msg = (r.stderr || r.stdout || "").toString();
    throw new Error(`pdftotext failed: ${msg}`);
  }
}

async function worker(queue, state) {
  while (true) {
    const item = queue.pop();
    if (!item) return;

    const { arxivId, sourceUrl } = item;
    const base = safeFileName(arxivId);

    const pdfPath = path.join(state.outDir, `${base}.pdf`);
    const txtPath = path.join(state.outDir, `${base}.txt`);

    const result = {
      arxivId,
      sourceUrl,
      pdfUrl: pdfUrlForId(arxivId),
      pdfPath,
      txtPath,
      status: "ok",
      error: null,
    };

    try {
      if (state.force || !fs.existsSync(pdfPath)) {
        await downloadToFile(result.pdfUrl, pdfPath);
        if (state.sleepMs) await sleep(state.sleepMs);
      }

      if (state.force || !fs.existsSync(txtPath)) {
        runPdfToText(pdfPath, txtPath);
      }

      state.done.push(result);
      process.stderr.write(`ok  ${arxivId}\n`);
    } catch (err) {
      result.status = "error";
      result.error = err instanceof Error ? err.message : String(err);
      state.done.push(result);
      process.stderr.write(`ERR ${arxivId}: ${result.error}\n`);
    }
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

fs.mkdirSync(args.outDir, { recursive: true });

const queue = items.slice().reverse();
const state = {
  outDir: args.outDir,
  force: args.force,
  sleepMs: args.sleepMs,
  done: [],
};

const workers = [];
for (let i = 0; i < args.concurrency; i++) {
  workers.push(worker(queue, state));
}

await Promise.all(workers);

const indexPath = path.join(args.outDir, "index.json");
fs.writeFileSync(indexPath, JSON.stringify({ count: state.done.length, items: state.done }, null, 2));

console.log(JSON.stringify({ uniqueIds: items.length, indexPath }, null, 2));
