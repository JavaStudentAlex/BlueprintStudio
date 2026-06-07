import { test, expect } from "@playwright/test";

/**
 * End-to-end golden demo test.
 *
 * Runs after `make up` (frontend on :3000, backend on :8000). Verifies:
 *  - "Load demo" works
 *  - Rooms, valuation, and compliance views render deterministic fixture data.
 *
 * Skipped automatically if the frontend is not reachable.
 */

const FRONTEND = process.env.PLAYWRIGHT_BASE_URL ?? "http://localhost:3000";

test.beforeEach(async ({ page }, testInfo) => {
  try {
    const r = await page.request.get(FRONTEND);
    if (!r.ok()) testInfo.skip();
  } catch {
    testInfo.skip();
  }
});

test("golden demo: load demo and verify views", async ({ page }) => {
  await page.goto("/");

  // Click "Load demo" in the Onboarding Wizard
  const loadDemoBtn = page.getByTestId("button-load-demo");
  await expect(loadDemoBtn).toBeVisible();
  await loadDemoBtn.click();

  // App shell should load and the default view is rooms
  await expect(page.getByTestId("app-shell")).toBeVisible({ timeout: 10000 });

  // Wait for the UI to settle and show Rooms view
  await expect(page.getByText("Rooms (Spaces)")).toBeVisible();

  // Switch to Valuation view via ActivityBar
  const valuationTab = page.getByRole("button", { name: "bob-valuation" });
  await valuationTab.click();

  await expect(page.getByText("Property Valuation")).toBeVisible();

  // Switch to Compliance view via ActivityBar
  const complianceTab = page.getByRole("button", { name: "bob-compliance" });
  await complianceTab.click();

  await expect(page.getByText("Compliance View")).toBeVisible();
});
