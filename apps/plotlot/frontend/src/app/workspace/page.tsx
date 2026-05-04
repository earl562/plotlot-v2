"use client";

import { useState, useRef, useEffect, useCallback, FormEvent, useId, type ReactNode, type RefObject } from "react";
import { motion } from "framer-motion";
import { staggerContainer, staggerItem, fadeUp, springGentle } from "@/lib/motion";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import ZoningReport from "@/components/ZoningReport";
import TabbedReport from "@/components/TabbedReport";
import DealTypeSelector from "@/components/DealTypeSelector";
import type { DealType } from "@/components/DealTypeSelector";
import PipelineApproval, { PIPELINE_STEPS } from "@/components/PipelineApproval";
import AnalysisStream from "@/components/AnalysisStream";
import AddressAutocomplete from "@/components/AddressAutocomplete";
import ModeToggle from "@/components/ModeToggle";
import type { AppMode } from "@/components/ModeToggle";
import CapabilityChips from "@/components/CapabilityChips";
import ToolCards from "@/components/ToolCards";
import DocumentCanvas from "@/components/DocumentCanvas";
import ErrorBoundary from "@/components/ErrorBoundary";
import InputBar from "@/components/InputBar";
import ThinkingIndicator from "@/components/ThinkingIndicator";
import { useToast } from "@/components/Toast";
import {
  AnalysisError,
  PipelineStatus,
  ZoningReportData,
  ChatMessageData,
  ToolUseEvent,
  ThinkingEvent,
  streamAnalysis,
  streamChat,
  saveAnalysis,
} from "@/lib/api";
import {
  createSession as createLocalSession,
  getSession as getLocalSession,
  updateSession as updateLocalSession,
} from "@/lib/sessions";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface ToolActivity {
  tool: string;
  message: string;
  status: "running" | "complete";
}

interface DisplayMessage {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  isStreaming?: boolean;
  pipelineSteps?: PipelineStatus[];
  thinkingEvents?: ThinkingEvent[];
  report?: ZoningReportData;
  saveStatus?: "idle" | "saving" | "saved" | "error";
  toolActivity?: ToolActivity[];
  errorType?: "timeout" | "bad_address" | "backend_unavailable" | "generic";
  retryAddress?: string;
}

// ---------------------------------------------------------------------------
// Address detection heuristic
// ---------------------------------------------------------------------------

const FL_PATTERNS = /\b(miami|fort lauderdale|hollywood|hialeah|pembroke|miramar|coral|doral|homestead|aventura|boca|delray|boynton|west palm|palm beach|broward|dade|FL|florida)\b/i;
const ADDRESS_PATTERN = /\d+\s+(?:\w+\s+)+(st|street|ave|avenue|blvd|boulevard|rd|road|dr|drive|ter|terrace|ct|court|ln|lane|way|pl|place|cir|circle|pkwy|parkway|hwy|highway|trl|trail|real|path)\b/i;
// Broader fallback: "123 Something, City, FL 33xxx" pattern (number + comma + FL indicator + zip)
const ADDRESS_WITH_ZIP = /\d+\s+[\w\s]+,\s*[\w\s]+,\s*FL\s+\d{5}/i;

function extractAddress(text: string): string | null {
  if (ADDRESS_PATTERN.test(text) && FL_PATTERNS.test(text)) {
    return text.trim();
  }
  if (ADDRESS_WITH_ZIP.test(text)) {
    return text.trim();
  }
  if (/\b(analyze|look up|lookup|check|search|zoning (?:for|rules|regulations|code)|what can .* build)\b/i.test(text) && FL_PATTERNS.test(text)) {
    // Only extract if there's an actual street address (starts with a number)
    const match = text.match(/\d+\s+[\w\s]+(?:,\s*[\w\s]+){0,3}/);
    if (match) return match[0].trim();
    // No street address found — route to chat instead
    return null;
  }
  return null;
}

// ---------------------------------------------------------------------------
// Suggestions
// ---------------------------------------------------------------------------

const FOLLOWUP_SUGGESTIONS = [
  "What can I build on this lot?",
  "Explain the density calculation",
  "What setback variances could I request?",
  "Is this suitable for multifamily?",
];

const WORKSPACE_PLAN_STEPS = [
  {
    key: "geocoding",
    label: "Resolve address",
    description: "Confirm the site location and jurisdiction before deeper analysis.",
  },
  {
    key: "property",
    label: "Pull parcel record",
    description: "Fetch parcel facts, lot dimensions, and ownership context.",
  },
  ...PIPELINE_STEPS.map((step) => ({
    key: step.key,
    label: step.label,
    description: step.description,
  })),
  {
    key: "report",
    label: "Assemble report",
    description: "Package evidence, recommendations, and follow-up actions.",
  },
] as const;

function getDealTypeLabel(dealType: DealType | null): string {
  if (!dealType) return "standard analysis";
  return dealType.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function RailCard({
  eyebrow,
  title,
  children,
  testId,
}: {
  eyebrow: string;
  title: string;
  children: ReactNode;
  testId: string;
}) {
  return (
    <section
      className="rounded-[1.5rem] border border-[var(--border-soft)] bg-[var(--bg-surface)] p-2 shadow-[var(--shadow-card)]"
      data-testid={testId}
    >
      <div className="rounded-[calc(1.5rem-0.5rem)] border border-white/50 bg-[var(--bg-surface-raised)] p-4 dark:border-white/5">
        <p className="text-[11px] uppercase tracking-[0.2em] text-[var(--text-muted)]">{eyebrow}</p>
        <h3 className="mt-2 text-sm font-semibold text-[var(--text-primary)]">{title}</h3>
        <div className="mt-3 space-y-3">{children}</div>
      </div>
    </section>
  );
}

function PlanStepPill({
  state,
  children,
}: {
  state: "complete" | "active" | "pending" | "skipped";
  children: ReactNode;
}) {
  const styles = {
    complete: "border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-800 dark:bg-emerald-950/30 dark:text-emerald-400",
    active: "border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-800 dark:bg-amber-950/30 dark:text-amber-400",
    pending: "border-[var(--border-soft)] bg-[var(--bg-primary)] text-[var(--text-muted)]",
    skipped: "border-[var(--border-soft)] bg-[var(--bg-primary)] text-[var(--text-muted)] opacity-70",
  } as const;

  return (
    <span className={`inline-flex shrink-0 rounded-full border px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.16em] ${styles[state]}`}>
      {children}
    </span>
  );
}

function getVisibleToolActivity(msg: DisplayMessage): ToolActivity[] {
  const tools = msg.toolActivity || [];
  if (tools.length === 0) return [];

  const running = tools.filter((t) => t.status === "running");
  if (running.length > 0) return running.slice(-1);

  return tools.slice(-1);
}

function getToolLabel(activity: ToolActivity): string {
  return activity.status === "complete" ? `Used ${activity.tool}` : activity.message;
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function Home() {
  const [mode, setMode] = useState<AppMode>("lookup");
  const [messages, setMessages] = useState<DisplayMessage[]>([]);
  const [input, setInput] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentReport, setCurrentReport] = useState<ZoningReportData | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  // Lookup mode: deal type flow
  const [pendingAddress, setPendingAddress] = useState<string | null>(null);
  const [selectedDealType, setSelectedDealType] = useState<DealType | null>(null);
  const [awaitingApproval, setAwaitingApproval] = useState(false);
  const [docCanvasOpen, setDocCanvasOpen] = useState(false);
  const [contextualSuggestions, setContextualSuggestions] = useState<string[]>([]);
  const [lastSkipSteps, setLastSkipSteps] = useState<string[]>([]);
  const [inputError, setInputError] = useState<string | null>(null);
  const [localSessionId, setLocalSessionId] = useState<string | null>(null);
  const [editingUserMessageId, setEditingUserMessageId] = useState<string | null>(null);
  const [editingUserDraft, setEditingUserDraft] = useState("");
  const [autoScrollEnabled, setAutoScrollEnabled] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const forceAutoScrollUntilRef = useRef<number>(0);
  const inputRef = useRef<HTMLInputElement | HTMLTextAreaElement>(null);
  const { toast } = useToast();
  const idPrefix = useId();
  const msgCounterRef = useRef(0);
  const localSessionIdRef = useRef<string | null>(null);
  const messagesRef = useRef<DisplayMessage[]>([]);
  const currentReportRef = useRef<ZoningReportData | null>(null);
  const modeRef = useRef<AppMode>("lookup");
  const hasProcessedRef = useRef(false);
  const chatAbortRef = useRef<AbortController | null>(null);
  const chatAssistantIdRef = useRef<string | null>(null);

  useEffect(() => {
    if (!autoScrollEnabled) return;
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, autoScrollEnabled]);

  const handleScroll = useCallback(() => {
    const el = scrollContainerRef.current;
    if (!el) return;
    if (Date.now() < forceAutoScrollUntilRef.current) {
      setAutoScrollEnabled((prev) => (prev ? prev : true));
      return;
    }
    const distanceFromBottom = el.scrollHeight - el.scrollTop - el.clientHeight;
    const nearBottom = distanceFromBottom < 160;
    setAutoScrollEnabled((prev) => (prev === nearBottom ? prev : nearBottom));
  }, []);

  const scrollToBottom = useCallback(() => {
    forceAutoScrollUntilRef.current = Date.now() + 1000;
    setAutoScrollEnabled(true);
    const el = scrollContainerRef.current;
    if (el) {
      el.scrollTo({ top: el.scrollHeight, behavior: "smooth" });
    } else {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, []);

  const copyToClipboard = useCallback(
    async (text: string) => {
      try {
        await navigator.clipboard.writeText(text);
        toast("Copied to clipboard", "success");
      } catch {
        toast("Copy failed", "error");
      }
    },
    [toast],
  );

  // Re-focus input on mount and when switching from welcome to conversation
  const isWelcome = messages.length === 0;
  useEffect(() => {
    inputRef.current?.focus();
  }, [isWelcome]);

  useEffect(() => {
    if (!isProcessing && !isWelcome && !docCanvasOpen) {
      inputRef.current?.focus();
    }
  }, [isProcessing, isWelcome, docCanvasOpen]);

  // Keep refs in sync with state
  useEffect(() => { messagesRef.current = messages; }, [messages]);
  useEffect(() => { currentReportRef.current = currentReport; }, [currentReport]);
  useEffect(() => { modeRef.current = mode; }, [mode]);
  useEffect(() => { localSessionIdRef.current = localSessionId; }, [localSessionId]);

  // Fix 3: Mode switch — clear lookup-mode state
  useEffect(() => {
    setPendingAddress(null);
    setSelectedDealType(null);
    setAwaitingApproval(false);
    setContextualSuggestions([]);
    setLastSkipSteps([]);
  }, [mode]);

  // Persist backend sessionId
  useEffect(() => {
    if (sessionId) localStorage.setItem("plotlot_backend_session", sessionId);
  }, [sessionId]);

  // Persist localSessionId
  useEffect(() => {
    if (localSessionId) localStorage.setItem("plotlot_last_session", localSessionId);
  }, [localSessionId]);

  // Mount: restore last session from localStorage
  useEffect(() => {
    const backendId = localStorage.getItem("plotlot_backend_session");
    if (backendId) setSessionId(backendId);

    const lastId = localStorage.getItem("plotlot_last_session");
    if (!lastId) return;
    const session = getLocalSession(lastId);
    if (!session || session.messages.length === 0) return;

    const restored: DisplayMessage[] = session.messages
      .filter((m) => m.role === "user" || m.role === "assistant")
      .map((m) => ({ id: m.id, role: m.role as "user" | "assistant", content: m.content }));
    if (restored.length === 0) return;

    if (session.report && restored.length > 0) {
      restored.splice(1, 0, {
        id: `${idPrefix}-mount-report`,
        role: "system",
        content: "",
        report: session.report,
      });
      setCurrentReport(session.report);
    }
    setMessages(restored);
    setLocalSessionId(lastId);
    localSessionIdRef.current = lastId;
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Save messages to local session after processing completes
  useEffect(() => {
    if (isProcessing) {
      hasProcessedRef.current = true;
      return;
    }
    if (!hasProcessedRef.current) return;
    hasProcessedRef.current = false;

    const msgs = messagesRef.current;
    const report = currentReportRef.current;
    const currentMode = modeRef.current;
    const sid = localSessionIdRef.current;

    const saveable = msgs
      .filter((m) => (m.role === "user" || m.role === "assistant") && m.content && !m.isStreaming)
      .map((m) => ({ id: m.id, role: m.role as "user" | "assistant", content: m.content, timestamp: new Date().toISOString() }));
    if (saveable.length === 0) return;

    const title = saveable[0]?.content?.slice(0, 60) || "New conversation";
    if (sid) {
      updateLocalSession(sid, { messages: saveable, ...(report ? { report } : {}) });
    } else {
      const newSession = createLocalSession(currentMode);
      updateLocalSession(newSession.id, { title, messages: saveable, ...(report ? { report } : {}) });
      setLocalSessionId(newSession.id);
      localSessionIdRef.current = newSession.id;
    }
    window.dispatchEvent(new CustomEvent("plotlot:sessions-changed"));
  }, [isProcessing]);

  // Listen for session selection from sidebar
  useEffect(() => {
    const handler = (e: Event) => {
      const id = (e as CustomEvent<{ id: string }>).detail?.id;
      if (!id) return;
      const session = getLocalSession(id);
      if (!session) return;

      const restored: DisplayMessage[] = session.messages
        .filter((m) => m.role === "user" || m.role === "assistant")
        .map((m) => ({ id: m.id, role: m.role as "user" | "assistant", content: m.content }));

      if (session.report && restored.length > 0) {
        restored.splice(1, 0, {
          id: `${idPrefix}-sel-report`,
          role: "system",
          content: "",
          report: session.report,
        });
        setCurrentReport(session.report);
      } else {
        setCurrentReport(null);
      }
      setMessages(restored);
      setLocalSessionId(id);
      localSessionIdRef.current = id;
      setInput("");
      setPendingAddress(null);
      setSelectedDealType(null);
      setAwaitingApproval(false);
      setLastSkipSteps([]);
      setIsProcessing(false);
    };
    window.addEventListener("plotlot:session-selected", handler);
    return () => window.removeEventListener("plotlot:session-selected", handler);
  }, [idPrefix]);

  const addMessage = useCallback((msg: Omit<DisplayMessage, "id">) => {
    const newMsg = { ...msg, id: `${idPrefix}-${msgCounterRef.current++}` };
    setMessages((prev) => [...prev, newMsg]);
    return newMsg.id;
  }, [idPrefix]);

  const updateMessage = useCallback((id: string, updates: Partial<DisplayMessage>) => {
    setMessages((prev) =>
      prev.map((m) => (m.id === id ? { ...m, ...updates } : m)),
    );
  }, []);

  // Run the full analysis pipeline
  const runAnalysis = useCallback(
    async (address: string, skipSteps: string[] = []) => {
      const progressId = addMessage({
        role: "system",
        content: "",
        pipelineSteps: [{
          step: "connecting",
          message: "Connecting to server...",
        }],
        thinkingEvents: [],
      });

      try {
        let finalReport: ZoningReportData | null = null;

        await streamAnalysis(
          {
            address,
            dealType: selectedDealType || "land_deal",
            skipSteps,
          },
          (status) => {
            setMessages((prev) =>
              prev.map((m) => {
                if (m.id !== progressId) return m;
                let steps = m.pipelineSteps || [];
                // Mark "connecting" as complete when first real step arrives
                const connectingIdx = steps.findIndex((s) => s.step === "connecting" && !s.complete);
                if (connectingIdx >= 0 && status.step !== "connecting") {
                  steps = steps.map((s) =>
                    s.step === "connecting" ? { ...s, complete: true, message: "Connected" } : s,
                  );
                }
                const existing = steps.findIndex((s) => s.step === status.step);
                if (existing >= 0) {
                  const updated = [...steps];
                  updated[existing] = status;
                  return { ...m, pipelineSteps: updated };
                }
                return { ...m, pipelineSteps: [...steps, status] };
              }),
            );
          },
          (report) => {
            finalReport = report;
            setCurrentReport(report);
            updateMessage(progressId, { report, pipelineSteps: undefined });
          },
          (error: AnalysisError) => {
            // Error recovery UX — provide actionable buttons based on error type
            const loweredError = error.detail.toLowerCase();
            const isTimeout = error.errorType === "timeout";
            const isBadAddress =
              error.errorType === "bad_address" ||
              error.errorType === "geocoding_failed" ||
              error.errorType === "low_accuracy" ||
              loweredError.includes("geocod") ||
              loweredError.includes("outside coverage") ||
              loweredError.includes("could not");
            const isBackendUnavailable =
              error.errorType === "backend_unavailable" ||
              loweredError.includes("backend is offline") ||
              loweredError.includes("temporarily unavailable");

            let errorContent = isBackendUnavailable
              ? "PlotLot's analysis backend is temporarily offline. Please try again shortly."
              : `I couldn't analyze that address: ${error.detail}`;
            if (isTimeout) {
              errorContent += "\n\nThe server took too long to respond. This can happen during the first request. Click **Retry** to try again.";
            } else if (isBadAddress) {
              errorContent += "\n\nPlease check the address and try a different one.";
            }
            updateMessage(progressId, {
              role: "assistant",
              content: errorContent,
              pipelineSteps: undefined,
              errorType: isTimeout ? "timeout" : isBadAddress ? "bad_address" : isBackendUnavailable ? "backend_unavailable" : "generic",
              retryAddress: address,
            } as Partial<DisplayMessage>);
          },
          (thinkingEvent) => {
            setMessages((prev) =>
              prev.map((m) => {
                if (m.id !== progressId) return m;
                return {
                  ...m,
                  thinkingEvents: [...(m.thinkingEvents || []), thinkingEvent],
                };
              }),
            );
          },
          (suggestions) => {
            setContextualSuggestions(suggestions);
          },
        );

        if (finalReport && mode === "agent") {
          addMessage({
            role: "assistant",
            content: "Here's the full zoning analysis. Ask me anything about this property.",
          });
        }
      } catch (err) {
        updateMessage(progressId, {
          role: "assistant",
          content: `Connection error: ${err instanceof Error ? err.message : "Failed to reach backend"}`,
          pipelineSteps: undefined,
        });
      }
    },
    [addMessage, updateMessage, selectedDealType, mode],
  );

  // Send a chat message
  const sendMessage = useCallback(
    async (text: string) => {
      if (!text.trim() || isProcessing) return;

      const address = extractAddress(text);

      // Lookup mode: validate address BEFORE adding to chat
      if (mode === "lookup" && !address) {
        setInputError("Please enter a street address to run a lookup analysis");
        return;
      }

      setIsProcessing(true);
      setInput("");
      setInputError(null);
      setAutoScrollEnabled(true);

      addMessage({ role: "user", content: text.trim() });

      // Lookup mode: address → deal type selector → pipeline
      if (mode === "lookup" && address) {
        setPendingAddress(address);
        setSelectedDealType(null);
        setCurrentReport(null);
        setIsProcessing(false);
        return;
      }

      // Agent mode: address detected — run pipeline directly
      if (address && !currentReport) {
        await runAnalysis(address);
        setIsProcessing(false);
        return;
      }
      if (address && currentReport) {
        setCurrentReport(null);
        await runAnalysis(address);
        setIsProcessing(false);
        return;
      }

      // Regular chat (agent mode only)
      const assistantId = addMessage({
        role: "assistant",
        content: "",
        isStreaming: true,
        toolActivity: [],
        thinkingEvents: [],
      });
      chatAssistantIdRef.current = assistantId;
      chatAbortRef.current = new AbortController();

      const history: ChatMessageData[] = [
        ...messagesRef.current
          .filter((m) => m.role === "user" || (m.role === "assistant" && m.content))
          .slice(-9)
          .map((m) => ({ role: m.role as "user" | "assistant", content: m.content })),
        { role: "user" as const, content: text.trim() },
      ];

      try {
        await streamChat(
          text.trim(),
          history,
          currentReport,
          (token) => {
            setMessages((prev) =>
              prev.map((m) =>
                m.id === assistantId && m.isStreaming
                  ? { ...m, content: m.content + token }
                  : m,
              ),
            );
          },
          (fullContent: string) => {
            updateMessage(assistantId, { content: fullContent, isStreaming: false });
          },
          (error) => {
            updateMessage(assistantId, {
              content: `Error: ${error}`,
              isStreaming: false,
            });
          },
          sessionId,
          (newSessionId) => {
            setSessionId(newSessionId);
            window.dispatchEvent(new CustomEvent("plotlot:sessions-changed"));
          },
          (toolEvent: ToolUseEvent) => {
            setMessages((prev) =>
              prev.map((m) => {
                if (m.id !== assistantId) return m;
                const tools = m.toolActivity || [];
                const lastTool = tools[tools.length - 1];
                if (lastTool?.tool === toolEvent.tool && lastTool.message === toolEvent.message) {
                  return m;
                }
                return {
                  ...m,
                  toolActivity: [...tools, { tool: toolEvent.tool, message: toolEvent.message, status: "running" as const }],
                };
              }),
            );
          },
          (toolName: string) => {
            setMessages((prev) =>
              prev.map((m) => {
                if (m.id !== assistantId) return m;
                const tools = [...(m.toolActivity || [])];
                for (let i = tools.length - 1; i >= 0; i -= 1) {
                  if (tools[i].tool === toolName && tools[i].status === "running") {
                    tools[i] = { ...tools[i], status: "complete" as const };
                    break;
                  }
                }
                return { ...m, toolActivity: tools };
              }),
            );
          },
          (thinkingEvent: ThinkingEvent) => {
            setMessages((prev) =>
              prev.map((m) => {
                if (m.id !== assistantId) return m;
                return {
                  ...m,
                  thinkingEvents: [...(m.thinkingEvents || []), thinkingEvent],
                };
              }),
            );
          },
          undefined,
          undefined,
          undefined,
          chatAbortRef.current.signal,
        );
      } catch {
        updateMessage(assistantId, {
          content: "Connection failed. Is the backend running?",
          isStreaming: false,
        });
      }

      setIsProcessing(false);
      chatAbortRef.current = null;
      chatAssistantIdRef.current = null;
    },
    [isProcessing, currentReport, sessionId, mode, addMessage, updateMessage, runAnalysis],
  );

  const stopGenerating = useCallback(() => {
    const controller = chatAbortRef.current;
    const assistantId = chatAssistantIdRef.current;
    if (!controller || !assistantId) return;
    controller.abort();
    chatAbortRef.current = null;
    chatAssistantIdRef.current = null;
    updateMessage(assistantId, { isStreaming: false });
    setIsProcessing(false);
  }, [updateMessage]);

  const beginEditUserMessage = useCallback((messageId: string, content: string) => {
    setEditingUserMessageId(messageId);
    setEditingUserDraft(content);
    toast("Editing prompt", "info");
  }, [toast]);

  const cancelEditUserMessage = useCallback(() => {
    setEditingUserMessageId(null);
    setEditingUserDraft("");
  }, []);

  const saveEditUserMessage = useCallback(() => {
    const messageId = editingUserMessageId;
    const nextText = editingUserDraft.trim();
    if (!messageId) return;
    if (!nextText) {
      toast("Prompt cannot be empty", "error");
      return;
    }

    const snapshot = messagesRef.current;
    const index = snapshot.findIndex((m) => m.id === messageId);
    if (index < 0) {
      cancelEditUserMessage();
      return;
    }

    // Trim conversation to before the edited prompt, then re-run the prompt.
    const trimmed = snapshot.slice(0, index);
    messagesRef.current = trimmed;
    setMessages(trimmed);
    cancelEditUserMessage();
    void sendMessage(nextText);
  }, [editingUserDraft, editingUserMessageId, cancelEditUserMessage, sendMessage, toast]);

  const retryFromAssistantIndex = useCallback(
    (assistantIndex: number) => {
      const snapshot = messagesRef.current;
      for (let i = assistantIndex - 1; i >= 0; i -= 1) {
        const candidate = snapshot[i];
        if (candidate?.role === "user" && candidate.content.trim()) {
          void sendMessage(candidate.content);
          return;
        }
      }
      toast("Nothing to retry yet", "info");
    },
    [sendMessage, toast],
  );

  const handleSave = useCallback(
    async (msgId: string, report: ZoningReportData) => {
      updateMessage(msgId, { saveStatus: "saving" });
      try {
        await saveAnalysis(report);
        updateMessage(msgId, { saveStatus: "saved" });
      } catch {
        updateMessage(msgId, { saveStatus: "error" });
      }
    },
    [updateMessage],
  );

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    sendMessage(input);
  };

  const hasReport = messages.some((m) => m.report);
  const latestPipelineMessage = [...messages].reverse().find((m) => (m.pipelineSteps?.length ?? 0) > 0) ?? null;
  const latestToolMessage = [...messages].reverse().find((m) => getVisibleToolActivity(m).length > 0) ?? null;
  const visibleToolActivity = latestToolMessage ? getVisibleToolActivity(latestToolMessage) : [];
  const latestPipelineMap = new Map((latestPipelineMessage?.pipelineSteps ?? []).map((step) => [step.step, step]));
  const inferredCompletedSteps = new Set<string>();
  if (currentReport) {
    inferredCompletedSteps.add("geocoding");
    inferredCompletedSteps.add("property");
    inferredCompletedSteps.add("search");
    inferredCompletedSteps.add("analysis");
    inferredCompletedSteps.add("report");
    if (currentReport.density_analysis) inferredCompletedSteps.add("calculation");
    if (currentReport.comp_analysis) inferredCompletedSteps.add("comps");
    if (currentReport.pro_forma) inferredCompletedSteps.add("proforma");
  }
  const activeAddress =
    currentReport?.formatted_address ||
    pendingAddress ||
    [...messages]
      .reverse()
      .map((m) => extractAddress(m.content))
      .find(Boolean) ||
    null;
  const dealTypeLabel = getDealTypeLabel(selectedDealType);
  const workspaceStage = awaitingApproval
    ? {
        label: "Approval needed",
        detail: `Review the ${dealTypeLabel} pipeline before PlotLot runs it.`,
        tone: "amber" as const,
      }
    : latestPipelineMessage
      ? {
          label: "Gathering evidence",
          detail:
            latestPipelineMessage.pipelineSteps?.find((step) => !step.complete)?.message ||
            "PlotLot is collecting parcel, zoning, and feasibility evidence.",
          tone: "amber" as const,
        }
      : currentReport
        ? {
            label: "Report ready",
            detail: "The latest report, evidence, and follow-up actions are ready in this workspace.",
            tone: "emerald" as const,
          }
        : mode === "agent" && messages.length > 0
          ? {
              label: "Agent follow-up",
              detail: "Use the conversation thread to refine conclusions and request deeper analysis.",
              tone: "blue" as const,
            }
          : {
              label: "Ready",
              detail: "Start with an address or a zoning question to create a new analysis.",
              tone: "slate" as const,
            };
  const stageBadgeStyles = {
    amber: "border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-800 dark:bg-amber-950/30 dark:text-amber-400",
    emerald: "border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-800 dark:bg-emerald-950/30 dark:text-emerald-400",
    blue: "border-sky-200 bg-sky-50 text-sky-700 dark:border-sky-800 dark:bg-sky-950/30 dark:text-sky-400",
    slate: "border-[var(--border-soft)] bg-[var(--bg-primary)] text-[var(--text-secondary)]",
  } as const;

  // Handle deal type selection in lookup mode — show pipeline approval
  const handleDealTypeSelect = useCallback(
    (dealType: DealType) => {
      if (!pendingAddress) return;
      setSelectedDealType(dealType);
      setAwaitingApproval(true);
    },
    [pendingAddress],
  );

  // Handle pipeline approval — run with selected skip steps
  const handlePipelineApprove = useCallback(
    async (skipSteps: string[]) => {
      if (!pendingAddress) return;
      const address = pendingAddress;
      setLastSkipSteps(skipSteps);
      setAwaitingApproval(false);
      setPendingAddress(null);
      setIsProcessing(true);
      try {
        await runAnalysis(address, skipSteps);
      } finally {
        setIsProcessing(false);
      }
    },
    [pendingAddress, runAnalysis],
  );

  const handlePipelineCancel = useCallback(() => {
    setAwaitingApproval(false);
    setSelectedDealType(null);
  }, []);

  const handleNewAnalysis = useCallback(() => {
    setMessages([]);
    setCurrentReport(null);
    setSessionId(null);
    setLocalSessionId(null);
    localSessionIdRef.current = null;
    hasProcessedRef.current = false;
    setPendingAddress(null);
    setSelectedDealType(null);
    setAwaitingApproval(false);
    setLastSkipSteps([]);
    setInput("");
    setIsProcessing(false);
    localStorage.removeItem("plotlot_backend_session");
    localStorage.removeItem("plotlot_last_session");
    setTimeout(() => inputRef.current?.focus(), 50);
  }, []);

  const getWorkspacePlanState = (key: string): "complete" | "active" | "pending" | "skipped" => {
    if (lastSkipSteps.includes(key)) return "skipped";
    if (inferredCompletedSteps.has(key)) return "complete";
    const pipelineStep = latestPipelineMap.get(key);
    if (pipelineStep?.complete) return "complete";
    if (pipelineStep && !pipelineStep.complete) return "active";
    return "pending";
  };

  const workspaceRail = (
    <div className="space-y-4">
      <RailCard eyebrow="Workspace status" title={workspaceStage.label} testId="workspace-status-card">
        <span className={`inline-flex w-fit rounded-full border px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.16em] ${stageBadgeStyles[workspaceStage.tone]}`}>
          {workspaceStage.label}
        </span>
        <p className="text-sm leading-6 text-[var(--text-secondary)]">{workspaceStage.detail}</p>
        <dl className="grid gap-2 text-xs text-[var(--text-secondary)]">
          <div className="flex items-start justify-between gap-4">
            <dt className="text-[var(--text-muted)]">Mode</dt>
            <dd className="font-medium text-[var(--text-primary)]">{mode === "lookup" ? "Lookup workspace" : "Agent workspace"}</dd>
          </div>
          {activeAddress && (
            <div className="flex items-start justify-between gap-4">
              <dt className="text-[var(--text-muted)]">Current site</dt>
              <dd className="max-w-[16rem] text-right font-medium text-[var(--text-primary)]">{activeAddress}</dd>
            </div>
          )}
          <div className="flex items-start justify-between gap-4">
            <dt className="text-[var(--text-muted)]">Deal lane</dt>
            <dd className="font-medium text-[var(--text-primary)]">{dealTypeLabel}</dd>
          </div>
          {visibleToolActivity.length > 0 && (
            <div className="flex items-start justify-between gap-4">
              <dt className="text-[var(--text-muted)]">Live tool</dt>
              <dd className="max-w-[16rem] text-right font-medium text-[var(--text-primary)]">
                {getToolLabel(visibleToolActivity[0])}
              </dd>
            </div>
          )}
          {latestToolMessage?.thinkingEvents?.length ? (
            <div className="flex items-start justify-between gap-4">
              <dt className="text-[var(--text-muted)]">Thinking trace</dt>
              <dd className="font-medium text-[var(--text-primary)]">{latestToolMessage.thinkingEvents.length} event{latestToolMessage.thinkingEvents.length === 1 ? "" : "s"}</dd>
            </div>
          ) : null}
        </dl>
      </RailCard>

      <RailCard eyebrow="Analysis plan" title="Plan, progress, and optional lanes" testId="workspace-plan-card">
        <p className="text-sm leading-6 text-[var(--text-secondary)]">
          PlotLot keeps the workflow explicit: parcel intake, zoning evidence, optional market/financial work, then a report you can refine.
        </p>
        <div className="space-y-2">
          {WORKSPACE_PLAN_STEPS.map((step) => {
            const state = getWorkspacePlanState(step.key);
            return (
              <div key={step.key} className="rounded-2xl border border-[var(--border-soft)] bg-[var(--bg-primary)] px-3 py-3">
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <p className="text-sm font-medium text-[var(--text-primary)]">{step.label}</p>
                    <p className="mt-1 text-xs leading-5 text-[var(--text-muted)]">{step.description}</p>
                  </div>
                  <PlanStepPill state={state}>{state}</PlanStepPill>
                </div>
              </div>
            );
          })}
        </div>
      </RailCard>

      <RailCard eyebrow="Evidence snapshot" title="What the current analysis has produced" testId="workspace-evidence-card">
        {currentReport ? (
          <>
            <dl className="grid gap-2 text-xs text-[var(--text-secondary)]">
              <div className="flex items-start justify-between gap-4">
                <dt className="text-[var(--text-muted)]">Jurisdiction</dt>
                <dd className="max-w-[16rem] text-right font-medium text-[var(--text-primary)]">
                  {currentReport.municipality}, {currentReport.county}
                </dd>
              </div>
              <div className="flex items-start justify-between gap-4">
                <dt className="text-[var(--text-muted)]">Zoning</dt>
                <dd className="font-medium text-[var(--text-primary)]">{currentReport.zoning_district || "Pending"}</dd>
              </div>
              <div className="flex items-start justify-between gap-4">
                <dt className="text-[var(--text-muted)]">Confidence</dt>
                <dd className="font-medium uppercase text-[var(--text-primary)]">{currentReport.confidence}</dd>
              </div>
              <div className="flex items-start justify-between gap-4">
                <dt className="text-[var(--text-muted)]">Sources</dt>
                <dd className="font-medium text-[var(--text-primary)]">{currentReport.sources.length}</dd>
              </div>
              <div className="flex items-start justify-between gap-4">
                <dt className="text-[var(--text-muted)]">Evidence refs</dt>
                <dd className="font-medium text-[var(--text-primary)]">{currentReport.source_refs?.length ?? 0}</dd>
              </div>
              {currentReport.density_analysis?.max_units != null && (
                <div className="flex items-start justify-between gap-4">
                  <dt className="text-[var(--text-muted)]">Max units</dt>
                  <dd className="font-medium text-[var(--text-primary)]">{currentReport.density_analysis.max_units}</dd>
                </div>
              )}
            </dl>
            {currentReport.confidence_warning && (
              <div className="rounded-2xl border border-amber-200 bg-amber-50 px-3 py-3 text-xs leading-5 text-amber-700 dark:border-amber-800 dark:bg-amber-950/30 dark:text-amber-400">
                {currentReport.confidence_warning}
              </div>
            )}
          </>
        ) : latestPipelineMessage ? (
          <p className="text-sm leading-6 text-[var(--text-secondary)]">
            Evidence is being assembled from parcel records, ordinance search, and optional market/financial steps. This card will summarize the results as soon as the report is ready.
          </p>
        ) : (
          <p className="text-sm leading-6 text-[var(--text-secondary)]">
            No evidence yet. Start with an address to generate parcel facts, zoning context, and structured report outputs.
          </p>
        )}
      </RailCard>

      <RailCard eyebrow="Report actions" title="How to work from the current result" testId="workspace-report-card">
        {currentReport ? (
          <>
            <p className="text-sm leading-6 text-[var(--text-secondary)]">
              Use the report panel for deep review, then keep the conversation focused on follow-up questions and document generation.
            </p>
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => setDocCanvasOpen(true)}
                className="rounded-full border border-amber-300 bg-amber-50 px-4 py-2 text-xs font-semibold text-amber-700 transition-colors hover:bg-amber-100 dark:border-amber-700 dark:bg-amber-950/30 dark:text-amber-400 dark:hover:bg-amber-950/50"
              >
                Open documents
              </button>
              {mode !== "agent" && (
                <button
                  onClick={() => setMode("agent")}
                  className="rounded-full border border-[var(--border)] bg-[var(--bg-primary)] px-4 py-2 text-xs font-semibold text-[var(--text-secondary)] transition-colors hover:bg-[var(--bg-surface-raised)]"
                >
                  Continue in agent mode
                </button>
              )}
            </div>
          </>
        ) : awaitingApproval ? (
          <p className="text-sm leading-6 text-[var(--text-secondary)]">
            The next action is to approve or trim the analysis plan so PlotLot can begin gathering evidence.
          </p>
        ) : (
          <p className="text-sm leading-6 text-[var(--text-secondary)]">
            Once PlotLot produces a report, this workspace will expose document generation and follow-up actions here instead of leaving everything buried in chat.
          </p>
        )}
      </RailCard>
    </div>
  );

  // Mode toggle is now the imported ModeToggle component

  // ─── Welcome State (both modes) ────────────────────────────────────
  if (isWelcome) {
    return (
      <main className="w-full max-w-full overflow-x-hidden px-4 py-8 sm:px-6 lg:px-10">
        <div className="mx-auto flex min-h-[calc(100dvh-5rem)] w-full max-w-7xl flex-col gap-8 py-12 md:py-20 xl:flex-row xl:items-start">
          <div className="flex min-w-0 flex-1 flex-col justify-center">
            <motion.div
              className="mb-6 inline-flex w-fit items-center gap-2 self-center rounded-full border border-[var(--border-soft)] bg-[var(--bg-surface)] px-4 py-2 text-[11px] uppercase tracking-[0.22em] text-[var(--text-secondary)] shadow-[var(--shadow-card)] xl:self-start"
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ ...springGentle, delay: 0.08 }}
            >
              <span className="inline-flex h-2 w-2 rounded-full bg-[var(--brand-strong)]" />
              PlotLot
            </motion.div>

            <motion.div
              className="mb-10"
              variants={staggerContainer}
              initial="hidden"
              animate="visible"
            >
              <div className="max-w-5xl">
                <motion.div
                  variants={staggerItem}
                  className="mb-4 text-sm tracking-wide text-[var(--text-muted)]"
                >
                  Hi there
                </motion.div>
                <motion.h1
                  variants={staggerItem}
                  className="max-w-5xl font-display text-[clamp(3.35rem,7vw,6.2rem)] leading-[0.98] text-[var(--text-primary)]"
                >
                  {mode === "lookup" ? (
                    <>Analyze any property in the US</>
                  ) : (
                    <>Ask anything about zoning &amp; land</>
                  )}
                </motion.h1>
                <motion.p variants={staggerItem} className="mt-5 max-w-2xl text-[15px] leading-7 text-[var(--text-secondary)] sm:text-[17px]">
                  {mode === "lookup"
                    ? "Zoning, density, comps, pro forma, and development potential — in seconds"
                    : "Search properties, research zoning codes, or get answers from our database. Use agent mode when you need an exploratory partner, not just a single lookup."}
                </motion.p>
              </div>
            </motion.div>

            {/* Input bar — z-30 so autocomplete dropdown (z-50 inside) paints above chips below */}
            <motion.form
              onSubmit={handleSubmit}
              {...fadeUp}
              transition={{ ...springGentle, delay: 0.25 }}
              className="relative z-30 mb-8 w-full max-w-4xl self-center xl:self-start"
            >
              <div
                className="glass-panel flex items-center gap-2 rounded-full border border-[var(--border-soft)] bg-[var(--bg-surface)] px-4 py-3 transition-all focus-within:border-amber-400/60 focus-within:ring-2 focus-within:ring-amber-400/15 sm:px-5 sm:py-4"
                style={{ boxShadow: "var(--shadow-elevated)" }}
              >
                {mode === "lookup" ? (
                  <AddressAutocomplete
                    inputRef={inputRef as RefObject<HTMLInputElement | null>}
                    value={input}
                    onChange={(v) => { setInput(v); if (inputError) setInputError(null); }}
                    onSelect={(address) => sendMessage(address)}
                    placeholder="Enter a property address..."
                    disabled={isProcessing}
                  />
                ) : (
                  <textarea
                    ref={inputRef as RefObject<HTMLTextAreaElement>}
                    rows={1}
                    value={input}
                    onChange={(e) => {
                      setInput(e.target.value);
                      if (inputError) setInputError(null);
                      e.currentTarget.style.height = "0px";
                      e.currentTarget.style.height = `${e.currentTarget.scrollHeight}px`;
                    }}
                    onKeyDown={(e) => {
                      if (e.key === "Enter" && !e.shiftKey) {
                        e.preventDefault();
                        e.currentTarget.form?.requestSubmit();
                      }
                    }}
                    placeholder="Ask about zoning, density, or property data..."
                    disabled={isProcessing}
                    className="min-w-0 flex-1 resize-none bg-transparent text-sm text-[var(--text-primary)] placeholder:text-[var(--text-muted)] focus:outline-none"
                    data-testid="agent-input"
                  />
                )}
                <ModeToggle mode={mode} onChange={setMode} />
                <button
                  type="submit"
                  disabled={!input.trim() || isProcessing}
                  aria-label="Send message"
                  data-testid="send-button"
                  className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[var(--text-primary)] text-[var(--bg-primary)] transition-all hover:opacity-80 disabled:opacity-20 sm:h-9 sm:w-9"
                >
                  {isProcessing ? (
                    <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                    </svg>
                  ) : (
                    <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.5}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
                    </svg>
                  )}
                </button>
              </div>
              {inputError && (
                <p className="mt-2 px-1 text-xs text-red-500">{inputError}</p>
              )}
            </motion.form>

            {/* Capability chips / Tool cards — z-0 so autocomplete dropdown from form above paints on top */}
            <motion.div
              {...fadeUp}
              transition={{ ...springGentle, delay: 0.35 }}
              className="relative z-0 min-h-[72px] w-full max-w-4xl self-center xl:self-start"
            >
              {mode === "lookup" ? (
                <CapabilityChips mode={mode} onSelect={sendMessage} disabled={isProcessing} />
              ) : (
                <ToolCards
                  onAnalyze={() => inputRef.current?.focus()}
                  onGenerateDoc={() => setDocCanvasOpen(true)}
                  onSendPrompt={sendMessage}
                  disabled={isProcessing}
                  hasReport={!!currentReport}
                  county={currentReport?.county}
                  municipality={currentReport?.municipality}
                  lat={currentReport?.lat}
                  lng={currentReport?.lng}
                />
              )}
            </motion.div>

            {/* Footer */}
            <motion.p
              {...fadeUp}
              transition={{ ...springGentle, delay: 0.45 }}
              className="mt-12 text-center text-xs text-[var(--text-muted)] xl:text-left"
            >
              PlotLot analyzes zoning, density, comps &amp; pro forma for any US property
            </motion.p>
          </div>

          <aside className="w-full xl:sticky xl:top-6 xl:w-[340px] xl:shrink-0">
            {workspaceRail}
          </aside>
        </div>
      </main>
    );
  }

  // ─── Conversation State ───────────────────────────────────────────────
  return (
    <div className="relative flex h-[calc(100vh-4rem)] flex-col">
      {/* New Analysis button — fixed top-right */}
      <div className="fixed right-4 top-5 z-40 sm:right-6">
        <button
          onClick={handleNewAnalysis}
          data-testid="new-analysis-button"
          className="flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--bg-surface)] px-3 py-1.5 text-xs font-medium text-[var(--text-muted)] transition-all hover:border-[var(--border-hover)] hover:text-[var(--text-secondary)] active:scale-[0.98]"
          style={{ boxShadow: "var(--shadow-nav)" }}
        >
          <svg className="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
            <path d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" />
          </svg>
          New analysis
        </button>
      </div>
      {/* Messages */}
      <div
        ref={scrollContainerRef}
        onScroll={handleScroll}
        className="flex-1 overflow-y-auto pb-52"
        data-testid="conversation-scroll"
      >
        <div className="mx-auto flex w-full max-w-7xl flex-col gap-6 px-3 py-4 sm:px-4 sm:py-6 xl:flex-row xl:items-start">
          <div className="min-w-0 flex-1">
            <div className="space-y-4 sm:space-y-6" role="log" aria-live="polite" aria-label="Analysis conversation">
              {messages.map((msg, msgIndex) => (
                <div key={msg.id} className="animate-fade-up">
              {/* Pipeline progress — inline stepper */}
              {msg.pipelineSteps && msg.pipelineSteps.length > 0 && !msg.report && (
                <div className="flex items-start gap-3">
                  <div className="mt-1 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-amber-800 text-xs font-black text-white">
                    P
                  </div>
                  <AnalysisStream
                    steps={msg.pipelineSteps}
                    error={null}
                    onWrongProperty={handleNewAnalysis}
                    thinkingEvents={msg.thinkingEvents}
                  />
                </div>
              )}

              {/* Embedded report — TabbedReport for lookup mode, ZoningReport for agent */}
              {msg.report && (
                <div className="space-y-3 animate-fade-up">
                  <ErrorBoundary>
                    {selectedDealType ? (
                      <TabbedReport report={msg.report} dealType={selectedDealType} />
                    ) : (
                      <ZoningReport report={msg.report} />
                    )}
                  </ErrorBoundary>
                  {msg.report.confidence_warning && (
                    <div className="rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 dark:border-amber-800 dark:bg-amber-950/40">
                      <div className="flex items-start gap-3">
                        <svg className="mt-0.5 h-4 w-4 shrink-0 text-amber-600" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M8.485 2.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.168 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 2.495zM10 6a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0v-3.5A.75.75 0 0110 6zm0 9a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
                        </svg>
                        <div>
                          <p className="text-sm font-medium text-amber-800 dark:text-amber-400">{msg.report.confidence_warning}</p>
                          {msg.report.suggested_next_steps && msg.report.suggested_next_steps.length > 0 && (
                            <ul className="mt-1.5 space-y-1">
                              {msg.report.suggested_next_steps.map((step, i) => (
                                <li key={i} className="text-xs text-amber-700 dark:text-amber-500">&#8226; {step}</li>
                              ))}
                            </ul>
                          )}
                        </div>
                      </div>
                    </div>
                  )}
                  <div className="flex justify-end gap-2">
                    <button
                      onClick={() => setDocCanvasOpen(true)}
                      className="min-h-[44px] rounded-lg border border-amber-300 bg-amber-50 px-4 py-2 text-sm font-semibold text-amber-700 transition-colors hover:bg-amber-100 dark:border-amber-700 dark:bg-amber-950/30 dark:text-amber-400 dark:hover:bg-amber-950/50 sm:min-h-0 sm:py-1.5"
                    >
                      Generate Documents
                    </button>
                    <button
                      onClick={() => handleSave(msg.id, msg.report!)}
                      disabled={msg.saveStatus === "saving" || msg.saveStatus === "saved"}
                      className={`min-h-[44px] rounded-lg px-4 py-2 text-sm font-semibold transition-colors sm:min-h-0 sm:py-1.5 ${
                        msg.saveStatus === "saved"
                          ? "bg-lime-100 text-lime-700"
                          : msg.saveStatus === "error"
                            ? "bg-red-100 text-red-600"
                            : "border border-[var(--border)] bg-[var(--bg-surface)] text-[var(--text-secondary)] hover:bg-[var(--bg-surface-raised)]"
                      }`}
                    >
                      {msg.saveStatus === "saving"
                        ? "Saving..."
                        : msg.saveStatus === "saved"
                          ? "Saved to Portfolio"
                          : "Save to Portfolio"}
                    </button>
                  </div>
                </div>
              )}

              {msg.role === "assistant" && msg.thinkingEvents && msg.thinkingEvents.length > 0 && (
                <div className="mb-2 ml-9 max-w-[95%] sm:max-w-[85%]">
                  <ThinkingIndicator events={msg.thinkingEvents} />
                </div>
              )}

              {/* Tool use badges (ChatGPT-style) */}
              {msg.toolActivity && msg.toolActivity.length > 0 && (() => {
                const visibleTools = getVisibleToolActivity(msg);
                if (visibleTools.length === 0) return null;

                return (
                  <div className="mb-2 flex justify-start">
                    <div className="flex items-start gap-3">
                      <div className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-amber-800 text-xs font-black text-white">
                        P
                      </div>
                      <div className="flex flex-wrap gap-1.5">
                        {visibleTools.map((t, i) => (
                          <span
                            key={i}
                            className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium transition-colors ${
                              t.status === "running"
                                ? "border border-amber-300 bg-amber-50 text-amber-700 dark:border-amber-700 dark:bg-amber-950/40 dark:text-amber-400"
                                : "border border-[var(--border)] bg-[var(--bg-surface-raised)] text-[var(--text-muted)]"
                            }`}
                          >
                            {t.status === "running" ? (
                              <div className="h-1.5 w-1.5 rounded-full bg-amber-500 animate-pulse-dot" />
                            ) : (
                              <svg className="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                              </svg>
                            )}
                            {getToolLabel(t)}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                );
              })()}

              {/* Regular message */}
              {msg.content && msg.role !== "system" && (
                <div className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                  {msg.role === "user" ? (
                    /* User message — right-aligned plain text, no bubble */
                    <div className="max-w-[90%] sm:max-w-[75%]">
                      {editingUserMessageId === msg.id ? (
                        <div className="rounded-2xl border border-[var(--border)] bg-[var(--bg-surface)] p-3 shadow-[var(--shadow-elevated)]">
                          <textarea
                            value={editingUserDraft}
                            onChange={(e) => setEditingUserDraft(e.target.value)}
                            rows={3}
                            className="w-full resize-none bg-transparent text-sm leading-relaxed text-[var(--text-secondary)] focus:outline-none"
                            data-testid="user-edit-input"
                            autoFocus
                          />
                          <div className="mt-2 flex justify-end gap-2">
                            <button
                              type="button"
                              onClick={cancelEditUserMessage}
                              className="rounded-lg border border-[var(--border)] bg-[var(--bg-surface)] px-3 py-1.5 text-xs font-semibold text-[var(--text-muted)] hover:text-[var(--text-secondary)]"
                              data-testid="user-edit-cancel"
                            >
                              Cancel
                            </button>
                            <button
                              type="button"
                              onClick={saveEditUserMessage}
                              className="rounded-lg bg-[var(--text-primary)] px-3 py-1.5 text-xs font-semibold text-[var(--bg-primary)] hover:opacity-90"
                              data-testid="user-edit-save"
                            >
                              Save &amp; run
                            </button>
                          </div>
                        </div>
                      ) : (
                        <div className="group text-sm leading-relaxed text-[var(--text-secondary)]">
                          <div>{msg.content}</div>
                          {mode === "agent" && (
                            <div className="mt-1 flex justify-end gap-1.5 text-[10px] font-semibold text-[var(--text-muted)] opacity-100 sm:opacity-0 sm:transition-opacity sm:group-hover:opacity-100">
                              <button
                                type="button"
                                onClick={() => copyToClipboard(msg.content)}
                                className="inline-flex items-center gap-1 rounded-md border border-[var(--border)] bg-[var(--bg-surface)] px-2 py-1 hover:text-[var(--text-secondary)]"
                                aria-label="Copy prompt"
                                data-testid="user-copy"
                              >
                                <svg className="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                                  <path d="M8 2a2 2 0 00-2 2v1H5a2 2 0 00-2 2v9a2 2 0 002 2h7a2 2 0 002-2v-1h1a2 2 0 002-2V7.414A2 2 0 0016.414 6L13 2.586A2 2 0 0011.586 2H8z" />
                                </svg>
                                Copy
                              </button>
                              <button
                                type="button"
                                onClick={() => beginEditUserMessage(msg.id, msg.content)}
                                className="inline-flex items-center gap-1 rounded-md border border-[var(--border)] bg-[var(--bg-surface)] px-2 py-1 hover:text-[var(--text-secondary)] disabled:opacity-40"
                                aria-label="Edit prompt"
                                data-testid="user-edit"
                                disabled={isProcessing}
                              >
                                <svg className="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-8.25 8.25a1 1 0 01-.43.263l-3 1a1 1 0 01-1.263-1.263l1-3a1 1 0 01.263-.43l8.25-8.25z" />
                                </svg>
                                Edit
                              </button>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  ) : (
                    /* Assistant message — left-aligned with avatar */
                    <div className="group flex items-start gap-2 max-w-[95%] sm:gap-3 sm:max-w-[85%]">
                      <div className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-amber-800 text-xs font-black text-white">
                        P
                      </div>
                      <div
                        className="text-sm leading-relaxed text-[var(--text-secondary)] min-w-0"
                        data-testid={
                          msg.errorType ||
                          msg.content.startsWith("Error:") ||
                          msg.content.startsWith("Connection error:")
                            ? "report-error"
                            : undefined
                        }
                      >
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm]}
                          components={{
                            p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                            strong: ({ children }) => <strong className="font-semibold text-[var(--text-primary)]">{children}</strong>,
                            ul: ({ children }) => <ul className="mb-2 ml-4 list-disc space-y-1">{children}</ul>,
                            ol: ({ children }) => <ol className="mb-2 ml-4 list-decimal space-y-1">{children}</ol>,
                            li: ({ children }) => <li>{children}</li>,
                            h1: ({ children }) => <h1 className="mb-2 text-lg font-bold text-[var(--text-primary)]">{children}</h1>,
                            h2: ({ children }) => <h2 className="mb-2 text-base font-bold text-[var(--text-primary)]">{children}</h2>,
                            h3: ({ children }) => <h3 className="mb-1 text-sm font-bold text-[var(--text-primary)]">{children}</h3>,
                            a: ({ href, children }) => <a href={href} target="_blank" rel="noopener noreferrer" className="text-amber-700 underline hover:text-amber-600">{children}</a>,
                            pre: ({ children }) => {
                              const child = Array.isArray(children) ? children[0] : children;
                              const codeChildren =
                                child && typeof child === "object" && "props" in child
                                  ? (child as { props?: { children?: unknown } }).props?.children
                                  : children;
                              const codeText = String(codeChildren ?? "").replace(/\n$/, "");
                              return (
                                <div className="group relative mb-2">
                                  <pre className="overflow-x-auto rounded-lg bg-[var(--bg-surface-raised)] p-3 text-xs">
                                    <code className="font-mono text-[var(--text-secondary)]">{codeText}</code>
                                  </pre>
                                  <button
                                    type="button"
                                    aria-label="Copy code"
                                    onClick={() => copyToClipboard(codeText)}
                                    className="absolute right-2 top-2 rounded-md border border-[var(--border)] bg-[var(--bg-surface)] px-2 py-1 text-[10px] font-semibold text-[var(--text-muted)] opacity-0 transition-opacity hover:text-[var(--text-secondary)] group-hover:opacity-100"
                                  >
                                    Copy
                                  </button>
                                </div>
                              );
                            },
                            code: ({ children }) => (
                              <code className="rounded bg-[var(--bg-surface-raised)] px-1.5 py-0.5 text-xs font-mono text-[var(--text-secondary)]">
                                {children}
                              </code>
                            ),
                            table: ({ children }) => (
                              <div className="my-2 overflow-x-auto rounded-lg border border-[var(--border)]">
                                <table className="min-w-full text-xs">{children}</table>
                              </div>
                            ),
                            thead: ({ children }) => <thead className="bg-[var(--bg-surface-raised)]">{children}</thead>,
                            tbody: ({ children }) => <tbody className="[&>tr:nth-child(even)]:bg-[var(--bg-surface-raised)]">{children}</tbody>,
                            th: ({ children }) => <th className="border-b border-[var(--border)] px-3 py-1.5 text-left font-semibold text-[var(--text-secondary)]">{children}</th>,
                            td: ({ children }) => <td className="border-b border-[var(--border)] px-3 py-1.5 text-[var(--text-secondary)]">{children}</td>,
                          }}
                        >
                          {msg.content}
                        </ReactMarkdown>
                        {/* Streaming cursor — pulsing dot */}
                        {msg.isStreaming && msg.content && (
                          <span className="ml-1 inline-block h-2 w-2 rounded-full bg-amber-500 animate-pulse-dot" />
                        )}
                        {msg.isStreaming && !msg.content && (
                          <span className="inline-flex items-center gap-1 text-[var(--text-muted)]">
                            <span className="h-2 w-2 rounded-full bg-amber-500 animate-pulse-dot" />
                            <span className="text-xs">Thinking...</span>
                          </span>
                        )}

                        {!msg.isStreaming && msg.content && (
                          <div className="mt-2 flex items-center gap-2 text-[10px] font-semibold text-[var(--text-muted)] opacity-100 sm:opacity-0 sm:transition-opacity sm:group-hover:opacity-100">
                            <button
                              type="button"
                              onClick={() => copyToClipboard(msg.content)}
                              className="inline-flex items-center gap-1 rounded-md border border-[var(--border)] bg-[var(--bg-surface)] px-2 py-1 hover:text-[var(--text-secondary)]"
                              aria-label="Copy response"
                              data-testid="assistant-copy"
                            >
                              <svg className="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                                <path d="M8 2a2 2 0 00-2 2v1H5a2 2 0 00-2 2v9a2 2 0 002 2h7a2 2 0 002-2v-1h1a2 2 0 002-2V7.414A2 2 0 0016.414 6L13 2.586A2 2 0 0011.586 2H8z" />
                              </svg>
                              Copy
                            </button>
                            <button
                              type="button"
                              onClick={() => retryFromAssistantIndex(msgIndex)}
                              className="inline-flex items-center gap-1 rounded-md border border-[var(--border)] bg-[var(--bg-surface)] px-2 py-1 hover:text-[var(--text-secondary)]"
                              aria-label="Retry prompt"
                              data-testid="assistant-retry"
                            >
                              <svg className="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M15.312 11.424a5.5 5.5 0 00-9.17-5.24l-.191.182V4.5a.75.75 0 00-1.5 0v3.25c0 .414.336.75.75.75h3.25a.75.75 0 000-1.5H6.61l.57-.54a4 4 0 016.677 3.814.75.75 0 001.455.39zm.239 1.151a.75.75 0 00-1.455-.39 4 4 0 01-6.676-3.814l.57.54H10a.75.75 0 000-1.5H6.75a.75.75 0 00-.75.75v3.25a.75.75 0 001.5 0v-1.866l.191.182a5.5 5.5 0 009.17 5.24z" clipRule="evenodd" />
                              </svg>
                              Retry
                            </button>
                          </div>
                        )}
                        {/* Error recovery buttons */}
                        {msg.errorType && !msg.isStreaming && (
                          <div className="mt-3 flex gap-2">
                            {(msg.errorType === "timeout" || msg.errorType === "backend_unavailable") && msg.retryAddress && (
                              <button
                                onClick={() => {
                                  setMessages((prev) => prev.filter((m) => m.id !== msg.id));
                                  runAnalysis(msg.retryAddress!);
                                }}
                                disabled={isProcessing}
                                data-testid="report-retry-button"
                                className="rounded-lg border border-amber-300 bg-amber-50 px-3 py-1.5 text-xs font-medium text-amber-700 transition-colors hover:bg-amber-100 disabled:opacity-40"
                              >
                                Retry
                              </button>
                            )}
                            {msg.errorType === "bad_address" && (
                              <button
                                onClick={() => {
                                  setInput("");
                                  inputRef.current?.focus();
                                }}
                                className="rounded-lg border border-[var(--border)] bg-[var(--bg-surface)] px-3 py-1.5 text-xs font-medium text-[var(--text-secondary)] transition-colors hover:bg-[var(--bg-surface-raised)]"
                              >
                                Try another address
                              </button>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              )}
                </div>
              ))}
              {/* Deal type selector — appears when address entered in lookup mode */}
              {pendingAddress && !selectedDealType && (
                <div className="mx-auto max-w-xl px-3 py-4 sm:px-0">
                  <DealTypeSelector onSelect={handleDealTypeSelect} disabled={isProcessing} />
                </div>
              )}

              {/* Pipeline approval gate — appears after deal type selection */}
              {pendingAddress && selectedDealType && awaitingApproval && (
                <div className="mx-auto max-w-xl px-3 py-4 sm:px-0 animate-fade-up">
                  <PipelineApproval
                    address={pendingAddress}
                    dealType={selectedDealType}
                    onApprove={handlePipelineApprove}
                    onCancel={handlePipelineCancel}
                    disabled={isProcessing}
                  />
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>
          </div>

          <aside className="xl:sticky xl:top-6 xl:w-[340px] xl:shrink-0">
            {workspaceRail}
          </aside>
        </div>
      </div>

      {/* Bottom area — gradient fade + suggestions + floating input */}
      <div className="absolute bottom-0 left-0 right-0">
        {!autoScrollEnabled && (
          <div className="pointer-events-none absolute -top-12 left-0 right-0 flex justify-center">
            <button
              type="button"
              onClick={scrollToBottom}
              className="pointer-events-auto inline-flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--bg-surface)] px-3 py-1.5 text-xs font-semibold text-[var(--text-secondary)] shadow-[var(--shadow-elevated)] hover:bg-[var(--bg-surface-raised)]"
              data-testid="scroll-to-bottom"
              aria-label="Scroll to latest"
            >
              <svg className="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 14a.75.75 0 01-.53-.22l-4-4a.75.75 0 111.06-1.06L10 12.19l3.47-3.47a.75.75 0 111.06 1.06l-4 4A.75.75 0 0110 14z" clipRule="evenodd" />
              </svg>
              Jump to latest
            </button>
          </div>
        )}
        {/* Gradient fade */}
        <div className="input-fade-bg h-8 pointer-events-none" />

        <div className="bg-[var(--bg-primary)] px-3 pb-3 sm:px-4 sm:pb-4">
          {/* Contextual suggestions — lookup mode after report */}
          {mode === "lookup" && hasReport && contextualSuggestions.length > 0 && !isProcessing && (
            <div className="mx-auto mb-3 flex max-w-3xl flex-wrap gap-2 px-3 sm:gap-2 sm:px-0">
              {contextualSuggestions.map((s) => (
                <button
                  key={s}
                  onClick={() => { setMode("agent"); sendMessage(s); }}
                  className="min-h-[44px] rounded-full border border-amber-200 bg-amber-50/50 px-4 py-2 text-xs text-amber-700 transition-all hover:bg-amber-100 hover:-translate-y-0.5 active:scale-[0.98] dark:border-amber-800 dark:bg-amber-950/30 dark:text-amber-400 dark:hover:bg-amber-950/50 sm:min-h-0 sm:py-1.5"
                >
                  {s}
                </button>
              ))}
            </div>
          )}

          {/* Follow-up suggestions — agent mode only */}
          {mode === "agent" && !isProcessing && messages.length > 0 && messages[messages.length - 1]?.role === "assistant" && !messages[messages.length - 1]?.isStreaming && (
            <div className="mx-auto mb-3 flex max-w-3xl flex-wrap gap-2 px-3 sm:gap-2 sm:px-0">
              {FOLLOWUP_SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  onClick={() => sendMessage(s)}
                  disabled={isProcessing}
                  className="min-h-[44px] rounded-full border border-[var(--border)] bg-[var(--bg-surface)] px-4 py-2 text-xs text-[var(--text-muted)] transition-all hover:border-[var(--border-hover)] hover:text-[var(--text-secondary)] hover:-translate-y-0.5 active:scale-[0.98] disabled:opacity-40 sm:min-h-0 sm:py-1.5"
                >
                  {s}
                </button>
              ))}
            </div>
          )}

          {/* Live tool shortcuts — agent mode */}
          {mode === "agent" && (
            <div className="mx-auto mb-3 w-full max-w-3xl px-3 sm:px-0" data-testid="agent-live-tools">
              <ToolCards
                onAnalyze={() => inputRef.current?.focus()}
                onGenerateDoc={() => setDocCanvasOpen(true)}
                onSendPrompt={sendMessage}
                disabled={isProcessing}
                hasReport={!!currentReport}
                county={currentReport?.county}
                municipality={currentReport?.municipality}
                lat={currentReport?.lat}
                lng={currentReport?.lng}
                visibleIds={["open_data_layers", "municode_live"]}
              />
            </div>
          )}

          {/* Input bar — hidden in lookup mode after report is shown */}
          {!(mode === "lookup" && hasReport) && (
            <div>
              <InputBar
                inputRef={inputRef}
                value={input}
                onChange={(v) => { setInput(v); if (inputError) setInputError(null); }}
                onSubmit={handleSubmit}
                onAddressSelect={(address) => sendMessage(address)}
                mode={mode}
                onModeChange={setMode}
                placeholder={mode === "lookup"
                  ? "Enter a property address..."
                  : hasReport
                    ? "Ask about this property's zoning..."
                    : "Ask about zoning, density, or property data..."
                }
                  disabled={isProcessing || !!pendingAddress || awaitingApproval}
                  isProcessing={isProcessing}
                  canStop={
                    mode === "agent" &&
                    isProcessing &&
                    messages.length > 0 &&
                    messages[messages.length - 1]?.role === "assistant" &&
                    !!messages[messages.length - 1]?.isStreaming
                  }
                  onStop={stopGenerating}
                />
              {inputError && (
                <p className="mt-2 px-4 text-xs text-red-500">{inputError}</p>
              )}
            </div>
          )}

        </div>
      </div>

      {/* Document Canvas modal */}
      {currentReport && (
        <DocumentCanvas
          report={currentReport}
          isOpen={docCanvasOpen}
          onClose={() => setDocCanvasOpen(false)}
        />
      )}
    </div>
  );
}
