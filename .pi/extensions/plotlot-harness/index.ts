import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

/**
 * PlotLot Harness Dev Extension
 *
 * Dev-only helper commands for building PlotLot's agentic harness.
 *
 * - /ralph <goal>                 : start a Ralph persistence loop (max 50 iterations by default)
 * - /ralph --max 25 <goal>        : override max iterations
 * - /ralph --yes <goal>           : skip confirmation (useful for RPC/scripted runs)
 * - /ralph status                 : show current Ralph state
 * - /ralph pause                  : pause auto-continue
 * - /ralph resume                 : resume auto-continue
 * - /ralph steer <note>           : add steering note applied on next iteration
 * - /ralph goal <new goal>        : update goal while running
 * - /ralph stop                   : stop Ralph loop
 * - /research <query>             : run autoresearch via skill
 */

type RalphState = {
  active: boolean;
  paused?: boolean;
  goal: string;
  iteration: number;
  maxIterations: number;
  startedAt: string;
  lastStatus?: string;
  steering?: string[];
};

const RALPH_STATE_ENTRY = "plotlot-harness:ralph-state";

function coerceInt(v: string | undefined, fallback: number) {
  const n = Number(v);
  return Number.isFinite(n) && n > 0 ? Math.floor(n) : fallback;
}

function extractText(content: unknown): string {
  if (typeof content === "string") return content;
  if (!Array.isArray(content)) return "";
  return content
    .filter((c) => c && typeof c === "object" && (c as any).type === "text")
    .map((c) => String((c as any).text || ""))
    .join("\n");
}

function extractRalphStatus(text: string): string | null {
  const matches = [...text.matchAll(/RALPH_STATUS:\s*([A-Z]+)/gi)];
  if (matches.length === 0) return null;
  return (matches[matches.length - 1][1] || "").toUpperCase();
}

function parseRalphArgs(rawArgs: string): {
  cmd: "start" | "status" | "stop" | "steer" | "goal" | "pause" | "resume";
  goal: string;
  maxIterations: number;
  yes: boolean;
  steerText: string;
} {
  const trimmed = (rawArgs || "").trim();
  if (trimmed === "status") return { cmd: "status", goal: "", maxIterations: 50, yes: false, steerText: "" };
  if (trimmed === "stop" || trimmed === "cancel") return { cmd: "stop", goal: "", maxIterations: 50, yes: false, steerText: "" };
  if (trimmed === "pause") return { cmd: "pause", goal: "", maxIterations: 50, yes: false, steerText: "" };
  if (trimmed === "resume" || trimmed === "continue") return { cmd: "resume", goal: "", maxIterations: 50, yes: false, steerText: "" };

  if (trimmed.startsWith("steer ")) {
    return {
      cmd: "steer",
      goal: "",
      maxIterations: 50,
      yes: false,
      steerText: trimmed.slice("steer ".length).trim(),
    };
  }
  if (trimmed.startsWith("goal ") || trimmed.startsWith("set-goal ")) {
    const prefix = trimmed.startsWith("goal ") ? "goal " : "set-goal ";
    return {
      cmd: "goal",
      goal: trimmed.slice(prefix.length).trim(),
      maxIterations: 50,
      yes: false,
      steerText: "",
    };
  }

  const tokens = trimmed.length ? trimmed.split(/\s+/) : [];
  let yes = false;
  let maxIterations = 50;
  let i = 0;
  while (i < tokens.length) {
    const t = tokens[i];
    if (t === "--yes" || t === "-y") {
      yes = true;
      i++;
      continue;
    }
    if (t === "--max") {
      maxIterations = coerceInt(tokens[i + 1], maxIterations);
      i += 2;
      continue;
    }
    if (t.startsWith("--max=")) {
      maxIterations = coerceInt(t.slice("--max=".length), maxIterations);
      i++;
      continue;
    }
    break;
  }

  const goal = tokens.slice(i).join(" ").trim();
  return { cmd: "start", goal, maxIterations, yes, steerText: "" };
}

export default function (pi: ExtensionAPI) {
  let ralph: RalphState | null = null;

  function persistState() {
    if (!ralph) return;
    pi.appendEntry(RALPH_STATE_ENTRY, ralph);
  }

  function setStatusLine(ctx: any) {
    if (!ctx?.ui) return;
    if (!ralph?.active) {
      ctx.ui.setStatus("ralph", undefined);
      return;
    }
    ctx.ui.setStatus("ralph", `ralph ${ralph.iteration}/${ralph.maxIterations}`);
  }

  // Restore state across /reload and session resume.
  pi.on("session_start", async (_event, ctx) => {
    const entries = ctx.sessionManager.getEntries();
    for (let i = entries.length - 1; i >= 0; i--) {
      const e = entries[i];
      if (e.type !== "custom" || e.customType !== RALPH_STATE_ENTRY) continue;
      const data = e.data as any;
      if (data && typeof data === "object") {
        ralph = data as RalphState;
      }
      break;
    }
    setStatusLine(ctx);
  });

  // Auto-continue Ralph after each agent run until COMPLETE/BLOCKED/MAXED or iteration budget exhausted.
  pi.on("agent_end", async (event, ctx) => {
    if (!ralph?.active) return;
    if (ralph.paused) return;

    const assistantText = (event.messages || [])
      .filter((m: any) => m?.role === "assistant")
      .map((m: any) => extractText(m.content))
      .join("\n");

    const status = extractRalphStatus(assistantText);
    ralph.lastStatus = status || ralph.lastStatus;

    if (status === "COMPLETE") {
      ralph.active = false;
      persistState();
      setStatusLine(ctx);
      ctx.ui.notify("Ralph complete.", "info");
      return;
    }

    if (status === "BLOCKED") {
      ralph.active = false;
      persistState();
      setStatusLine(ctx);
      ctx.ui.notify("Ralph blocked (needs user input).", "warning");
      return;
    }

    if (status === "MAXED") {
      ralph.active = false;
      persistState();
      setStatusLine(ctx);
      ctx.ui.notify("Ralph stopped (MAXED).", "warning");
      return;
    }

    if (ralph.iteration >= ralph.maxIterations) {
      ralph.active = false;
      ralph.lastStatus = "MAXED";
      persistState();
      setStatusLine(ctx);
      ctx.ui.notify(`Ralph hit max iterations (${ralph.maxIterations}).`, "warning");
      return;
    }

    const next = ralph.iteration + 1;
    ralph.iteration = next;
    persistState();
    setStatusLine(ctx);

    const missingStatus = status == null;
    const steering = (ralph.steering || []).slice();
    ralph.steering = [];
    persistState();

    const prompt = [
      `[RALPH ITERATION ${next}/${ralph.maxIterations}]`,
      "Continue working on the same goal. Do not restart from scratch.",
      `Goal: ${ralph.goal}`,
      steering.length ? `Steering updates (apply now):\n- ${steering.join("\n- ")}` : "",
      missingStatus ? "(Your last iteration did not include a RALPH_STATUS line; include it this time.)" : "",
      "Remember: end your response with exactly one RALPH_STATUS line.",
    ]
      .filter(Boolean)
      .join("\n");

    pi.sendUserMessage(`/skill:ralph-loop ${prompt}`);
  });

  pi.registerCommand("ralph", {
    description: "Start/stop/status/steer for Ralph persistence loop (dev-only).",
    handler: async (args, ctx) => {
      const parsed = parseRalphArgs(args || "");

      if (parsed.cmd === "status") {
        if (!ralph?.active) {
          ctx.ui.notify("Ralph is not active.", "info");
          return;
        }
        ctx.ui.notify(
          `Ralph ${ralph.paused ? "(paused)" : "(active)"}: ${ralph.iteration}/${ralph.maxIterations}` +
            `\nLast status: ${ralph.lastStatus || "(none)"}` +
            `\nGoal: ${ralph.goal}`,
          "info"
        );
        return;
      }

      if (parsed.cmd === "pause") {
        if (ralph?.active) {
          ralph.paused = true;
          persistState();
          setStatusLine(ctx);
        }
        ctx.ui.notify("Ralph paused. Use /ralph resume to continue.", "info");
        return;
      }

      if (parsed.cmd === "resume") {
        if (ralph?.active) {
          ralph.paused = false;
          persistState();
          setStatusLine(ctx);
          ctx.ui.notify("Ralph resumed (will continue after the next agent run).", "info");
        } else {
          ctx.ui.notify("Ralph is not active.", "info");
        }
        return;
      }

      if (parsed.cmd === "steer") {
        if (!ralph?.active) {
          ctx.ui.notify("Ralph is not active. Start it with /ralph <goal>.", "warning");
          return;
        }
        const note = (parsed.steerText || "").trim();
        if (!note) {
          ctx.ui.notify("Usage: /ralph steer <note>", "warning");
          return;
        }
        ralph.steering = [...(ralph.steering || []), note];
        persistState();
        ctx.ui.notify("Steering note queued for next Ralph iteration.", "info");
        return;
      }

      if (parsed.cmd === "goal") {
        if (!ralph?.active) {
          ctx.ui.notify("Ralph is not active. Start it with /ralph <goal>.", "warning");
          return;
        }
        const newGoal = (parsed.goal || "").trim();
        if (!newGoal) {
          ctx.ui.notify("Usage: /ralph goal <new goal>", "warning");
          return;
        }
        ralph.goal = newGoal;
        persistState();
        ctx.ui.notify("Ralph goal updated.", "info");
        return;
      }

      if (parsed.cmd === "stop") {
        if (ralph?.active) {
          ralph.active = false;
          ralph.lastStatus = "STOPPED";
          persistState();
          setStatusLine(ctx);
        }
        ctx.ui.notify("Ralph stopped.", "info");
        return;
      }

      const goal = parsed.goal.trim();
      if (!goal) {
        ctx.ui.notify(
          "Usage: /ralph [--max N] [--yes] <goal> | status | pause | resume | steer <note> | goal <new goal> | stop",
          "warning"
        );
        return;
      }

      const expandedGoal = `${goal}\n\nAfter we review the arXiv papers, implement our findings for PlotLot's specific agentic vertical (land-use/site-feasibility harness).`;

      if (!parsed.yes) {
        const ok = await ctx.ui.confirm(
          "Start Ralph loop?",
          `Goal:\n\n${expandedGoal}\n\nMax iterations: ${parsed.maxIterations}\n\nThis will enqueue follow-up agent messages until COMPLETE/BLOCKED/MAXED. Continue?`
        );
        if (!ok) return;
      }

      ralph = {
        active: true,
        paused: false,
        goal: expandedGoal,
        iteration: 1,
        maxIterations: parsed.maxIterations,
        startedAt: new Date().toISOString(),
        steering: [],
      };
      persistState();
      setStatusLine(ctx);

      // Run Ralph iteration 1 via the ralph-loop skill; the extension will auto-continue up to max iterations.
      pi.sendUserMessage(`/skill:ralph-loop [RALPH ITERATION 1/${parsed.maxIterations}]\nGoal: ${expandedGoal}`);
    },
  });

  pi.registerCommand("research", {
    description: "Run autoresearch over URLs/papers (dev-only).",
    handler: async (args, ctx) => {
      const q = (args || "").trim();
      if (!q) {
        ctx.ui.notify("Usage: /research <topic|question|url>", "warning");
        return;
      }

      pi.sendUserMessage(`/skill:autoresearch ${q}`);
    },
  });
}
