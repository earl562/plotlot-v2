import { test, expect, type Locator, type Page } from "@playwright/test";

async function gotoWelcome(page: Page) {
  await page.goto("/");
  await page.waitForLoadState("networkidle");
  await expect(page.getByText("PlotLot", { exact: true }).first()).toBeVisible();
}

async function stubAnalyzeStream(page: Page) {
  const body = `event: status\ndata: ${JSON.stringify({ step: "geocoding", message: "Resolving address...", complete: false })}\n\n`;

  await page.evaluate((streamBody) => {
    const originalFetch = window.fetch.bind(window);
    window.fetch = ((input: RequestInfo | URL, init?: RequestInit) => {
      const url = typeof input === "string" ? input : input instanceof Request ? input.url : input.toString();
      if (url.includes("/api/v1/analyze/stream")) {
        const stream = new ReadableStream({
          start(controller) {
            controller.enqueue(new TextEncoder().encode(streamBody));
          },
        });
        return Promise.resolve(
          new Response(stream, {
            status: 200,
            headers: { "content-type": "text/event-stream" },
          }),
        );
      }
      return originalFetch(input, init);
    }) as typeof window.fetch;
  }, body);

  await page.route("**/api/v1/analyze/stream", async (route) => {
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "content-type",
    };
    if (route.request().method() === "OPTIONS") {
      await route.fulfill({
        status: 204,
        headers: corsHeaders,
      });
      return;
    }

    await route.fulfill({
      status: 200,
      contentType: "text/event-stream",
      headers: corsHeaders,
      body,
    });
  });
}

async function expectCompactHero(heading: Locator) {
  await expect(heading).toBeVisible();

  const metrics = await heading.evaluate((node) => {
    const el = node as HTMLElement;
    const style = window.getComputedStyle(el);
    const lineHeight = Number.parseFloat(style.lineHeight);
    const rect = el.getBoundingClientRect();
    const lineCount =
      Number.isFinite(lineHeight) && lineHeight > 0
        ? Math.round(rect.height / lineHeight)
        : el.getClientRects().length;

    return {
      lineCount,
      width: rect.width,
      fontSize: Number.parseFloat(style.fontSize),
    };
  });

  expect(metrics.width).toBeGreaterThan(320);
  expect(metrics.fontSize).toBeGreaterThan(40);
  expect(metrics.lineCount).toBeLessThanOrEqual(3);
}

async function expectModeButtonState(active: Locator, inactive: Locator) {
  const [activeBg, inactiveBg] = await Promise.all([
    active.evaluate((node) => window.getComputedStyle(node as HTMLElement).backgroundColor),
    inactive.evaluate((node) => window.getComputedStyle(node as HTMLElement).backgroundColor),
  ]);

  expect(activeBg).not.toBe("rgba(0, 0, 0, 0)");
  expect(activeBg).not.toBe(inactiveBg);
}

test.describe("PlotLot design system", () => {
  test("lookup welcome screen matches the current editorial hero contract", async ({ page }, testInfo) => {
    await gotoWelcome(page);

    await expect(page.getByRole("button", { name: "Toggle dark mode" })).toBeVisible();
    await expect(page.getByText("Hi there", { exact: true })).toBeVisible();

    const heading = page.getByRole("heading", { name: "Analyze any property in the US" });
    await expectCompactHero(heading);
    await expect(page.getByText(/Zoning, density, comps, pro forma, and development potential/)).toBeVisible();

    const input = page.getByPlaceholder("Enter a property address...");
    await expect(input).toBeVisible();
    await expect(page.getByRole("button", { name: "Send message" })).toBeDisabled();

    for (const chip of ["Miramar, FL", "Miami Gardens, FL", "Boca Raton, FL"]) {
      await expect(page.getByRole("button", { name: chip })).toBeVisible();
    }

    await expect(page.getByText(/PlotLot analyzes zoning, density, comps/i)).toBeVisible();
    await page.screenshot({ path: testInfo.outputPath("ds-01-lookup-welcome.png"), fullPage: true });
  });

  test("agent welcome swaps into the tool-first surface without breaking the hero", async ({ page }, testInfo) => {
    await gotoWelcome(page);

    const lookupButton = page.getByRole("button", { name: "Lookup" });
    const agentButton = page.getByRole("button", { name: "Agent" });
    await agentButton.click();

    await expectCompactHero(
      page.getByRole("heading", { name: "Ask anything about zoning & land" }),
    );
    await expect(page.getByPlaceholder("Ask about zoning, density, or property data...")).toBeVisible();

    for (const label of [
      "Analyze Property",
      "Generate LOI",
      "Search Comps",
      "Run Pro Forma",
      "Search Properties",
    ]) {
      await expect(page.getByRole("button", { name: new RegExp(label) })).toBeVisible();
    }

    await expect(page.getByText("Analyze a property first").first()).toBeVisible();
    await expectModeButtonState(agentButton, lookupButton);
    await page.screenshot({ path: testInfo.outputPath("ds-02-agent-welcome.png"), fullPage: true });
  });

  test("theme toggle persists while switching between lookup and agent modes", async ({ page }) => {
    await gotoWelcome(page);

    const html = page.locator("html");
    await expect(html).not.toHaveClass(/dark/);

    await page.getByRole("button", { name: "Toggle dark mode" }).click();
    await expect(html).toHaveClass(/dark/);

    await page.getByRole("button", { name: "Agent" }).click();
    await expect(page.getByRole("heading", { name: "Ask anything about zoning & land" })).toBeVisible();
    await expect(html).toHaveClass(/dark/);

    await page.getByRole("button", { name: "Lookup" }).click();
    await expect(page.getByRole("heading", { name: "Analyze any property in the US" })).toBeVisible();
    await expect(html).toHaveClass(/dark/);
  });

  test("lookup address submission starts analysis directly without a deal gate", async ({ page }) => {
    await gotoWelcome(page);

    await stubAnalyzeStream(page);

    await page.getByPlaceholder("Enter a property address...").fill("18901 NW 27th Ave, Miami Gardens, FL 33056");
    await page.getByRole("button", { name: "Send message" }).click();

    await expect(page.getByTestId("deal-type-selector")).toHaveCount(0);
    await expect(page.getByText("What type of deal are you evaluating?")).toHaveCount(0);
    await expect(page.getByTestId("pipeline-stepper")).toBeVisible();
    await expect(page.getByTestId("pipeline-step-geocoding")).toBeVisible();
  });

  test("lookup mode rejects non-address prompts instead of drifting into chat", async ({ page }) => {
    await gotoWelcome(page);

    await page.getByPlaceholder("Enter a property address...").fill("What can I build in Houston?");
    await page.getByRole("button", { name: "Send message" }).click();

    await expect(
      page.getByText("Please enter a street address to run a lookup analysis"),
    ).toBeVisible();
    await expect(page.getByTestId("deal-type-selector")).toHaveCount(0);
  });
});
