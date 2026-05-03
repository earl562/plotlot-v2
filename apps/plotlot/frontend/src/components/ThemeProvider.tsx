"use client";

import { createContext, useContext, useCallback } from "react";

type Theme = "light";

interface ThemeContextValue {
  theme: Theme;
  resolved: "light";
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

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const setTheme = useCallback(() => {
    document.documentElement.classList.remove("dark");
    localStorage.setItem("theme", "light");
  }, []);

  return (
    <ThemeContext.Provider value={{ theme: "light", resolved: "light", setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
