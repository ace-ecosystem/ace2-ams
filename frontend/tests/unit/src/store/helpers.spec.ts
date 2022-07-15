import { createTestingPinia } from "@pinia/testing";
import { describe, it, beforeEach, expect, vi } from "vitest";
import { useAlertDispositionStore } from "@/stores/alertDisposition";
import { useAlertTableStore } from "@/stores/alertTable";
import { useAlertToolInstanceStore } from "@/stores/alertToolInstance";
import { useAlertToolStore } from "@/stores/alertTool";
import { useAlertTypeStore } from "@/stores/alertType";
import { useAuthStore } from "@/stores/auth";
import { useCurrentUserSettingsStore } from "@/stores/currentUserSettings";
import { useEventPreventionToolStore } from "@/stores/eventPreventionTool";
import { useEventSeverityStore } from "@/stores/eventSeverity";
import { useEventStatusStore } from "@/stores/eventStatus";
import { useEventTableStore } from "@/stores/eventTable";
import { useEventTypeStore } from "@/stores/eventType";
import { useEventVectorStore } from "@/stores/eventVector";
import { useFilterStore } from "@/stores/filter";
import { useMetadataDirectiveStore } from "@/stores/metadataDirective";
import { useObservableTypeStore } from "@/stores/observableType";
import { useQueueStore } from "@/stores/queue";
import { userReadFactory } from "@mocks/user";
import { useUserStore } from "@/stores/user";
import {
  setUserDefaults,
  loadFiltersFromStorage,
  populateCommonStores,
  populateEventStores,
} from "@/stores/helpers";
import {
  genericObjectReadFactory,
  queueableObjectReadFactory,
} from "@mocks/genericObject";
import { useEventRemediationStore } from "@/stores/eventRemediation";
import { useThreatStore } from "@/stores/threat";
import { useThreatActorStore } from "@/stores/threatActor";
import { useThreatTypeStore } from "@/stores/threatType";
import { User } from "@/services/api/user";
import { AlertDisposition } from "@/services/api/alertDisposition";
import { AlertTool } from "@/services/api/alertTool";
import { AlertToolInstance } from "@/services/api/alertToolInstance";
import { AlertType } from "@/services/api/alertType";
import { EventPreventionTool } from "@/services/api/eventPreventionTool";
import { EventRemediation } from "@/services/api/eventRemediation";
import { EventSeverity } from "@/services/api/eventSeverity";
import { EventStatus } from "@/services/api/eventStatus";
import { EventType } from "@/services/api/eventType";
import { EventVector } from "@/services/api/eventVector";
import { MetadataDirective } from "@/services/api/metadataDirective";
import { ObservableType } from "@/services/api/observableType";
import { Threat } from "@/services/api/threat";
import { ThreatActor } from "@/services/api/threatActor";
import { ThreatType } from "@/services/api/threatType";
import { queue } from "@/services/api/queue";

createTestingPinia({ createSpy: vi.fn, stubActions: false });

describe("populateCommonStores", () => {
  it("will call readAll for all the hardcoded 'common' stores on populateCommonStores", async () => {
    vi.spyOn(EventPreventionTool, "readAll").mockImplementationOnce(
      async () => {
        return [];
      },
    );
    vi.spyOn(EventRemediation, "readAll").mockImplementationOnce(async () => {
      return [];
    });
    vi.spyOn(EventSeverity, "readAll").mockImplementationOnce(async () => {
      return [];
    });
    vi.spyOn(EventStatus, "readAll").mockImplementationOnce(async () => {
      return [];
    });
    vi.spyOn(EventType, "readAll").mockImplementationOnce(async () => {
      return [];
    });
    vi.spyOn(EventVector, "readAll").mockImplementationOnce(async () => {
      return [];
    });
    vi.spyOn(Threat, "readAll").mockImplementationOnce(async () => {
      return [];
    });
    vi.spyOn(ThreatActor, "readAll").mockImplementationOnce(async () => {
      return [];
    });
    vi.spyOn(ThreatType, "readAll").mockImplementationOnce(async () => {
      return [];
    });
    vi.spyOn(ObservableType, "readAll").mockImplementationOnce(async () => {
      return [];
    });
    vi.spyOn(MetadataDirective, "readAll").mockImplementationOnce(async () => {
      return [];
    });
    vi.spyOn(AlertDisposition, "readAll").mockImplementationOnce(async () => {
      return [];
    });
    vi.spyOn(AlertType, "readAll").mockImplementationOnce(async () => {
      return [];
    });
    vi.spyOn(AlertTool, "readAll").mockImplementationOnce(async () => {
      return [];
    });
    vi.spyOn(AlertToolInstance, "readAll").mockImplementationOnce(async () => {
      return [];
    });
    vi.spyOn(queue, "readAll").mockImplementationOnce(async () => {
      return [];
    });
    vi.spyOn(User, "readAll").mockImplementationOnce(async () => {
      return [];
    });

    const alertDispositionStore = useAlertDispositionStore();
    const alertTypeStore = useAlertTypeStore();
    const alertToolStore = useAlertToolStore();
    const alertToolInstanceStore = useAlertToolInstanceStore();
    const eventPreventionToolStore = useEventPreventionToolStore();
    const eventSeverityStore = useEventSeverityStore();
    const eventStatusStore = useEventStatusStore();
    const eventTypeStore = useEventTypeStore();
    const eventVectorStore = useEventVectorStore();
    const metadataDirectiveStore = useMetadataDirectiveStore();
    const observableTypeStore = useObservableTypeStore();
    const queueStore = useQueueStore();
    const userStore = useUserStore();
    await populateCommonStores();
    expect(alertDispositionStore.readAll).toHaveBeenCalled();
    expect(alertTypeStore.readAll).toHaveBeenCalled();
    expect(alertToolStore.readAll).toHaveBeenCalled();
    expect(alertToolInstanceStore.readAll).toHaveBeenCalled();
    expect(eventPreventionToolStore.readAll).toHaveBeenCalled();
    expect(eventSeverityStore.readAll).toHaveBeenCalled();
    expect(eventStatusStore.readAll).toHaveBeenCalled();
    expect(eventTypeStore.readAll).toHaveBeenCalled();
    expect(eventVectorStore.readAll).toHaveBeenCalled();
    expect(metadataDirectiveStore.readAll).toHaveBeenCalled();
    expect(observableTypeStore.readAll).toHaveBeenCalled();
    expect(queueStore.readAll).toHaveBeenCalled();
    expect(userStore.readAll).toHaveBeenCalled();
  });
  it("will throw an error if any attempt to read from common stores fails", async () => {
    const spy = vi.spyOn(User, "readAll");
    spy.mockImplementationOnce(() => {
      throw new Error("populateCommonStores failed");
    });

    try {
      await populateCommonStores();
    } catch (e) {
      const error = e as Error;
      expect(error.message).toEqual("populateCommonStores failed");
    }
  });
});

describe("populateEventStores", () => {
  it("will call readAll for all the hardcoded 'common' stores on populateEventStores", async () => {
    vi.spyOn(EventPreventionTool, "readAll").mockImplementationOnce(
      async () => {
        return [];
      },
    );
    vi.spyOn(EventRemediation, "readAll").mockImplementationOnce(async () => {
      return [];
    });
    vi.spyOn(EventSeverity, "readAll").mockImplementationOnce(async () => {
      return [];
    });
    vi.spyOn(EventStatus, "readAll").mockImplementationOnce(async () => {
      return [];
    });
    vi.spyOn(EventType, "readAll").mockImplementationOnce(async () => {
      return [];
    });
    vi.spyOn(EventVector, "readAll").mockImplementationOnce(async () => {
      return [];
    });
    vi.spyOn(Threat, "readAll").mockImplementationOnce(async () => {
      return [];
    });
    vi.spyOn(ThreatActor, "readAll").mockImplementationOnce(async () => {
      return [];
    });
    vi.spyOn(ThreatType, "readAll").mockImplementationOnce(async () => {
      return [];
    });
    vi.spyOn(User, "readAll").mockImplementationOnce(async () => {
      return [];
    });

    const eventPreventionToolStore = useEventPreventionToolStore();
    const eventRemediationStore = useEventRemediationStore();
    const eventSeverityStore = useEventSeverityStore();
    const eventStatusStore = useEventStatusStore();
    const eventTypeStore = useEventTypeStore();
    const threatActorStore = useThreatActorStore();
    const threatStore = useThreatStore();
    const threatTypeStore = useThreatTypeStore();
    const userStore = useUserStore();
    const eventVectorStore = useEventVectorStore();
    await populateEventStores();
    expect(eventPreventionToolStore.readAll).toHaveBeenCalled();
    expect(eventSeverityStore.readAll).toHaveBeenCalled();
    expect(eventStatusStore.readAll).toHaveBeenCalled();
    expect(eventTypeStore.readAll).toHaveBeenCalled();
    expect(eventVectorStore.readAll).toHaveBeenCalled();
    expect(userStore.readAll).toHaveBeenCalled();
    expect(eventRemediationStore.readAll).toHaveBeenCalled();
    expect(threatActorStore.readAll).toHaveBeenCalled();
    expect(threatStore.readAll).toHaveBeenCalled();
    expect(threatTypeStore.readAll).toHaveBeenCalled();
  });
  it("will throw an error if any attempt to read from event stores fails", async () => {
    const spy = vi.spyOn(User, "readAll");
    spy.mockImplementationOnce(() => {
      throw new Error("populateEventStores failed");
    });

    try {
      await populateEventStores();
    } catch (e) {
      const error = e as Error;
      expect(error.message).toEqual("populateEventStores failed");
    }
  });
});

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
  it("correctly sets filters to default when aceFilters not in storage", () => {
    const filterStore = useFilterStore();
    const alertTableStore = useAlertTableStore();
    const eventTableStore = useEventTableStore();

    localStorage.removeItem("aceFilters");

    loadFiltersFromStorage();

    expect(filterStore.$state).toEqual({
      alerts: {},
      events: {},
    });
    expect(alertTableStore.stateFiltersLoaded).toStrictEqual(true);
    expect(eventTableStore.stateFiltersLoaded).toStrictEqual(true);
  });
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
