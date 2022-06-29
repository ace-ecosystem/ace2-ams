import { describe, it, beforeEach, expect, vi } from "vitest";
import { setUserDefaults, loadFiltersFromStorage } from "@/stores/helpers";
import { useAlertTableStore } from "@/stores/alertTable";
import { useAuthStore } from "@/stores/auth";
import { useCurrentUserSettingsStore } from "@/stores/currentUserSettings";
import { useEventTableStore } from "@/stores/eventTable";
import { useFilterStore } from "@/stores/filter";
import {
  genericObjectReadFactory,
  queueableObjectReadFactory,
} from "@mocks/genericObject";
import { userReadFactory } from "@mocks/user";
import { createTestingPinia } from "@pinia/testing";
import { useEventStatusStore } from "@/stores/eventStatus";

createTestingPinia({ createSpy: vi.fn, stubActions: false });

describe("setUserDefaults", () => {
  const authStore = useAuthStore();
  const filterStore = useFilterStore();
  const eventStatusStore = useEventStatusStore();
  const currentUserSettingsStore = useCurrentUserSettingsStore();

  const alertQueue = genericObjectReadFactory({ value: "alertQueue" });
  const eventQueue = genericObjectReadFactory({ value: "eventQueue" });
  const openStatus = queueableObjectReadFactory({ value: "OPEN" });
  const closedStatus = queueableObjectReadFactory({ value: "CLOSED" });

  beforeEach(() => {
    authStore.$reset();
    filterStore.$reset();
    currentUserSettingsStore.$reset();
  });

  it("will do nothing when there is no authStore user set", () => {
    setUserDefaults();
    expect(currentUserSettingsStore.queues.events).toStrictEqual(null);
    expect(currentUserSettingsStore.queues.alerts).toStrictEqual(null);

    expect(filterStore.events).toEqual({});
    expect(filterStore.alerts).toEqual({});
  });

  it("will correctly set all user defaults when objectType == 'all' and 'OPEN' event status is available", () => {
    authStore.user = userReadFactory({
      defaultAlertQueue: alertQueue,
      defaultEventQueue: eventQueue,
    });
    eventStatusStore.items = [openStatus, closedStatus];
    setUserDefaults();
    expect(currentUserSettingsStore.queues.events).toEqual(eventQueue);
    expect(currentUserSettingsStore.queues.alerts).toEqual(alertQueue);
    expect(filterStore.events).toEqual({
      queue: { included: [eventQueue], notIncluded: [] },
      status: { included: [openStatus], notIncluded: [] },
    });
    expect(filterStore.alerts).toEqual({
      queue: { included: [alertQueue], notIncluded: [] },
      owner: {
        included: [authStore.user, { displayName: "None", username: "none" }],
        notIncluded: [],
      },
      disposition: { included: [{ value: "None" }], notIncluded: [] },
    });
  });
  it("will correctly set all user defaults when objectType == 'all' and 'OPEN' event status is not available", () => {
    authStore.user = userReadFactory({
      defaultAlertQueue: alertQueue,
      defaultEventQueue: eventQueue,
    });
    eventStatusStore.items = [closedStatus];
    setUserDefaults();
    expect(currentUserSettingsStore.queues.events).toEqual(eventQueue);
    expect(currentUserSettingsStore.queues.alerts).toEqual(alertQueue);
    expect(filterStore.events).toEqual({
      queue: { included: [eventQueue], notIncluded: [] },
    });
    expect(filterStore.alerts).toEqual({
      queue: { included: [alertQueue], notIncluded: [] },
      owner: {
        included: [authStore.user, { displayName: "None", username: "none" }],
        notIncluded: [],
      },
      disposition: { included: [{ value: "None" }], notIncluded: [] },
    });
  });
  it("will correctly set event user defaults when objectType == 'events' and 'OPEN' event status is available", () => {
    authStore.user = userReadFactory({
      defaultAlertQueue: alertQueue,
      defaultEventQueue: eventQueue,
    });
    eventStatusStore.items = [openStatus, closedStatus];
    setUserDefaults("events");
    expect(currentUserSettingsStore.queues.events).toEqual(eventQueue);
    expect(currentUserSettingsStore.queues.alerts).toStrictEqual(null);
    expect(filterStore.events).toEqual({
      queue: { included: [eventQueue], notIncluded: [] },
      status: { included: [openStatus], notIncluded: [] },
    });
    expect(filterStore.alerts).toEqual({});
  });
  it("will correctly set event user defaults when objectType == 'events' and 'OPEN' event status is not available", () => {
    authStore.user = userReadFactory({
      defaultAlertQueue: alertQueue,
      defaultEventQueue: eventQueue,
    });
    eventStatusStore.items = [closedStatus];
    setUserDefaults("events");
    expect(currentUserSettingsStore.queues.events).toEqual(eventQueue);
    expect(currentUserSettingsStore.queues.alerts).toStrictEqual(null);
    expect(filterStore.events).toEqual({
      queue: { included: [eventQueue], notIncluded: [] },
    });
    expect(filterStore.alerts).toEqual({});
  });
  it("will correctly set alert user defaults when objectType == 'alerts'", () => {
    authStore.user = userReadFactory({
      defaultAlertQueue: alertQueue,
      defaultEventQueue: eventQueue,
    });
    setUserDefaults("alerts");
    expect(currentUserSettingsStore.queues.events).toStrictEqual(null);
    expect(currentUserSettingsStore.queues.alerts).toEqual(alertQueue);
    expect(filterStore.events).toEqual({});
    expect(filterStore.alerts).toEqual({
      queue: { included: [alertQueue], notIncluded: [] },
      owner: {
        included: [authStore.user, { displayName: "None", username: "none" }],
        notIncluded: [],
      },
      disposition: { included: [{ value: "None" }], notIncluded: [] },
    });
  });

  it("will not set any user defaults when objectType is unknown", () => {
    setUserDefaults("unknown");
    expect(currentUserSettingsStore.queues.events).toStrictEqual(null);
    expect(currentUserSettingsStore.queues.alerts).toStrictEqual(null);

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
          queue: {
            included: [{ description: null, value: "external", uuid: "uuid1" }],
            notIncluded: [],
          },
        },
      }),
    );

    loadFiltersFromStorage();

    expect(filterStore.$state).toEqual({
      alerts: {},
      events: {
        queue: {
          included: [{ description: null, value: "external", uuid: "uuid1" }],
          notIncluded: [],
        },
      },
    });
    expect(alertTableStore.stateFiltersLoaded).toStrictEqual(true);
    expect(eventTableStore.stateFiltersLoaded).toStrictEqual(true);
  });
});
