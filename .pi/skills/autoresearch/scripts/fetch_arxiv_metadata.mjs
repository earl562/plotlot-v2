#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

function parseArgs(argv) {
  const args = {
    input: null,
    output: "docs/research/arxiv-abstracts.json",
    batchSize: 20,
    sleepMs: 350,
    max: null,
  };

  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--input") args.input = argv[++i];
    else if (a === "--output") args.output = argv[++i];
    else if (a === "--batch-size") args.batchSize = Number(argv[++i] || 20);
    else if (a === "--sleep-ms") args.sleepMs = Number(argv[++i] || 0);
    else if (a === "--max") args.max = Number(argv[++i]);
  }

  if (!args.input) {
    console.error(
      "Usage: fetch_arxiv_metadata.mjs --input <arxiv-urls.txt> [--output <out.json>] [--batch-size N] [--max N]"
    );
    process.exit(2);
  }

  if (!Number.isFinite(args.batchSize) || args.batchSize < 1) args.batchSize = 10;
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

function decodeXml(s) {
  return s
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&amp;/g, "&")
    .replace(/&#x([0-9a-fA-F]+);/g, (_m, hex) =>
      String.fromCodePoint(parseInt(hex, 16))
    )
    .replace(/&#([0-9]+);/g, (_m, num) =>
      String.fromCodePoint(parseInt(num, 10))
    );
}

function matchTag(block, tag) {
  const re = new RegExp(`<${tag}>([\\s\\S]*?)<\\/${tag}>`, "i");
  const m = block.match(re);
  return m ? decodeXml(m[1]).trim().replace(/\s+/g, " ") : null;
}

function matchAll(block, tag) {
  const re = new RegExp(`<${tag}>([\\s\\S]*?)<\\/${tag}>`, "gi");
  const out = [];
  let m;
  while ((m = re.exec(block)) !== null) {
    out.push(decodeXml(m[1]).trim().replace(/\s+/g, " "));
  }
  return out;
}

function parseFeed(xml) {
  const entries = xml.split("<entry>").slice(1).map((chunk) => chunk.split("</entry>")[0]);

  return entries.map((entry) => {
    const idUrl = matchTag(entry, "id");
    const title = matchTag(entry, "title");
    const summary = matchTag(entry, "summary");
    const published = matchTag(entry, "published");
    const updated = matchTag(entry, "updated");

    const authors = [];
    const authorBlocks = entry.split("<author>").slice(1).map((c) => c.split("</author>")[0]);
    for (const ab of authorBlocks) {
      const name = matchTag(ab, "name");
      if (name) authors.push(name);
    }

    const primaryCatMatch = entry.match(/<arxiv:primary_category\s+term="([^"]+)"\s*\/>/i);
    const primaryCategory = primaryCatMatch ? primaryCatMatch[1] : null;

    const categoryTerms = [];
    const catMatches = entry.matchAll(/<category\s+term="([^"]+)"/gi);
    for (const cm of catMatches) categoryTerms.push(cm[1]);

    // prefer https pdf link
    const pdfLinkMatch = entry.match(
      /<link\s+href="([^"]+)"\s+rel="related"\s+type="application\/pdf"\s+title="pdf"\s*\/>/i
    );
    const pdfUrl = pdfLinkMatch ? pdfLinkMatch[1].replace("http://", "https://") : null;

    const comment = matchTag(entry, "arxiv:comment");

    return {
      idUrl,
      arxivId: idUrl ? idUrl.replace(/^https?:\/\/arxiv\.org\/abs\//, "") : null,
      title,
      summary,
      published,
      updated,
      authors,
      primaryCategory,
      categories: categoryTerms,
      pdfUrl,
      comment,
    };
  });
}

async function fetchBatch(ids) {
  // Important: arXiv API defaults to max_results=10 even with id_list.
  // Set max_results to the batch size to avoid silently dropping entries.
  const url = `https://export.arxiv.org/api/query?id_list=${encodeURIComponent(
    ids.join(",")
  )}&start=0&max_results=${ids.length}`;
  const res = await fetch(url, {
    headers: {
      "User-Agent": "plotlot-autoresearch/0.1",
      Accept: "application/atom+xml",
    },
  });
  if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText}`);
  const xml = await res.text();
  return parseFeed(xml);
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

const ids = items.map((x) => x.arxivId);

/** @type {Record<string, any>} */
const sourceUrlById = {};
for (const it of items) sourceUrlById[it.arxivId] = it.sourceUrl;

const out = [];
for (let i = 0; i < ids.length; i += args.batchSize) {
  const batch = ids.slice(i, i + args.batchSize);
  process.stderr.write(`batch ${Math.floor(i / args.batchSize) + 1} (${batch.length} ids)\n`);

  try {
    const entries = await fetchBatch(batch);
    for (const e of entries) {
      const arxivId = e.arxivId;
      if (!arxivId) continue;
      out.push({
        arxivId,
        sourceUrl: sourceUrlById[arxivId] ?? null,
        title: e.title,
        abstract: e.summary,
        authors: e.authors,
        primaryCategory: e.primaryCategory,
        categories: e.categories,
        publishedAt: e.published,
        updatedAt: e.updated,
        absUrl: e.idUrl ? e.idUrl.replace("http://", "https://") : null,
        pdfUrl: e.pdfUrl,
        comment: e.comment,
        status: "ok",
      });
    }
  } catch (err) {
    for (const arxivId of batch) {
      out.push({
        arxivId,
        sourceUrl: sourceUrlById[arxivId] ?? null,
        status: "error",
        error: err instanceof Error ? err.message : String(err),
      });
    }
  }

  if (args.sleepMs) await sleep(args.sleepMs);
}

out.sort((a, b) => (a.arxivId < b.arxivId ? -1 : a.arxivId > b.arxivId ? 1 : 0));

fs.mkdirSync(path.dirname(args.output), { recursive: true });
fs.writeFileSync(
  args.output,
  JSON.stringify({ retrievedAt: new Date().toISOString(), count: out.length, items: out }, null, 2) + "\n",
  "utf-8"
);

console.log(JSON.stringify({ uniqueIds: ids.length, output: args.output }, null, 2));
