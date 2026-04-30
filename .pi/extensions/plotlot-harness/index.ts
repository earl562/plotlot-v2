import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

/**
 * PlotLot Harness Dev Extension
 *
 * Dev-only helper commands for building PlotLot's agentic harness.
 *
 * - /ralph <goal>      : run a Ralph-style continuous loop via skill
 * - /research <query>  : run autoresearch via skill
 */
export default function (pi: ExtensionAPI) {
  pi.registerCommand("ralph", {
    description: "Run a Ralph-style continuous improvement loop on a goal (dev-only).",
    handler: async (args, ctx) => {
      const goal = (args || "").trim();
      if (!goal) {
        ctx.ui.notify("Usage: /ralph <goal>", "warning");
        return;
      }

      const ok = await ctx.ui.confirm(
        "Start Ralph loop?",
        `Goal:\n\n${goal}\n\nThis will enqueue follow-up agent messages. Continue?`
      );
      if (!ok) return;

      pi.sendUserMessage(`/skill:ralph-loop ${goal}`);
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
