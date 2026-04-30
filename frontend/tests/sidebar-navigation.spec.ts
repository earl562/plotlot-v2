import { test, expect } from "@playwright/test";

test.describe("sidebar navigation", () => {
  test("sidebar items are clickable and switch between lookup and agent modes", async ({ page }) => {
    await page.goto("/");

    await expect(page.getByTestId("lookup-input")).toBeVisible();

    const harnessWorkspace = page.getByTestId("sidebar-nav-harness-workspace");
    await harnessWorkspace.click();
    await expect(page.getByTestId("agent-input")).toBeVisible();
    await expect(harnessWorkspace).toHaveAttribute("aria-current", "page");

    const siteFinder = page.getByTestId("sidebar-nav-site-finder");
    await siteFinder.click();
    await expect(page.getByTestId("lookup-input")).toBeVisible();
    await expect(siteFinder).toHaveAttribute("aria-current", "page");
  });
});
