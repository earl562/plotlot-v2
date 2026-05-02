#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const DEFAULT_PROFILE_PATH = "docs/research/arxiv-search-profiles/harness-agents.json";
const DEFAULT_METADATA_PATH = "docs/research/arxiv-abstracts.json";
const DEFAULT_URLS_PATH = "docs/research/arxiv-urls.txt";
const DEFAULT_NOTES_DIR = "docs/research/arxiv-notes";
const DEFAULT_CACHE_DIR = "docs/research/_cache/arxiv";
const DEFAULT_OUTPUT_JSON = "docs/research/arxiv-harness-search.json";
const DEFAULT_OUTPUT_MD = "docs/research/arxiv-harness-search.md";
const DEFAULT_OUTPUT_URLS = "docs/research/arxiv-discovery-candidates.txt";
const DEFAULT_CATEGORIES = ["cs.AI", "cs.SE", "cs.CL", "cs.LG", "cs.MA", "cs.RO", "cs.CR", "cs.HC"];
const DEFAULT_STOPWORDS = new Set([
  "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "how", "in", "into", "is", "of", "on", "or", "that", "the", "their", "to", "using", "via", "with"
]);

function parseArgs(argv) {
  const args = {
    queries: [],
    profile: DEFAULT_PROFILE_PATH,
    metadata: DEFAULT_METADATA_PATH,
    existingUrls: DEFAULT_URLS_PATH,
    notesDir: DEFAULT_NOTES_DIR,
    cacheDir: DEFAULT_CACHE_DIR,
    outputJson: DEFAULT_OUTPUT_JSON,
    outputMd: DEFAULT_OUTPUT_MD,
    outputUrls: DEFAULT_OUTPUT_URLS,
    vaultReport: null,
    limit: 12,
    remoteMaxPerQuery: 20,
    since: "2024-01-01",
    categories: [...DEFAULT_CATEGORIES],
    localOnly: false,
    remoteOnly: false,
  };

  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--query") args.queries.push(argv[++i]);
    else if (a === "--profile") args.profile = argv[++i];
    else if (a === "--metadata") args.metadata = argv[++i];
    else if (a === "--existing-urls") args.existingUrls = argv[++i];
    else if (a === "--notes-dir") args.notesDir = argv[++i];
    else if (a === "--cache-dir") args.cacheDir = argv[++i];
    else if (a === "--output-json") args.outputJson = argv[++i];
    else if (a === "--output-md") args.outputMd = argv[++i];
    else if (a === "--output-urls") args.outputUrls = argv[++i];
    else if (a === "--vault-report") args.vaultReport = argv[++i];
    else if (a === "--limit") args.limit = Number(argv[++i] || 12);
    else if (a === "--remote-max-per-query") args.remoteMaxPerQuery = Number(argv[++i] || 20);
    else if (a === "--since") args.since = argv[++i];
    else if (a === "--category") args.categories.push(argv[++i]);
    else if (a === "--local-only") args.localOnly = true;
    else if (a === "--remote-only") args.remoteOnly = true;
    else if (a === "-h" || a === "--help") {
      printUsage();
      process.exit(0);
    } else {
      console.error(`Unknown arg: ${a}`);
      printUsage();
      process.exit(2);
    }
  }

  if (args.localOnly && args.remoteOnly) {
    console.error("Choose only one of --local-only or --remote-only.");
    process.exit(2);
  }

  if (!Number.isFinite(args.limit) || args.limit < 1) args.limit = 12;
  if (!Number.isFinite(args.remoteMaxPerQuery) || args.remoteMaxPerQuery < 1) args.remoteMaxPerQuery = 20;
  args.categories = Array.from(new Set(args.categories.filter(Boolean)));
  return args;
}

function printUsage() {
  console.log(`Usage:
  node scripts/search_harness_arxiv.mjs [options]

Options:
  --query <text>              Add a query (repeatable)
  --profile <path>            Query profile JSON (default: ${DEFAULT_PROFILE_PATH})
  --metadata <path>           Existing arXiv metadata JSON
  --existing-urls <path>      Existing arXiv URLs txt
  --notes-dir <dir>           arXiv note directory
  --cache-dir <dir>           Full-text cache directory
  --output-json <path>        Write combined JSON report
  --output-md <path>          Write markdown report
  --output-urls <path>        Write newly discovered arXiv abs URLs
  --vault-report <path>       Also write markdown report into the Obsidian vault
  --limit <n>                 Local results per query / top aggregate count
  --remote-max-per-query <n>  Max remote results fetched per query
  --since <YYYY-MM-DD>        Keep remote discoveries updated on/after this date
  --category <cs.XY>          Add arXiv category filter (repeatable)
  --local-only                Skip remote discovery
  --remote-only               Skip local corpus search
`);
}

function ensureDirFor(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

function safeReadJson(filePath, fallback = null) {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch {
    return fallback;
  }
}

function safeReadText(filePath, fallback = "") {
  try {
    return fs.readFileSync(filePath, "utf8");
  } catch {
    return fallback;
  }
}

function parseProfile(profilePath) {
  const raw = safeReadJson(profilePath, null);
  if (!raw) return { name: "default", queries: [] };
  if (Array.isArray(raw)) return { name: path.basename(profilePath), queries: raw.map(String) };
  const queries = Array.isArray(raw.queries) ? raw.queries.map((q) => (typeof q === "string" ? q : q.query)).filter(Boolean) : [];
  return { name: raw.name || path.basename(profilePath), queries };
}

function parseArxivId(url) {
  try {
    const u = new URL(url);
    const parts = u.pathname.split("/").filter(Boolean);
    const idx = parts.findIndex((p) => p === "abs" || p === "pdf" || p === "html");
    if (idx === -1) return null;
    return parts.slice(idx + 1).join("/").replace(/\.pdf$/i, "") || null;
  } catch {
    return null;
  }
}

function normalizeArxivId(id) {
  return String(id || "").trim();
}

function toAbsUrl(arxivId) {
  return `https://arxiv.org/abs/${arxivId}`;
}

function safeFileName(arxivId) {
  return arxivId.replaceAll("/", "_");
}

function tokenize(text) {
  return String(text || "")
    .toLowerCase()
    .replace(/[^a-z0-9+]+/g, " ")
    .split(/\s+/)
    .map((x) => x.trim())
    .filter((x) => x && x.length > 1 && !DEFAULT_STOPWORDS.has(x));
}

function escapeRegex(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function countMatches(text, term) {
  if (!text || !term) return 0;
  const re = new RegExp(escapeRegex(term), "gi");
  let count = 0;
  while (re.exec(text)) count++;
  return count;
}

function compactWhitespace(s) {
  return String(s || "").replace(/\s+/g, " ").trim();
}

function parseStatusFromNote(notePath) {
  const raw = safeReadText(notePath, "");
  const m = raw.match(/^status:\s*(.+)$/m);
  return m ? m[1].trim() : "unknown";
}

function loadLocalCorpus(metadataPath, notesDir, cacheDir) {
  const metadata = safeReadJson(metadataPath, { items: [] });
  const items = Array.isArray(metadata?.items) ? metadata.items : [];
  const byId = new Map();

  for (const item of items) {
    if (!item || item.status === "error" || !item.arxivId) continue;
    const arxivId = normalizeArxivId(item.arxivId);
    if (byId.has(arxivId)) continue;
    const notePath = path.join(notesDir, `${arxivId}.md`);
    const txtPath = path.join(cacheDir, `${safeFileName(arxivId)}.txt`);
    byId.set(arxivId, {
      arxivId,
      title: item.title || "",
      abstract: item.abstract || "",
      authors: item.authors || [],
      primaryCategory: item.primaryCategory || null,
      categories: item.categories || [],
      publishedAt: item.publishedAt || null,
      updatedAt: item.updatedAt || null,
      absUrl: item.absUrl || toAbsUrl(arxivId),
      noteStatus: parseStatusFromNote(notePath),
      notePath,
      txtPath,
    });
  }

  return Array.from(byId.values());
}

function loadExistingIds(metadataPath, existingUrlsPath) {
  const ids = new Set();
  const meta = safeReadJson(metadataPath, { items: [] });
  for (const item of meta?.items || []) {
    if (item?.arxivId) ids.add(normalizeArxivId(item.arxivId));
  }
  const urlText = safeReadText(existingUrlsPath, "");
  for (const line of urlText.split(/\r?\n/)) {
    const id = parseArxivId(line.trim());
    if (id) ids.add(normalizeArxivId(id));
  }
  return ids;
}

function loadFullText(txtPath) {
  return safeReadText(txtPath, "");
}

function scorePaperAgainstQuery(paper, query) {
  const q = compactWhitespace(query).toLowerCase();
  const terms = Array.from(new Set(tokenize(query)));
  const title = paper.title.toLowerCase();
  const abstract = paper.abstract.toLowerCase();
  const fullText = loadFullText(paper.txtPath).toLowerCase();

  let score = 0;
  if (q && title.includes(q)) score += 80;
  if (q && abstract.includes(q)) score += 30;
  if (q && fullText.includes(q)) score += 12;

  const matchedTerms = [];
  for (const term of terms) {
    const titleCount = countMatches(title, term);
    const abstractCount = countMatches(abstract, term);
    const fullCount = Math.min(countMatches(fullText, term), 40);
    const termScore = titleCount * 14 + abstractCount * 5 + fullCount * 0.4;
    if (termScore > 0) matchedTerms.push(term);
    score += termScore;
  }

  if (paper.noteStatus === "reviewed") score += 2;
  if (paper.primaryCategory && /^cs\./.test(paper.primaryCategory)) score += 1;

  return {
    score,
    matchedTerms: Array.from(new Set(matchedTerms)),
    snippet: compactWhitespace(paper.abstract).slice(0, 280),
  };
}

function searchLocalCorpus(corpus, queries, limit) {
  const byQuery = [];
  const aggregate = new Map();

  for (const query of queries) {
    const scored = corpus
      .map((paper) => ({ paper, ...scorePaperAgainstQuery(paper, query) }))
      .filter((x) => x.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, limit)
      .map((x) => ({
        arxivId: x.paper.arxivId,
        title: x.paper.title,
        primaryCategory: x.paper.primaryCategory,
        noteStatus: x.paper.noteStatus,
        absUrl: x.paper.absUrl,
        score: Number(x.score.toFixed(2)),
        matchedTerms: x.matchedTerms,
        snippet: x.snippet,
      }));

    byQuery.push({ query, hits: scored });

    for (const hit of scored) {
      const key = hit.arxivId;
      const current = aggregate.get(key) || {
        arxivId: hit.arxivId,
        title: hit.title,
        primaryCategory: hit.primaryCategory,
        noteStatus: hit.noteStatus,
        absUrl: hit.absUrl,
        score: 0,
        matchedQueries: [],
        matchedTerms: new Set(),
        snippet: hit.snippet,
      };
      current.score += hit.score;
      current.matchedQueries.push(query);
      for (const term of hit.matchedTerms) current.matchedTerms.add(term);
      aggregate.set(key, current);
    }
  }

  const topAggregate = Array.from(aggregate.values())
    .map((item) => ({
      ...item,
      score: Number(item.score.toFixed(2)),
      matchedQueries: Array.from(new Set(item.matchedQueries)),
      matchedTerms: Array.from(item.matchedTerms),
    }))
    .sort((a, b) => b.score - a.score)
    .slice(0, limit);

  return { byQuery, topAggregate };
}

function decodeXml(s) {
  return String(s || "")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&amp;/g, "&")
    .replace(/&#x([0-9a-fA-F]+);/g, (_m, hex) => String.fromCodePoint(parseInt(hex, 16)))
    .replace(/&#([0-9]+);/g, (_m, num) => String.fromCodePoint(parseInt(num, 10)));
}

function matchTag(block, tag) {
  const re = new RegExp(`<${tag}>([\\s\\S]*?)<\\/${tag}>`, "i");
  const m = block.match(re);
  return m ? compactWhitespace(decodeXml(m[1])) : null;
}

function parseFeed(xml) {
  const entries = xml.split("<entry>").slice(1).map((chunk) => chunk.split("</entry>")[0]);
  return entries.map((entry) => {
    const idUrl = matchTag(entry, "id");
    const title = matchTag(entry, "title");
    const abstract = matchTag(entry, "summary");
    const published = matchTag(entry, "published");
    const updated = matchTag(entry, "updated");
    const primaryCatMatch = entry.match(/<arxiv:primary_category\s+term="([^"]+)"\s*\/>/i);
    const categoryTerms = Array.from(entry.matchAll(/<category\s+term="([^"]+)"/gi)).map((m) => m[1]);
    const authorBlocks = entry.split("<author>").slice(1).map((c) => c.split("</author>")[0]);
    const authors = authorBlocks.map((block) => matchTag(block, "name")).filter(Boolean);
    const pdfMatch = entry.match(/<link\s+href="([^"]+)"\s+rel="related"\s+type="application\/pdf"\s+title="pdf"\s*\/>/i);
    const arxivId = idUrl ? idUrl.replace(/^https?:\/\/arxiv\.org\/abs\//, "") : null;
    return {
      arxivId,
      title,
      abstract,
      authors,
      publishedAt: published,
      updatedAt: updated,
      primaryCategory: primaryCatMatch ? primaryCatMatch[1] : null,
      categories: categoryTerms,
      absUrl: idUrl ? idUrl.replace("http://", "https://") : null,
      pdfUrl: pdfMatch ? pdfMatch[1].replace("http://", "https://") : null,
    };
  });
}

function buildSearchQuery(query, categories) {
  const safeQuery = String(query || "").replace(/"/g, "").trim();
  const phrase = `all:\"${safeQuery}\"`;
  const catExpr = categories.length ? `(${categories.map((c) => `cat:${c}`).join(" OR ")})` : "";
  return catExpr ? `${phrase} AND ${catExpr}` : phrase;
}

async function fetchArxivSearch(query, categories, maxResults) {
  const searchQuery = buildSearchQuery(query, categories);
  const url = `https://export.arxiv.org/api/query?search_query=${encodeURIComponent(searchQuery)}&start=0&max_results=${maxResults}&sortBy=submittedDate&sortOrder=descending`;
  const res = await fetch(url, {
    headers: {
      "User-Agent": "plotlot-arxiv-search/0.1",
      Accept: "application/atom+xml",
    },
  });
  if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText}`);
  return parseFeed(await res.text());
}

function isOnOrAfter(dateText, since) {
  if (!dateText || !since) return true;
  const d = new Date(dateText);
  const s = new Date(since);
  if (Number.isNaN(d.getTime()) || Number.isNaN(s.getTime())) return true;
  return d.getTime() >= s.getTime();
}

function scoreRemoteCandidate(item, query) {
  const title = String(item.title || "").toLowerCase();
  const abstract = String(item.abstract || "").toLowerCase();
  const q = compactWhitespace(query).toLowerCase();
  const terms = Array.from(new Set(tokenize(query)));
  let score = 0;
  if (q && title.includes(q)) score += 70;
  if (q && abstract.includes(q)) score += 24;
  const matchedTerms = [];
  for (const term of terms) {
    const titleCount = countMatches(title, term);
    const abstractCount = countMatches(abstract, term);
    const termScore = titleCount * 12 + abstractCount * 4;
    if (termScore > 0) matchedTerms.push(term);
    score += termScore;
  }
  return { score, matchedTerms };
}

async function discoverRemote(queries, categories, existingIds, maxResults, since, limit) {
  const merged = new Map();
  const byQuery = [];

  for (const query of queries) {
    const entries = await fetchArxivSearch(query, categories, maxResults);
    const kept = [];

    for (const entry of entries) {
      if (!entry.arxivId) continue;
      if (!isOnOrAfter(entry.updatedAt || entry.publishedAt, since)) continue;
      const scoring = scoreRemoteCandidate(entry, query);
      if (scoring.score <= 0) continue;

      const existing = merged.get(entry.arxivId) || {
        ...entry,
        existingInVault: existingIds.has(entry.arxivId),
        score: 0,
        matchedQueries: [],
        matchedTerms: new Set(),
      };
      existing.score += scoring.score;
      existing.matchedQueries.push(query);
      for (const term of scoring.matchedTerms) existing.matchedTerms.add(term);
      merged.set(entry.arxivId, existing);

      kept.push({
        arxivId: entry.arxivId,
        title: entry.title,
        absUrl: entry.absUrl || toAbsUrl(entry.arxivId),
        updatedAt: entry.updatedAt || entry.publishedAt,
        primaryCategory: entry.primaryCategory,
        score: Number(scoring.score.toFixed(2)),
        existingInVault: existingIds.has(entry.arxivId),
      });
    }

    byQuery.push({
      query,
      hits: kept.sort((a, b) => b.score - a.score).slice(0, limit),
    });
  }

  const all = Array.from(merged.values())
    .map((item) => ({
      ...item,
      absUrl: item.absUrl || toAbsUrl(item.arxivId),
      score: Number(item.score.toFixed(2)),
      matchedQueries: Array.from(new Set(item.matchedQueries)),
      matchedTerms: Array.from(item.matchedTerms),
      snippet: compactWhitespace(item.abstract).slice(0, 280),
    }))
    .sort((a, b) => b.score - a.score);

  return {
    byQuery,
    topNew: all.filter((x) => !x.existingInVault).slice(0, limit),
    topExisting: all.filter((x) => x.existingInVault).slice(0, limit),
    allCount: all.length,
  };
}

function renderMarkdown(report) {
  const lines = [];
  lines.push("# Paperclip-style arXiv search report");
  lines.push("");
  lines.push(`Generated: ${report.generatedAt}`);
  lines.push(`Profile: ${report.profileName}`);
  lines.push(`Queries: ${report.queries.length}`);
  lines.push("");
  lines.push("> Note: this is a Paperclip-style workflow for arXiv. The actual Paperclip product currently targets biomedical corpora (bioRxiv/medRxiv/PMC), so this report reproduces the search/discovery pattern against PlotLot's arXiv corpus and the arXiv API.");
  lines.push("");

  if (report.local) {
    lines.push("## Existing arXiv papers already in the vault/repo");
    lines.push("");
    lines.push("### Top aggregate matches");
    lines.push("");
    for (const item of report.local.topAggregate) {
      lines.push(`- [${item.arxivId}](${item.absUrl}) — ${item.title} — score ${item.score} — ${item.noteStatus}`);
      lines.push(`  - matched queries: ${item.matchedQueries.join(", ")}`);
      if (item.matchedTerms.length) lines.push(`  - matched terms: ${item.matchedTerms.join(", ")}`);
      if (item.primaryCategory) lines.push(`  - category: ${item.primaryCategory}`);
    }
    lines.push("");

    for (const block of report.local.byQuery) {
      lines.push(`### Query: ${block.query}`);
      lines.push("");
      for (const item of block.hits) {
        lines.push(`- [${item.arxivId}](${item.absUrl}) — ${item.title} — score ${item.score} — ${item.noteStatus}`);
        if (item.primaryCategory) lines.push(`  - category: ${item.primaryCategory}`);
        if (item.snippet) lines.push(`  - ${item.snippet}`);
      }
      lines.push("");
    }
  }

  if (report.remote) {
    lines.push("## New arXiv discovery candidates");
    lines.push("");
    lines.push(`Remote matches considered: ${report.remote.allCount}`);
    lines.push(`Since: ${report.since}`);
    lines.push("");

    lines.push("### Top new candidates not already in the vault");
    lines.push("");
    for (const item of report.remote.topNew) {
      lines.push(`- [${item.arxivId}](${item.absUrl}) — ${item.title} — score ${item.score}`);
      lines.push(`  - updated: ${item.updatedAt || "unknown"}`);
      if (item.primaryCategory) lines.push(`  - category: ${item.primaryCategory}`);
      if (item.matchedQueries?.length) lines.push(`  - matched queries: ${item.matchedQueries.join(", ")}`);
      if (item.snippet) lines.push(`  - ${item.snippet}`);
    }
    lines.push("");

    lines.push("### Strong remote hits already in the vault");
    lines.push("");
    for (const item of report.remote.topExisting) {
      lines.push(`- [${item.arxivId}](${item.absUrl}) — ${item.title} — score ${item.score}`);
      if (item.primaryCategory) lines.push(`  - category: ${item.primaryCategory}`);
      if (item.matchedQueries?.length) lines.push(`  - matched queries: ${item.matchedQueries.join(", ")}`);
    }
    lines.push("");
  }

  return lines.join("\n") + "\n";
}

const args = parseArgs(process.argv);
const profile = parseProfile(args.profile);
const queries = Array.from(new Set([...profile.queries, ...args.queries].map(compactWhitespace).filter(Boolean)));
if (!queries.length) {
  console.error("No queries found. Provide --query or a profile JSON with queries[].");
  process.exit(2);
}

const corpus = args.remoteOnly ? [] : loadLocalCorpus(args.metadata, args.notesDir, args.cacheDir);
const existingIds = loadExistingIds(args.metadata, args.existingUrls);

const report = {
  generatedAt: new Date().toISOString(),
  profileName: profile.name,
  queries,
  since: args.since,
  categories: args.categories,
  local: null,
  remote: null,
};

if (!args.remoteOnly) {
  report.local = searchLocalCorpus(corpus, queries, args.limit);
}

if (!args.localOnly) {
  report.remote = await discoverRemote(
    queries,
    args.categories,
    existingIds,
    args.remoteMaxPerQuery,
    args.since,
    args.limit
  );
}

ensureDirFor(args.outputJson);
ensureDirFor(args.outputMd);
ensureDirFor(args.outputUrls);
fs.writeFileSync(args.outputJson, JSON.stringify(report, null, 2) + "\n", "utf8");
const markdown = renderMarkdown(report);
fs.writeFileSync(args.outputMd, markdown, "utf8");
if (args.vaultReport) {
  ensureDirFor(args.vaultReport);
  fs.writeFileSync(args.vaultReport, markdown, "utf8");
}

const discoveredUrls = (report.remote?.topNew || []).map((item) => item.absUrl).filter(Boolean);
fs.writeFileSync(args.outputUrls, discoveredUrls.join("\n") + (discoveredUrls.length ? "\n" : ""), "utf8");

console.log(JSON.stringify({
  outputJson: args.outputJson,
  outputMd: args.outputMd,
  outputUrls: args.outputUrls,
  vaultReport: args.vaultReport,
  queries: queries.length,
  localTop: report.local?.topAggregate?.length || 0,
  remoteNewTop: report.remote?.topNew?.length || 0,
}, null, 2));
