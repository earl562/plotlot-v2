#!/usr/bin/env node

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

function readJson(p, fallback) {
  return exists(p) ? JSON.parse(readText(p)) : fallback;
}

function mkdirp(p) {
  fs.mkdirSync(p, { recursive: true });
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
    out.push({
      arxivId: (fm.arxiv_id || path.basename(f, ".md")).replace(/"/g, ""),
      title: (fm.title || "").replace(/^"|"$/g, ""),
      absUrl: (fm.abs_url || "").replace(/"/g, ""),
      pdfUrl: (fm.pdf_url || "").replace(/"/g, ""),
      repoPath: full,
    });
  }
  out.sort((a, b) => a.arxivId.localeCompare(b.arxivId));
  return out;
}

function extractSection(md, heading) {
  const re = new RegExp(`^##\\s+${heading.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\s*$([\\s\\S]*?)(?=^##\\s+|$)`, "im");
  const m = md.match(re);
  return m?.[1]?.trim() || "";
}

function bulletsFromSection(md, heading) {
  return extractSection(md, heading)
    .split(/\r?\n/)
    .map((l) => l.trim())
    .filter((l) => l.startsWith("- "))
    .map((l) => l.slice(2).trim());
}

function writeNode(node, nodesDir) {
  const p = path.join(nodesDir, `${node.name}.md`);
  const body = [
    "---",
    "kg_node: true",
    `kg_type: ${JSON.stringify(node.type || "primitive")}`,
    node.sources?.length ? `sources: [${node.sources.map((s) => JSON.stringify(s)).join(", ")}]` : null,
    "---",
    `# ${node.name}`,
    "## What this is",
    `- Type: ${node.type || "primitive"}`,
    "## Notes",
    ...((node.bullets || []).map((b) => `- ${b}`)),
    "## Sources",
    ...((node.sources || []).map((s) => `- [[Sources/arXiv/${s}|${s}]]`)),
    "## Links",
    ...((node.links || []).map((l) => `- [[${l}]]`)),
    "",
  ].filter(Boolean).join("\n");
  fs.writeFileSync(p, body, "utf8");
}

function writeSourceNote(reviewedNote, curation, sourcesDir) {
  const md = readText(reviewedNote.repoPath);
  const relRepo = path.relative(REPO_ROOT, reviewedNote.repoPath);
  const connection = curation.sourceConnections?.[reviewedNote.arxivId] || {};
  const section = (name) => extractSection(md, name);
  const out = [
    "---",
    `source_type: "arxiv"`,
    `arxiv_id: ${JSON.stringify(reviewedNote.arxivId)}`,
    `title: ${JSON.stringify(reviewedNote.title)}`,
    reviewedNote.absUrl ? `abs_url: ${JSON.stringify(reviewedNote.absUrl)}` : null,
    reviewedNote.pdfUrl ? `pdf_url: ${JSON.stringify(reviewedNote.pdfUrl)}` : null,
    `repo_note: ${JSON.stringify(relRepo)}`,
    "---",
    `# ${reviewedNote.arxivId} — ${reviewedNote.title}`,
    "## Repo note",
    `- ${relRepo}`,
    "## Key primitives",
    section("Key primitives / claims") || section("Key primitives"),
    "## PlotLot implications",
    section("Harness implications for PlotLot") || section("PlotLot implications"),
    "## Evaluation ideas",
    section("Evaluation ideas"),
    "## Deltas",
    section("Deltas"),
    "## KG connections",
    ...((connection.wikilinks || []).map((l) => `- [[${l}]]`)),
    "## Current synthesis",
    ...((connection.bullets || []).map((b) => `- ${b}`)),
    "## Quotes",
    section("Quotes") || section("Relevant quotes (optional)"),
    "",
  ].filter(Boolean).join("\n");
  fs.writeFileSync(path.join(sourcesDir, `${reviewedNote.arxivId}.md`), out, "utf8");
}

function main() {
  const vaultPathFile = path.join(REPO_ROOT, "docs/research/obsidian-vault-path.txt");
  if (!exists(vaultPathFile)) throw new Error(`missing ${vaultPathFile}`);
  const vault = readText(vaultPathFile).trim();
  if (!exists(vault)) throw new Error(`vault path does not exist: ${vault}`);

  const kgRoot = path.join(vault, "Harnesses", "Harness Engineering KG");
  const nodesDir = path.join(kgRoot, "Nodes");
  const sourcesDir = path.join(kgRoot, "Sources", "arXiv");
  mkdirp(nodesDir);
  mkdirp(sourcesDir);

  const curationPath = path.join(REPO_ROOT, "docs/research/harness-kg-curation.json");
  const curation = readJson(curationPath, { nodes: [], overviewConnections: [], sourceConnections: {} });
  const reviewed = listReviewedArxivNotes();

  const coreNodes = [
    {
      name: "Harness Runtime",
      type: "system",
      bullets: [
        "Orchestrates skills, tools, memory, evidence, approvals, and reports.",
        "The harness is the product; the model is just one component inside it."
      ],
      links: ["Context Broker", "Governance Middleware", "Evidence Ledger"]
    },
    {
      name: "Context Broker",
      type: "primitive",
      bullets: [
        "Select -> Write -> Compress -> Isolate operations over memory/evidence.",
        "Keep context small, specific, and stage-bounded."
      ],
      links: ["Harness Runtime", "Evidence Ledger"]
    },
    {
      name: "Governance Middleware",
      type: "primitive",
      bullets: [
        "Policy layer for tool execution: read vs write, internal vs external, expensive vs cheap.",
        "Requires approvals for high-risk actions and captures audit logs."
      ],
      links: ["Harness Runtime", "Evidence Ledger"]
    },
    {
      name: "Evidence Ledger",
      type: "primitive",
      bullets: [
        "Every important claim should resolve to a source-backed evidence item.",
        "Tool runs should emit evidence records with URLs, timestamps, and extracted fields."
      ],
      links: ["Harness Runtime", "Workflow Verification"]
    }
  ];

  for (const node of [...coreNodes, ...(curation.nodes || [])]) writeNode(node, nodesDir);
  for (const reviewedNote of reviewed) writeSourceNote(reviewedNote, curation, sourcesDir);

  const latestReviewed = reviewed.length ? reviewed[reviewed.length - 1].arxivId : null;
  const overview = [
    "---",
    "kg_root: true",
    `generated_from_repo: ${JSON.stringify("docs/research/harness-primitives.md")}`,
    `generated_from_curation: ${JSON.stringify("docs/research/harness-kg-curation.json")}`,
    `generated_at: ${JSON.stringify(new Date().toISOString())}`,
    "---",
    "# Harness Engineering KG — Overview",
    "",
    "This folder is a living knowledge graph in Obsidian for harness engineering, built from repo-owned arXiv reviews and distilled toward PlotLot’s land-use/site-feasibility harness.",
    "",
    "## How to use",
    "",
    "- Start with [[Harness Runtime]] and branch into [[Context Broker]], [[Governance Middleware]], and [[Evidence Ledger]].",
    "- Then move into workflow-spec and adaptation nodes like [[Executable Specification]], [[Step-Bounded Context]], [[Workflow Module Interface]], [[Replayable Trajectory]], [[Workflow Verification]], [[Agent-Supervised Tool Adaptation]], [[Adaptation Signal Design]], and [[Graduated Subagent]].",
    "- Keep detailed learning in Nodes; keep Sources/arXiv as paper-backed entry points into the graph.",
    "",
    "## PlotLot mapping (first principles)",
    "",
    "- Harness coordinates: Workspace -> Project -> Site -> Analysis -> Evidence -> Report -> Action.",
    "- Deterministic code handles facts, schemas, numeric validation, and scoring; LLMs handle decomposition, extraction strategy, synthesis, and explanation.",
    "- Governance and verification gate any transition from retrieved text to product-facing conclusions.",
    "- The long-term architecture trend is frozen core + adaptive periphery: stable orchestrator, evolving retrieval/memory/review specialists.",
    "",
    "## Latest connection pass",
    "",
    ...((curation.overviewConnections || []).flatMap((c) => [
      `### ${c.title}`,
      ...c.bullets.map((b) => `- ${b}`),
      ""
    ])),
    "## Index",
    "",
    "### Core nodes",
    "- [[Harness Runtime]]",
    "- [[Context Broker]]",
    "- [[Governance Middleware]]",
    "- [[Evidence Ledger]]",
    "",
    `### Curated nodes (${(curation.nodes || []).length})`,
    ...((curation.nodes || []).map((n) => `- [[${n.name}]]`)),
    "",
    `### Sources (reviewed arXiv notes: ${reviewed.length})`,
    "- Browse: `Sources/arXiv/`",
    latestReviewed ? `- Latest reviewed source in repo export: [[Sources/arXiv/${latestReviewed}|${latestReviewed}]]` : null,
    "",
  ].filter(Boolean).join("\n");

  fs.writeFileSync(path.join(kgRoot, "00 - Overview.md"), overview, "utf8");
  console.log(JSON.stringify({ vault, kgRoot, reviewedSources: reviewed.length, nodesWritten: coreNodes.length + (curation.nodes || []).length, latestReviewed }, null, 2));
}

main();
