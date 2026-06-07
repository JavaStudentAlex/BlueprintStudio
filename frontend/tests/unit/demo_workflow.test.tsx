import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, beforeEach, vi } from "vitest";
import HomePage from "../../src/app/page";
import { useChatStore } from "../../src/lib/store";

describe("Frontend Golden Demo Workflow", () => {
  beforeEach(() => {
    // Reset store before each test
    useChatStore.getState().reset();
    useChatStore.setState({ onboardingStep: "step1" });
  });

  it("should bypass onboarding and show AppShell when 'Load demo' is clicked", () => {
    render(<HomePage />);

    // "Load demo" should be present in Step 1
    const loadDemoBtn = screen.getByTestId("button-load-demo");
    expect(loadDemoBtn).toBeDefined();

    fireEvent.click(loadDemoBtn);

    // Store state should be updated to ready and rooms
    expect(useChatStore.getState().onboardingStep).toBe("ready");
    expect(useChatStore.getState().activeView).toBe("rooms");

    // The component should rerender and show AppShell
    const appShell = screen.getByTestId("app-shell");
    expect(appShell).toBeDefined();

    // Verify 'rooms' view is rendered with the deterministic mock spaces
    expect(screen.getByText("Rooms (Spaces)")).toBeDefined();
    expect(screen.getByText("space-1")).toBeDefined();
  });

  it("should render valuation view when clicked in ActivityBar", () => {
    useChatStore.setState({ onboardingStep: "ready", activeView: "valuation" });
    render(<HomePage />);

    expect(screen.getByText("Property Valuation")).toBeDefined();
    expect(screen.getByText("$2,450,000")).toBeDefined(); // Mock valuation data
  });

  it("should render compliance view when clicked in ActivityBar", () => {
    useChatStore.setState({
      onboardingStep: "ready",
      activeView: "compliance",
    });
    render(<HomePage />);

    expect(screen.getByText("Compliance View")).toBeDefined();
    // Expected text from demo_compliance_report.json
    expect(screen.getByText(/Checks run: 8/i)).toBeDefined();
    expect(screen.getByText(/Failed/i)).toBeDefined();
  });
});
