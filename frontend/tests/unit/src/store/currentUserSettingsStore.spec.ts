import { describe, it, beforeEach, expect } from "vitest";
import { useCurrentUserSettingsStore } from "@/stores/currentUserSettings";
import { userReadFactory } from "@mocks/user";
import { genericObjectReadFactory } from "@mocks/genericObject";
import { useAuthStore } from "@/stores/auth";
import { createCustomPinia } from "@tests/unitHelpers";

createCustomPinia();

const mockAlertQueue = genericObjectReadFactory({ value: "defaultAlertQueue" });
const mockEventQueue = genericObjectReadFactory({ value: "defaultEventQueue" });

const mockUser = userReadFactory({
  defaultAlertQueue: mockAlertQueue,
  defaultEventQueue: mockEventQueue,
});

describe("currentUserSettings Store", () => {
  const store = useCurrentUserSettingsStore();
  beforeEach(() => {
    store.$reset();
  });

  it("will set default queue values to null when there is no user set in the authStore", () => {
    expect(store.queues.alerts).toBeNull();
    expect(store.queues.events).toBeNull();
  });
  it("will set default queue values to null when there is no user set in the authStore", () => {
    const authStore = useAuthStore();
    authStore.user = mockUser;
    store.$reset();

    expect(store.queues.alerts).toEqual(mockAlertQueue);
    expect(store.queues.events).toEqual(mockEventQueue);
  });
});
