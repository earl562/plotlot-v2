"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { usePathname } from "next/navigation";

type Theme = "light" | "dark";

interface ThemeContextValue {
  theme: Theme;
  resolved: Theme;
  setTheme: (t: Theme) => void;
}

const ThemeContext = createContext<ThemeContextValue>({
  theme: "light",
  resolved: "light",
  setTheme: () => {},
});

export function useTheme() {
  return useContext(ThemeContext);
}

function isPublicRoute(pathname: string) {
  return pathname === "/" || pathname === "/reference" || pathname === "/analyze";
}

function resolveInitialTheme(pathname: string): Theme {
  if (typeof window === "undefined") return "light";
  try {
    const stored = localStorage.getItem("theme");
    if (stored === "light" || stored === "dark") return stored;
  } catch {
    // ignore storage errors
  }

  return isPublicRoute(pathname) ? "light" : "dark";
}

function applyThemeClass(theme: Theme) {
  if (typeof document === "undefined") return;
  document.documentElement.classList.toggle("dark", theme === "dark");
}

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const pathname = usePathname() ?? "/";
  // Keep the first render deterministic (matches server HTML); reconcile in an effect.
  const [theme, setThemeState] = useState<Theme>("light");

  useEffect(() => {
    const initial = resolveInitialTheme(pathname);
    applyThemeClass(initial);
    const frame = window.requestAnimationFrame(() => {
      setThemeState(initial);
    });
    return () => window.cancelAnimationFrame(frame);
  }, [pathname]);

  const setTheme = useCallback((next: Theme) => {
    setThemeState(next);
    applyThemeClass(next);
    try {
      localStorage.setItem("theme", next);
    } catch {
      // ignore storage errors
    }
  }, []);

  const value = useMemo<ThemeContextValue>(() => {
    return { theme, resolved: theme, setTheme };
  }, [setTheme, theme]);

  return (
    <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
  );
}
