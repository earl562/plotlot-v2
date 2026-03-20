"use client";

import { useState, useEffect, useCallback } from "react";
import Sidebar, { SidebarToggle } from "@/components/Sidebar";
import {
  listSessions,
  createSession,
  deleteSession,
  type ChatSession,
} from "@/lib/sessions";

export function SidebarLayout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);

  // Load sessions on mount
  useEffect(() => {
    const loaded = listSessions();
    setSessions(loaded);
    if (loaded.length > 0) {
      setActiveSessionId(loaded[0].id);
    }
  }, []);

  // Auto-hide sidebar on mobile
  useEffect(() => {
    const mq = window.matchMedia("(min-width: 1024px)");
    const handler = (e: MediaQueryListEvent) => {
      if (!e.matches) setSidebarOpen(false);
    };
    if (!mq.matches) setSidebarOpen(false);
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);

  const handleToggle = useCallback(() => setSidebarOpen((p) => !p), []);

  const handleNewChat = useCallback(() => {
    const session = createSession("lookup");
    setSessions(listSessions());
    setActiveSessionId(session.id);
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

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar
        sessions={sessions}
        activeSessionId={activeSessionId}
        isOpen={sidebarOpen}
        onToggle={handleToggle}
        onNewChat={handleNewChat}
        onSelectSession={handleSelectSession}
        onDeleteSession={handleDeleteSession}
      />

      <div className="flex min-w-0 flex-1 flex-col">
        {/* Mobile top bar */}
        <div className="flex items-center border-b px-3 py-2 lg:hidden" style={{ borderColor: "var(--border)", background: "var(--bg-surface)" }}>
          <SidebarToggle onClick={handleToggle} />
          <div className="ml-2 flex items-center gap-2">
            <div className="flex h-6 w-6 items-center justify-center rounded-full bg-amber-800 text-[10px] font-black text-white dark:bg-amber-600">
              P
            </div>
            <span className="font-display text-base tracking-tight" style={{ color: "var(--text-primary)" }}>
              PlotLot
            </span>
          </div>
        </div>

        {/* Main content */}
        <main className="flex-1 overflow-y-auto">{children}</main>
      </div>
    </div>
  );
}
