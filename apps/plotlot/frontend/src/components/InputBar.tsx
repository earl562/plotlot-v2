"use client";

import { FormEvent, RefObject } from "react";
import AddressAutocomplete from "@/components/AddressAutocomplete";
import ModeToggle from "@/components/ModeToggle";
import type { AppMode } from "@/components/ModeToggle";

interface InputBarProps {
  inputRef: RefObject<HTMLInputElement | null>;
  value: string;
  onChange: (value: string) => void;
  onSubmit: (e: FormEvent) => void;
  onAddressSelect: (address: string) => void;
  mode: AppMode;
  onModeChange: (mode: AppMode) => void;
  placeholder?: string;
  disabled?: boolean;
  isProcessing?: boolean;
}

export default function InputBar({
  inputRef,
  value,
  onChange,
  onSubmit,
  onAddressSelect,
  mode,
  onModeChange,
  placeholder = "Enter an address or ask a question...",
  disabled = false,
  isProcessing = false,
}: InputBarProps) {
  return (
    <div className="mx-auto max-w-3xl">
      <form onSubmit={onSubmit}>
        <div
          className="flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--bg-surface)] px-3 py-2.5 transition-all focus-within:border-amber-400/60 focus-within:ring-2 focus-within:ring-amber-400/15 sm:px-4 sm:py-3"
          style={{ boxShadow: "var(--shadow-elevated)" }}
        >
          {mode === "lookup" ? (
            <AddressAutocomplete
              inputRef={inputRef}
              value={value}
              onChange={onChange}
              onSelect={onAddressSelect}
              placeholder={placeholder}
              disabled={disabled}
            />
          ) : (
            <input
              ref={inputRef}
              type="text"
              value={value}
              onChange={(e) => onChange(e.target.value)}
              placeholder={placeholder}
              disabled={disabled}
              className="min-w-0 flex-1 bg-transparent text-sm text-[var(--text-primary)] placeholder:text-[var(--text-muted)] focus:outline-none"
              data-testid="agent-input"
            />
          )}
          <ModeToggle mode={mode} onChange={onModeChange} />
          <button
            type="submit"
            disabled={!value.trim() || isProcessing}
            aria-label="Send message"
            data-testid="send-button"
            className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-[var(--text-primary)] text-[var(--bg-primary)] transition-all hover:opacity-80 disabled:opacity-20"
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
      </form>
    </div>
  );
}
