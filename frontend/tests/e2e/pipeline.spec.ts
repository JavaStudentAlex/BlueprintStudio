import { test, expect } from "@playwright/test";

/**
 * End-to-end pipeline test.
 *
 * Run after `make up` (frontend on :3000, backend on :8000). Verifies:
 *  - onboarding can enter the current app shell
 *  - the active chat panel renders
 *  - sending a message produces the deterministic offline assistant reply
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

test("pipeline: load demo, send message, get reply", async ({
  page,
}) => {
  await page.goto("/");

  await page.getByTestId("button-load-demo").click();
  await expect(page.getByTestId("app-shell")).toBeVisible({ timeout: 10_000 });
  await expect(page.getByTestId("chat-panel")).toBeVisible();

  const composer = page.getByLabel("Message");
  await expect(composer).toBeVisible();

  const probe = `playwright-marker-${Date.now()}`;
  await composer.fill(probe);
  await composer.press("Enter");

  // The user message appears immediately.
  await expect(page.getByText(probe)).toBeVisible();

  // The assistant message is rendered (may or may not contain the marker text).
  const assistant = page.locator("[data-role='assistant']").last();
  await expect(assistant).toBeVisible({ timeout: 10_000 });
  await expect(assistant).toContainText("bob-foundation");
});
