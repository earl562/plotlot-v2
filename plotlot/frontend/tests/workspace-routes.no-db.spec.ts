import { test, expect } from "@playwright/test";

test.describe("workspace route scaffolds", () => {
  test("projects routes render", async ({ page }) => {
    await page.goto("/projects");
    await expect(page.getByRole("heading", { name: "Projects" })).toBeVisible();

    await page.goto("/projects/project_1");
    await expect(page.getByRole("heading", { name: "Project" })).toBeVisible();

    await page.goto("/projects/project_1/sites/site_1");
    await expect(page.getByRole("heading", { name: "Site" })).toBeVisible();

    await page.goto("/projects/project_1/sites/site_1/analyses/analysis_1");
    await expect(page.getByRole("heading", { name: "Analysis" })).toBeVisible();
  });
});
