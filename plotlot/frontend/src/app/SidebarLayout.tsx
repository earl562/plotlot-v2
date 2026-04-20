"use client";

import { useState, useEffect, useCallback } from "react";
import Sidebar, { SidebarToggle } from "@/components/Sidebar";
import { fetchRuntimeHealth, type RuntimeHealthData } from "@/lib/api";
import {
  listSessions,
  createSession,
  deleteSession,
  type ChatSession,
} from "@/lib/sessions";

export function SidebarLayout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(() => {
    if (typeof window === "undefined") return true;
    return window.matchMedia("(min-width: 1024px)").matches;
  });
  const [sessions, setSessions] = useState<ChatSession[]>(() => listSessions());
  const [activeSessionId, setActiveSessionId] = useState<string | null>(() => {
    const loaded = listSessions();
    return loaded.length > 0 ? loaded[0].id : null;
  });
  const [runtimeHealth, setRuntimeHealth] = useState<RuntimeHealthData | null>(null);

  // Auto-hide sidebar on mobile
  useEffect(() => {
    const mq = window.matchMedia("(min-width: 1024px)");
    const handler = (e: MediaQueryListEvent) => {
      setSidebarOpen(e.matches);
    };
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);

  const handleToggle = useCallback(() => setSidebarOpen((p) => !p), []);

  const handleNewChat = useCallback(() => {
    const session = createSession("lookup");
    setSessions(listSessions());
    setActiveSessionId(session.id);
    window.dispatchEvent(new CustomEvent("plotlot:session-selected", { detail: { id: session.id } }));
    setSidebarOpen(false); // close on mobile after action
  }, []);

  const handleSelectSession = useCallback((id: string) => {
    setActiveSessionId(id);
    window.dispatchEvent(new CustomEvent("plotlot:session-selected", { detail: { id } }));
    if (window.innerWidth < 1024) setSidebarOpen(false);
  }, []);

  const handleDeleteSession = useCallback(
    (id: string) => {
      deleteSession(id);
      const updated = listSessions();
      setSessions(updated);
      if (activeSessionId === id) {
        setActiveSessionId(updated.length > 0 ? updated[0].id : null);
      }
    },
    [activeSessionId],
  );

  // Expose session refresh for page.tsx via custom event
  useEffect(() => {
    const handler = () => setSessions(listSessions());
    window.addEventListener("plotlot:sessions-changed", handler);
    return () => window.removeEventListener("plotlot:sessions-changed", handler);
  }, []);

  useEffect(() => {
    let cancelled = false;

    const loadHealth = async () => {
      try {
        const health = await fetchRuntimeHealth();
        if (!cancelled) setRuntimeHealth(health);
      } catch {
        if (!cancelled) {
          setRuntimeHealth({
            status: "degraded",
            checks: { backend: "unreachable" },
            runtime: {
              startup_mode: "degraded",
              startup_warnings: ["backend_unreachable"],
            },
          });
        }
      }
    };

    void loadHealth();
    const interval = window.setInterval(() => void loadHealth(), 30_000);

    return () => {
      cancelled = true;
      window.clearInterval(interval);
    };
  }, []);

  const runtimeWarnings = runtimeHealth?.runtime?.startup_warnings ?? [];
  const isDegraded = runtimeHealth?.status === "degraded";

  return (
    <div className="flex h-screen overflow-hidden bg-[var(--bg-primary)]">
      <Sidebar
        sessions={sessions}
        activeSessionId={activeSessionId}
        isOpen={sidebarOpen}
        onToggle={handleToggle}
        onNewChat={handleNewChat}
        onSelectSession={handleSelectSession}
        onDeleteSession={handleDeleteSession}
        runtimeHealth={runtimeHealth}
      />

      <div className="relative flex min-w-0 flex-1 flex-col overflow-hidden">
        <div className="pointer-events-none absolute inset-x-0 top-0 h-56 bg-[radial-gradient(circle_at_top,var(--hero-glow),transparent_58%)] opacity-80" />
        {/* Mobile top bar */}
        <div
          className="relative z-10 flex items-center border-b border-[var(--border-soft)] bg-[var(--bg-surface)]/90 px-3 py-3 backdrop-blur-xl lg:hidden"
        >
          <SidebarToggle onClick={handleToggle} />
          <div className="ml-2 flex items-center gap-2">
            <div className="flex h-7 w-7 items-center justify-center rounded-full bg-[var(--brand-strong)] text-[10px] font-black text-white shadow-[0_10px_30px_rgba(180,83,9,0.18)]">
              P
            </div>
            <span className="font-display text-base tracking-tight text-[var(--text-primary)]">
              PlotLot
            </span>
          </div>
        </div>

        {isDegraded && (
          <div className="relative z-10 border-b border-amber-200/70 bg-[linear-gradient(90deg,rgba(255,251,235,0.96),rgba(255,247,237,0.9))] px-4 py-3 text-[13px] text-amber-900 dark:border-amber-800/60 dark:bg-[linear-gradient(90deg,rgba(69,26,3,0.92),rgba(67,20,7,0.88))] dark:text-amber-100">
            <div className="mx-auto flex max-w-6xl flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex items-center gap-2">
                <span className="inline-flex h-2.5 w-2.5 rounded-full bg-amber-500" />
                <span className="font-medium">
                  PlotLot is running in degraded local mode.
                </span>
              </div>
              <span className="text-[12px] text-amber-800/80 dark:text-amber-200/80">
                {runtimeWarnings.includes("database_unavailable")
                  ? "Database-backed analysis is unavailable until the local DB comes back."
                  : "Some backend capabilities are temporarily unavailable."}
              </span>
            </div>
          </div>
        )}

        {/* Main content */}
        <main className="relative z-0 flex-1 overflow-y-auto">{children}</main>
      </div>
    </div>
  );
}
