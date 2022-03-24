import {
  setUserDefaults,
  loadFiltersFromStorage,
} from "../../../../src/stores/helpers";
import { beforeEach, expect } from "vitest";
import { useAlertTableStore } from "../../../../src/stores/alertTable";
import { useAuthStore } from "../../../../src/stores/auth";
import { useCurrentUserSettingsStore } from "../../../../src/stores/currentUserSettings";
import { useEventTableStore } from "../../../../src/stores/eventTable";
import { useFilterStore } from "../../../../src/stores/filter";
import { genericObjectReadFactory } from "../../../mocks/genericObject";
import { userReadFactory } from "../../../mocks/user";
import { vi, describe, it } from "vitest";
import { createTestingPinia } from "@pinia/testing";

createTestingPinia({ createSpy: vi.fn });

describe("setUserDefaults", () => {
  const authStore = useAuthStore();
  const filterStore = useFilterStore();
  const currentUserSettingsStore = useCurrentUserSettingsStore();

  const alertQueue = genericObjectReadFactory({ value: "alertQueue" });
  const eventQueue = genericObjectReadFactory({ value: "eventQueue" });

  beforeEach(() => {
    authStore.$reset();
    filterStore.$reset();
    currentUserSettingsStore.$reset();
  });

  it("will do nothing when there is no authStore user set", () => {
    setUserDefaults();
    expect(currentUserSettingsStore.queues.events).toBeNull();
    expect(currentUserSettingsStore.queues.alerts).toBeNull();

    expect(filterStore.events).toEqual({});
    expect(filterStore.alerts).toEqual({});
  });

  it("will correctly set all user defaults when nodeType == 'all'", () => {
    authStore.user = userReadFactory({
      defaultAlertQueue: alertQueue,
      defaultEventQueue: eventQueue,
    });
    setUserDefaults();
    expect(currentUserSettingsStore.queues.events).toEqual(eventQueue);
    expect(currentUserSettingsStore.queues.alerts).toEqual(alertQueue);
    expect(filterStore.events).toEqual({
      queue: eventQueue,
    });
    expect(filterStore.alerts).toEqual({
      queue: alertQueue,
    });
  });
  it("will correctly set event user defaults when nodeType == 'events'", () => {
    authStore.user = userReadFactory({
      defaultAlertQueue: alertQueue,
      defaultEventQueue: eventQueue,
    });
    setUserDefaults("events");
    expect(currentUserSettingsStore.queues.events).toEqual(eventQueue);
    expect(currentUserSettingsStore.queues.alerts).toBeNull();
    expect(filterStore.events).toEqual({
      queue: eventQueue,
    });
    expect(filterStore.alerts).toEqual({});
  });
  it("will correctly set alert user defaults when nodeType == 'alerts'", () => {
    authStore.user = userReadFactory({
      defaultAlertQueue: alertQueue,
      defaultEventQueue: eventQueue,
    });
    setUserDefaults("alerts");
    expect(currentUserSettingsStore.queues.events).toBeNull();
    expect(currentUserSettingsStore.queues.alerts).toEqual(alertQueue);
    expect(filterStore.events).toEqual({});
    expect(filterStore.alerts).toEqual({
      queue: alertQueue,
    });
  });

  it("will not set any user defaults when nodeType is unknown", () => {
    setUserDefaults("unknown");
    expect(currentUserSettingsStore.queues.events).toBeNull();
    expect(currentUserSettingsStore.queues.alerts).toBeNull();

    expect(filterStore.events).toEqual({});
    expect(filterStore.alerts).toEqual({});
  });
});

describe("loadFiltersFromStorage", () => {
  it("correctly sets filters from storage and sets table store stateFiltersLoaded values to true", () => {
    const filterStore = useFilterStore();
    const alertTableStore = useAlertTableStore();
    const eventTableStore = useEventTableStore();

    localStorage.setItem(
      "aceFilters",
      JSON.stringify({
        alerts: {},
        events: {
          queue: { description: null, value: "external", uuid: "uuid1" },
        },
      }),
    );

    loadFiltersFromStorage();

    expect(filterStore.$state).toStrictEqual({
      alerts: {},
      events: {
        queue: { description: null, value: "external", uuid: "uuid1" },
      },
    });
    expect(alertTableStore.stateFiltersLoaded).toBeTruthy();
    expect(eventTableStore.stateFiltersLoaded).toBeTruthy();
  });
});
