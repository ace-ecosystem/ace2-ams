import { setUserDefaults, loadFiltersFromStorage } from "@/stores/helpers";
import { beforeEach, expect } from "vitest";
import { useAlertTableStore } from "@/stores/alertTable";
import { useAuthStore } from "@/stores/auth";
import { useCurrentUserSettingsStore } from "@/stores/currentUserSettings";
import { useEventTableStore } from "@/stores/eventTable";
import { useFilterStore } from "@/stores/filter";
import { genericObjectReadFactory } from "@mocks/genericObject";
import { userReadFactory } from "@mocks/user";
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
    expect(currentUserSettingsStore.queues.events).to.equal(null);
    expect(currentUserSettingsStore.queues.alerts).to.equal(null);

    expect(filterStore.events).to.eql({});
    expect(filterStore.alerts).to.eql({});
  });

  it("will correctly set all user defaults when nodeType == 'all'", () => {
    authStore.user = userReadFactory({
      defaultAlertQueue: alertQueue,
      defaultEventQueue: eventQueue,
    });
    setUserDefaults();
    expect(currentUserSettingsStore.queues.events).to.eql(eventQueue);
    expect(currentUserSettingsStore.queues.alerts).to.eql(alertQueue);
    expect(filterStore.events).to.eql({
      queue: eventQueue,
    });
    expect(filterStore.alerts).to.eql({
      queue: alertQueue,
    });
  });
  it("will correctly set event user defaults when nodeType == 'events'", () => {
    authStore.user = userReadFactory({
      defaultAlertQueue: alertQueue,
      defaultEventQueue: eventQueue,
    });
    setUserDefaults("events");
    expect(currentUserSettingsStore.queues.events).to.eql(eventQueue);
    expect(currentUserSettingsStore.queues.alerts).to.equal(null);
    expect(filterStore.events).to.eql({
      queue: eventQueue,
    });
    expect(filterStore.alerts).to.eql({});
  });
  it("will correctly set alert user defaults when nodeType == 'alerts'", () => {
    authStore.user = userReadFactory({
      defaultAlertQueue: alertQueue,
      defaultEventQueue: eventQueue,
    });
    setUserDefaults("alerts");
    expect(currentUserSettingsStore.queues.events).to.equal(null);
    expect(currentUserSettingsStore.queues.alerts).to.eql(alertQueue);
    expect(filterStore.events).to.eql({});
    expect(filterStore.alerts).to.eql({
      queue: alertQueue,
    });
  });

  it("will not set any user defaults when nodeType is unknown", () => {
    setUserDefaults("unknown");
    expect(currentUserSettingsStore.queues.events).to.equal(null);
    expect(currentUserSettingsStore.queues.alerts).to.equal(null);

    expect(filterStore.events).to.eql({});
    expect(filterStore.alerts).to.eql({});
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

    expect(filterStore.$state).to.eql({
      alerts: {},
      events: {
        queue: { description: null, value: "external", uuid: "uuid1" },
      },
    });
    expect(alertTableStore.stateFiltersLoaded).to.equal(true);
    expect(eventTableStore.stateFiltersLoaded).to.equal(true);
  });
});
