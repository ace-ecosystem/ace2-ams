import { useAlertDispositionStore } from "./alertDisposition";
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
import { useEventVectorStore } from "./eventVector";
import { useFilterStore } from "./filter";
import { useMetadataDirectiveStore } from "./metadataDirective";
import { useThreatStore } from "./threat";
import { useThreatActorStore } from "./threatActor";
import { useThreatTypeStore } from "./threatType";
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
  const metadataDirectiveStore = useMetadataDirectiveStore();
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
    metadataDirectiveStore.readAll(),
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
  const threatActorStore = useThreatActorStore();
  const threatStore = useThreatStore();
  const threatTypeStore = useThreatTypeStore();
  const userStore = useUserStore();
  const eventVectorStore = useEventVectorStore();

  await Promise.all([
    eventPreventionToolStore.readAll(),
    eventSeverityStore.readAll(),
    eventRemediationStore.readAll(),
    eventStatusStore.readAll(),
    eventTypeStore.readAll(),
    threatActorStore.readAll(),
    threatStore.readAll(),
    threatTypeStore.readAll(),
    eventVectorStore.readAll(),
    userStore.readAll(),
  ]).catch((error) => {
    throw error;
  });
}

// Sets default user filters and currentUserSettings
export function setUserDefaults(objectType = "all"): void {
  const authStore = useAuthStore();
  const filterStore = useFilterStore();
  const eventStatusStore = useEventStatusStore();
  const currentUserSettingsStore = useCurrentUserSettingsStore();

  if (!authStore.user) {
    return;
  }

  if (objectType === "all" || objectType === "events") {
    // Set default event queue
    currentUserSettingsStore.queues.events = authStore.user.defaultEventQueue;
    filterStore.setFilter({
      objectType: "events",
      filterName: "queue",
      filterValue: currentUserSettingsStore.queues.events,
      isIncluded: true,
    });

    // Set default event status filter
    const openStatus = eventStatusStore.items.find((status) => {
      return status.value === "OPEN";
    });
    if (openStatus) {
      filterStore.setFilter({
        objectType: "events",
        filterName: "status",
        filterValue: openStatus,
        isIncluded: true,
      });
    }
  }

  if (objectType === "all" || objectType === "alerts") {
    // Set default alert queue
    currentUserSettingsStore.queues.alerts = authStore.user.defaultAlertQueue;
    filterStore.setFilter({
      objectType: "alerts",
      filterName: "queue",
      filterValue: currentUserSettingsStore.queues.alerts,
      isIncluded: true,
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
