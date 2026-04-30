import { defineConfig, devices } from "@playwright/test";

// The Codex sandbox disallows binding to 0.0.0.0, so keep the dev server on loopback.
const PLAYWRIGHT_PORT = process.env.PLAYWRIGHT_PORT ?? "3003";
const BASE_URL = process.env.PLAYWRIGHT_BASE_URL ?? `http://127.0.0.1:${PLAYWRIGHT_PORT}`;
const USE_EXTERNAL_WEBSERVER = process.env.PLAYWRIGHT_DISABLE_WEBSERVER === "1";
const REUSE_EXISTING_WEBSERVER = process.env.PLAYWRIGHT_REUSE_SERVER === "1";
const WEB_SERVER_PORT = new URL(BASE_URL).port || PLAYWRIGHT_PORT;

export default defineConfig({
  testDir: "./tests",
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: 1,
  reporter: [["html", { open: "never" }], ["list"]],
  timeout: 120_000,
  globalSetup: require.resolve("./tests/global-setup"),
  use: {
    baseURL: BASE_URL,
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
  },
  outputDir: "./test-results",
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
  webServer: USE_EXTERNAL_WEBSERVER
    ? undefined
    : [
        {
          command: `npm run dev -- --hostname 127.0.0.1 --port ${WEB_SERVER_PORT}`,
          url: BASE_URL,
          reuseExistingServer: REUSE_EXISTING_WEBSERVER,
          timeout: 90_000,
          env: { PLAYWRIGHT_TESTING: "1" },
        },
      ],
});
