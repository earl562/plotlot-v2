#!/usr/bin/env node

/**
 * Export harness-engineering knowledge graph artifacts into the Obsidian vault.
 *
 * Inputs (repo-owned):
 * - docs/research/arxiv-notes/*.md (reviewed notes)
 * - docs/research/harness-primitives.md (consolidated primitives)
 * - docs/research/obsidian-vault-path.txt (absolute path to Obsidian vault)
 *
 * Outputs (vault, NOT git-tracked):
 * - <vault>/Harnesses/Harness Engineering KG/
 *   - 00 - Overview.md
 *   - Nodes/<slug>.md
 *   - Sources/arXiv/<arxivId>.md (backlinks to repo notes)
 *
 * Design:
 * - Obsidian-native: wikilinks, minimal frontmatter, human editable.
 * - “KG” is a set of interlinked notes (nodes) + an overview index.
 */

import fs from "node:fs";
import path from "node:path";

const REPO_ROOT = process.cwd();

function readText(p) {
  return fs.readFileSync(p, "utf8");
}

function exists(p) {
  try {
    fs.accessSync(p);
    return true;
  } catch {
    return false;
  }
}

function mkdirp(p) {
  fs.mkdirSync(p, { recursive: true });
}

function slugify(s) {
  return (s || "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80);
}

function parseFrontmatter(md) {
  if (!md.startsWith("---")) return { fm: {}, body: md };
  const end = md.indexOf("\n---", 3);
  if (end === -1) return { fm: {}, body: md };
  const block = md.slice(3, end).trim();
  const body = md.slice(end + "\n---".length);
  const fm = {};
  for (const line of block.split(/\r?\n/)) {
    const m = line.match(/^([a-zA-Z0-9_\-]+):\s*(.*)$/);
    if (!m) continue;
    fm[m[1]] = m[2].trim();
  }
  return { fm, body };
}

function listReviewedArxivNotes() {
  const notesDir = path.join(REPO_ROOT, "docs/research/arxiv-notes");
  const files = fs.readdirSync(notesDir).filter((f) => f.endsWith(".md"));
  const out = [];
  for (const f of files) {
    const full = path.join(notesDir, f);
    const md = readText(full);
    const { fm } = parseFrontmatter(md);
    const status = (fm.status || "").replace(/"/g, "");
    if (status !== "reviewed") continue;
    const arxivId = (fm.arxiv_id || path.basename(f, ".md")).replace(/"/g, "");
    const title = (fm.title || "").replace(/^"|"$/g, "");
    const absUrl = (fm.abs_url || "").replace(/"/g, "");
    const pdfUrl = (fm.pdf_url || "").replace(/"/g, "");
    out.push({ arxivId, title, absUrl, pdfUrl, repoPath: full, file: f });
  }
  out.sort((a, b) => a.arxivId.localeCompare(b.arxivId));
  return out;
}

function extractBullets(md, heading) {
  const re = new RegExp(`^##\\s+${heading}\\s*$`, "m");
  const m = md.match(re);
  if (!m) return [];
  const start = m.index + m[0].length;
  const rest = md.slice(start);
  const next = rest.search(/^##\s+/m);
  const block = (next === -1 ? rest : rest.slice(0, next)).trim();
  const bullets = block
    .split(/\r?\n/)
    .map((l) => l.trim())
    .filter((l) => l.startsWith("- "))
    .map((l) => l.slice(2).trim());
  return bullets;
}

function writeNode({ outDir, name, type, bullets, sources }) {
  const fileName = `${name}.md`;
  const p = path.join(outDir, fileName);
  const fm = [
    "---",
    `kg_node: true`,
    `kg_type: ${JSON.stringify(type)}`,
    sources?.length ? `sources: [${sources.map((s) => JSON.stringify(s)).join(", ")}]` : null,
    "---",
    "",
  ]
    .filter(Boolean)
    .join("\n");

  const body = [
    `# ${name}`,
    "",
    "## What this is",
    "",
    `- Type: ${type}`,
    "",
    "## Notes",
    "",
    ...bullets.map((b) => `- ${b}`),
    "",
    "## Links",
    "",
    "- (add wikilinks like [[Governance Middleware]] / [[Evidence Ledger]] as this grows)",
    "",
  ].join("\n");

  fs.writeFileSync(p, `${fm}\n${body}`, "utf8");
}

function main() {
  const vaultPathFile = path.join(REPO_ROOT, "docs/research/obsidian-vault-path.txt");
  if (!exists(vaultPathFile)) {
    console.error(`ERR: missing ${vaultPathFile}`);
    process.exit(2);
  }

  const vault = readText(vaultPathFile).trim();
  if (!vault.startsWith("/")) {
    console.error(`ERR: vault path must be absolute, got: ${vault}`);
    process.exit(2);
  }
  if (!exists(vault)) {
    console.error(`ERR: vault path does not exist: ${vault}`);
    process.exit(2);
  }

  const kgRoot = path.join(vault, "Harnesses", "Harness Engineering KG");
  const nodesDir = path.join(kgRoot, "Nodes");
  const sourcesDir = path.join(kgRoot, "Sources", "arXiv");
  mkdirp(nodesDir);
  mkdirp(sourcesDir);

  // Node seed list: start from repo’s consolidated primitives as stable entry points.
  const primitivesPath = path.join(REPO_ROOT, "docs/research/harness-primitives.md");
  const primitivesMd = exists(primitivesPath) ? readText(primitivesPath) : "";

  const reviewed = listReviewedArxivNotes();

  // Write per-paper source notes (thin wrappers for backlinks and local annotations).
  for (const p of reviewed) {
    const relRepo = path.relative(REPO_ROOT, p.repoPath);
    const out = [
      "---",
      `source_type: "arxiv"`,
      `arxiv_id: ${JSON.stringify(p.arxivId)}`,
      `title: ${JSON.stringify(p.title)}`,
      p.absUrl ? `abs_url: ${JSON.stringify(p.absUrl)}` : null,
      p.pdfUrl ? `pdf_url: ${JSON.stringify(p.pdfUrl)}` : null,
      "---",
      "",
      `# ${p.arxivId} — ${p.title}`,
      "",
      "## Repo note",
      "",
      `- ${relRepo}`,
      "",
      "## Extracted primitives (copy/paste or link into Nodes)",
      "",
      "- ",
      "",
    ]
      .filter(Boolean)
      .join("\n");

    fs.writeFileSync(path.join(sourcesDir, `${p.arxivId}.md`), out, "utf8");
  }

  // Seed core harness nodes (first principles).
  const coreNodes = [
    {
      name: "Harness Runtime",
      type: "system",
      bullets: [
        "Orchestrates skills/tools/memory/evidence/approvals; the harness is the product.",
        "Owns selection of context + deterministic validation gates.",
      ],
      sources: ["docs/research/harness-primitives.md"],
    },
    {
      name: "Evidence Ledger",
      type: "primitive",
      bullets: [
        "Every claim must link to a source-backed evidence item.",
        "Tool runs should emit evidence records with URLs/section ids/timestamps.",
      ],
      sources: [],
    },
    {
      name: "Governance Middleware",
      type: "primitive",
      bullets: [
        "Policy layer for tool execution: read vs write, internal vs external, expensive vs cheap.",
        "Requires approvals for high-risk actions and captures audit logs.",
      ],
      sources: [],
    },
    {
      name: "Context Broker",
      type: "primitive",
      bullets: [
        "Select → Write → Compress → Isolate operations over memory/evidence.",
        "Keep context small, specific, and stage-bounded.",
      ],
      sources: [],
    },
  ];

  for (const n of coreNodes) {
    writeNode({
      outDir: nodesDir,
      name: n.name,
      type: n.type,
      bullets: n.bullets,
      sources: n.sources,
    });
  }

  // Overview
  const overview = [
    "---",
    "kg_root: true",
    `generated_from_repo: ${JSON.stringify(path.relative(REPO_ROOT, primitivesPath))}`,
    `generated_at: ${JSON.stringify(new Date().toISOString())}`,
    "---",
    "",
    "# Harness Engineering KG — Overview",
    "",
    "This folder is a living knowledge graph (KG) in Obsidian for harness engineering, built from your arXiv review workflow and refined into first principles for PlotLot.",
    "",
    "## How to use",
    "",
    "- Start with [[Harness Runtime]] and branch into [[Context Broker]], [[Governance Middleware]], [[Evidence Ledger]].",
    "- Each arXiv source has a note under `Sources/arXiv/` you can annotate and link into Nodes.",
    "- Keep detailed learning in Nodes; keep sources as raw citations/backlinks.",
    "",
    "## PlotLot mapping (first principles)",
    "",
    "- Harness coordinates: Workspace → Project → Site → Analysis → Evidence → Report → Action.",
    "- Deterministic code handles facts/validation/scoring; LLM handles synthesis/strategy.",
    "- Governance + approvals gate any external side effects.",
    "",
    "## Index",
    "",
    "### Core nodes",
    "- [[Harness Runtime]]",
    "- [[Context Broker]]",
    "- [[Governance Middleware]]",
    "- [[Evidence Ledger]]",
    "",
    `### Sources (reviewed arXiv notes: ${reviewed.length})`,
    "- Browse: `Sources/arXiv/`",
    "",
  ].join("\n");

  fs.writeFileSync(path.join(kgRoot, "00 - Overview.md"), overview, "utf8");

  console.log(
    JSON.stringify(
      {
        vault,
        kgRoot,
        reviewedSources: reviewed.length,
        nodesWritten: coreNodes.length,
      },
      null,
      2
    )
  );
}

main();
