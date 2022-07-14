import { describe, it, beforeEach, expect } from "vitest";
import { useCurrentUserSettingsStore } from "@/stores/currentUserSettings";
import { userReadFactory } from "@mocks/user";
import { genericObjectReadFactory } from "@mocks/genericObject";
import { useAuthStore } from "@/stores/auth";
import { createCustomPinia } from "@tests/unitHelpers";

createCustomPinia();

const mockUser = userReadFactory({
  defaultAlertQueue: genericObjectReadFactory({ value: "defaultAlertQueue" }),
  defaultEventQueue: genericObjectReadFactory({ value: "defaultEventQueue" }),
});

describe("currentUserSettings Store", () => {
  it("will set default queue values to null when there is no user set in the authStore", () => {
    const store = useCurrentUserSettingsStore();
    expect(store.queues.alerts).toBeNull();
    expect(store.queues.events).toBeNull();
  });
  it("will set default queue values to null when there is no user set in the authStore", () => {
    const authStore = useAuthStore();
    authStore.user = mockUser;

    const store = useCurrentUserSettingsStore();
    expect(store.queues.alerts).toBeNull();
    expect(store.queues.events).toBeNull();
  });
});
