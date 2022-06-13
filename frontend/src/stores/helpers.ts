import { useAlertDispositionStore } from "./alertDisposition";
import { useEventVectorStore } from "./eventVector";
import { useAlertToolStore } from "./alertTool";
import { useAlertTypeStore } from "./alertType";
import { useAlertToolInstanceStore } from "./alertToolInstance";
import { useAlertTableStore } from "./alertTable";
import { useAuthStore } from "./auth";
import { useCurrentUserSettingsStore } from "./currentUserSettings";
import { useEventPreventionToolStore } from "./eventPreventionTool";
import { useEventRemediationStore } from "./eventRemediation";
import { useEventSeverityStore } from "./eventSeverity";
import { useEventStatusStore } from "./eventStatus";
import { useEventTableStore } from "./eventTable";
import { useEventTypeStore } from "./eventType";
import { useFilterStore } from "./filter";
import { useNodeDirectiveStore } from "./nodeDirective";
import { useNodeThreatStore } from "./nodeThreat";
import { useNodeThreatActorStore } from "./nodeThreatActor";
import { useNodeThreatTypeStore } from "./nodeThreatType";
import { useObservableTypeStore } from "./observableType";
import { useQueueStore } from "./queue";
import { useUserStore } from "./user";
import { dateParser } from "@/etc/helpers";

export async function populateCommonStores(): Promise<void> {
  const alertDispositionStore = useAlertDispositionStore();
  const alertTypeStore = useAlertTypeStore();
  const alertToolStore = useAlertToolStore();
  const alertToolInstanceStore = useAlertToolInstanceStore();
  const eventPreventionToolStore = useEventPreventionToolStore();
  const eventSeverityStore = useEventSeverityStore();
  const eventStatusStore = useEventStatusStore();
  const eventTypeStore = useEventTypeStore();
  const eventVectorStore = useEventVectorStore();
  const nodeDirectiveStore = useNodeDirectiveStore();
  const observableTypeStore = useObservableTypeStore();
  const queueStore = useQueueStore();
  const userStore = useUserStore();

  await Promise.all([
    alertDispositionStore.readAll(),
    alertTypeStore.readAll(),
    alertToolStore.readAll(),
    alertToolInstanceStore.readAll(),
    eventPreventionToolStore.readAll(),
    eventSeverityStore.readAll(),
    eventStatusStore.readAll(),
    eventTypeStore.readAll(),
    eventVectorStore.readAll(),
    nodeDirectiveStore.readAll(),
    observableTypeStore.readAll(),
    queueStore.readAll(),
    userStore.readAll(),
  ]).catch((error) => {
    throw error;
  });
}

export async function populateEventStores(): Promise<void> {
  const eventPreventionToolStore = useEventPreventionToolStore();
  const eventRemediationStore = useEventRemediationStore();
  const eventSeverityStore = useEventSeverityStore();
  const eventStatusStore = useEventStatusStore();
  const eventTypeStore = useEventTypeStore();
  const nodeThreatActorStore = useNodeThreatActorStore();
  const nodeThreatStore = useNodeThreatStore();
  const nodeThreatTypeStore = useNodeThreatTypeStore();
  const userStore = useUserStore();
  const eventVectorStore = useEventVectorStore();

  await Promise.all([
    eventPreventionToolStore.readAll(),
    eventSeverityStore.readAll(),
    eventRemediationStore.readAll(),
    eventStatusStore.readAll(),
    eventTypeStore.readAll(),
    nodeThreatActorStore.readAll(),
    nodeThreatStore.readAll(),
    nodeThreatTypeStore.readAll(),
    eventVectorStore.readAll(),
    userStore.readAll(),
  ]).catch((error) => {
    throw error;
  });
}

// Sets default user filters and currentUserSettings
export function setUserDefaults(nodeType = "all"): void {
  const authStore = useAuthStore();
  const filterStore = useFilterStore();
  const eventStatusStore = useEventStatusStore();
  const currentUserSettingsStore = useCurrentUserSettingsStore();

  if (!authStore.user) {
    return;
  }

  if (nodeType === "all" || nodeType === "events") {
    // Set default event queue
    currentUserSettingsStore.queues.events = authStore.user.defaultEventQueue;
    filterStore.setFilter({
      nodeType: "events",
      filterName: "queue",
      filterValue: currentUserSettingsStore.queues.events,
    });

    // Set default event status filter
    const openStatus = eventStatusStore.items.find((status) => {
      return status.value === "OPEN";
    });
    if (openStatus) {
      filterStore.setFilter({
        nodeType: "events",
        filterName: "status",
        filterValue: openStatus,
      });
    }
  }

  if (nodeType === "all" || nodeType === "alerts") {
    // Set default alert queue
    currentUserSettingsStore.queues.alerts = authStore.user.defaultAlertQueue;
    filterStore.setFilter({
      nodeType: "alerts",
      filterName: "queue",
      filterValue: currentUserSettingsStore.queues.alerts,
    });
  }
}

export function loadFiltersFromStorage(): void {
  const filterStore = useFilterStore();
  const alertTableStore = useAlertTableStore();
  const eventTableStore = useEventTableStore();
  filterStore.$state = JSON.parse(
    localStorage.getItem("aceFilters") || "{}",
    dateParser,
  );
  alertTableStore.stateFiltersLoaded = true;
  eventTableStore.stateFiltersLoaded = true;
}
