import { useFilterStore } from "@/stores/filter";
import { useAuthStore } from "@/stores/auth";
import { useCurrentUserSettingsStore } from "./../stores/currentUserSettings";
import { useEventRemediationStore } from "./../stores/eventRemediation";
import {
  alertFilterParams,
  alertRead,
  alertSummary,
  alertTreeRead,
} from "@/models/alert";
import { genericObjectRead, propertyOption } from "@/models/base";
import { eventFilterParams } from "@/models/event";
import { nodeTagRead } from "@/models/nodeTag";
import { useAlertDispositionStore } from "@/stores/alertDisposition";
import { useAlertToolStore } from "@/stores/alertTool";
import { useAlertToolInstanceStore } from "@/stores/alertToolInstance";
import { useAlertTypeStore } from "@/stores/alertType";
import { useEventPreventionToolStore } from "@/stores/eventPreventionTool";
import { useEventRiskLevelStore } from "@/stores/eventRiskLevel";
import { useEventStatusStore } from "@/stores/eventStatus";
import { useEventTypeStore } from "@/stores/eventType";
import { useNodeThreatStore } from "@/stores/nodeThreat";
import { useNodeThreatActorStore } from "@/stores/nodeThreatActor";
import { useNodeThreatTypeStore } from "@/stores/nodeThreatType";
import { useEventVectorStore } from "@/stores/eventVector";
import { useNodeDirectiveStore } from "@/stores/nodeDirective";
import { useObservableTypeStore } from "@/stores/observableType";
import { useQueueStore } from "@/stores/queue";
import { useUserStore } from "@/stores/user";
import { inputTypes } from "@/etc/constants/base";
import { isValidDate, isObject } from "@/etc/validators";
import { nodeThreatRead } from "@/models/nodeThreat";
import { useFilterStore } from "@/stores/filter";
import { useAlertTableStore } from "@/stores/alertTable";
import { useEventTableStore } from "@/stores/eventTable";

export const camelToSnakeCase = (str: string): string =>
  str.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);

export async function populateCommonStores(): Promise<void> {
  const alertDispositionStore = useAlertDispositionStore();
  const alertTypeStore = useAlertTypeStore();
  const alertToolStore = useAlertToolStore();
  const alertToolInstanceStore = useAlertToolInstanceStore();
  const eventPreventionToolStore = useEventPreventionToolStore();
  const eventRiskLevelStore = useEventRiskLevelStore();
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
    eventRiskLevelStore.readAll(),
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
  const eventRiskLevelStore = useEventRiskLevelStore();
  const eventStatusStore = useEventStatusStore();
  const eventTypeStore = useEventTypeStore();
  const nodeThreatActorStore = useNodeThreatActorStore();
  const nodeThreatStore = useNodeThreatStore();
  const nodeThreatTypeStore = useNodeThreatTypeStore();
  const userStore = useUserStore();
  const eventVectorStore = useEventVectorStore();

  await Promise.all([
    eventPreventionToolStore.readAll(),
    eventRiskLevelStore.readAll(),
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

// https://stackoverflow.com/a/33928558
export function copyToClipboard(text: string): void | boolean | string | null {
  if (
    document.queryCommandSupported &&
    document.queryCommandSupported("copy")
  ) {
    const textarea = document.createElement("textarea");
    textarea.textContent = text;
    textarea.style.position = "fixed"; // Prevent scrolling to bottom of page in Microsoft Edge.
    document.body.appendChild(textarea);
    textarea.select();
    try {
      return document.execCommand("copy"); // Security exception may be thrown by some browsers.
    } catch (ex) {
      console.warn("Copy to clipboard failed.", ex);
      return prompt("Copy to clipboard: Ctrl+C, Enter", text);
    } finally {
      document.body.removeChild(textarea);
    }
  }
}

// https://weblog.west-wind.com/posts/2014/jan/06/javascript-json-date-parsing-and-real-dates
export function dateParser(key: string, value: unknown): Date | unknown {
  const reISO =
    /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2}(?:\.\d*))(?:Z|(\+|-)([\d|:]*))?$/;
  const reMsAjax = /^\/Date\((d|-|.*)\)[/|\\]$/;

  if (typeof value === "string") {
    let a = reISO.exec(value);
    if (a) return new Date(value);
    a = reMsAjax.exec(value);
    if (a) {
      const b = a[1].split(/[-+,.]/);
      return new Date(b[0] ? +b[0] : 0 - +b[1]);
    }
  }
  return value;
}

export function parseFilters(
  queryFilters: Record<string, string>,
  availableFilters: readonly propertyOption[],
): alertFilterParams | eventFilterParams {
  const parsedFilters: Record<string, unknown> = {};

  // parse each filter
  for (const filterName in queryFilters) {
    // first get the filter object so you can validate the filter exists and use its metadata
    let filterNameObject = availableFilters.find((filter) => {
      return filter.name === filterName;
    });
    filterNameObject = filterNameObject ? filterNameObject : undefined;

    // if the filter doesn't exist, skip it
    if (!filterNameObject) {
      continue;
    }

    let filterValueUnparsed:
      | string
      | string[]
      | Date
      | { category: string; value: string } = queryFilters[filterName]; // the filter value from URL
    // format filterValueUnparsed for GUI if method available
    if (filterNameObject.parseStringRepr) {
      filterValueUnparsed = filterNameObject.parseStringRepr(
        queryFilters[filterName],
      );
    }

    // use correct property for determinining equality (default is 'value')
    const filterValueProperty = filterNameObject.valueProperty
      ? filterNameObject.valueProperty
      : "value";

    // load the filter options store if available
    let store = null; // store that may be used to find filter value object
    if (filterNameObject.store) {
      store = filterNameObject.store();
    }

    let filterValueParsed = null; // the target filter value, might be an Object, Array, Date, or string
    // based on the filter type, parse/format the filter value
    switch (filterNameObject.type) {
      case inputTypes.MULTISELECT:
        // look up each array item in store, add to filter value
        filterValueParsed = [];
        if (store && Array.isArray(filterValueUnparsed)) {
          for (const value of filterValueUnparsed) {
            const valueObject = store.allItems.find(
              (element: Record<string, unknown>) => {
                return element[filterValueProperty] === value;
              },
            );
            if (valueObject) {
              filterValueParsed.push(valueObject);
            }
          }
        }
        filterValueParsed = filterValueParsed.length ? filterValueParsed : null;
        break;

      case inputTypes.CHIPS:
        // array of strings, handled in parseFormattedFilterString
        filterValueParsed = filterValueUnparsed;
        break;

      case inputTypes.SELECT:
        // look item up in store
        if (store) {
          filterValueParsed = store.allItems.find(
            (element: Record<string, unknown>) => {
              return element[filterValueProperty] === filterValueUnparsed;
            },
          );
        }
        break;

      case inputTypes.DATE:
        // Date string, handled in parseFormattedFilterString
        filterValueParsed = isValidDate(filterValueUnparsed)
          ? filterValueUnparsed
          : null;
        break;

      case inputTypes.INPUT_TEXT:
        // does not need parsing
        filterValueParsed = filterValueUnparsed;
        break;

      case inputTypes.CATEGORIZED_VALUE:
        // look up category value in store, sub-value stays untouched
        if (store && isObject(filterValueUnparsed)) {
          const unparsedCategory = filterValueUnparsed.category;
          const category = store.allItems.find(
            (element: Record<string, unknown>) => {
              return element[filterValueProperty] === unparsedCategory;
            },
          );
          filterValueParsed = {
            category: category,
            value: filterValueUnparsed.value,
          };
        }
        break;

      // Unsupported filter types will be ignored
      default:
        console.log(`Unsupported filter type found: ${filterNameObject.type}`);
        continue;
    }

    // If filter value was successfully parsed add it to the new filter object
    if (filterValueParsed) {
      parsedFilters[filterName] = filterValueParsed;
    }
  }

  return parsedFilters;
}

export function formatNodeFiltersForAPI(
  availableFilters: readonly propertyOption[],
  params: alertFilterParams | eventFilterParams,
): Record<string, string> | Record<string, number> {
  const formattedParams = {} as alertFilterParams;
  for (const param in params) {
    let paramValue = params[param] as any;

    //  check if the given param is specific to node and not pageOptionParams, i.e. disposition
    const filterType = availableFilters.find((filter) => {
      return filter.name === param;
    });

    // if so, check if the param's value needs to be formatted, and replace with the newly formatted val
    if (filterType) {
      // First check if there is a method provided to get string representation
      if (filterType.stringRepr) {
        paramValue = filterType.stringRepr(paramValue) as never;
        // Otherwise check if the param's value is a specific property
      } else if (filterType.valueProperty && isObject(paramValue)) {
        paramValue = paramValue[filterType.valueProperty];
      }
    }

    formattedParams[param] = paramValue;
  }
  return formattedParams;
}

export function getAllAlertTags(
  alert: alertRead | alertTreeRead,
): Array<nodeTagRead> {
  const allTags = alert.tags.concat(alert.childTags);

  // Return a sorted and deduplicated list of the tags based on the tag UUID.
  return [...new Map(allTags.map((v) => [v.uuid, v])).values()].sort((a, b) =>
    a.value > b.value ? 1 : -1,
  );
}

export function getAlertLink(alert: alertRead): string {
  return "/alert/" + alert.uuid;
}

export function parseAlertSummary(alert: alertRead): alertSummary {
  return {
    childTags: alert.childTags,
    comments: alert.comments,
    description: alert.description ? alert.description : "",
    disposition: alert.disposition ? alert.disposition.value : "OPEN",
    dispositionTime: alert.dispositionTime
      ? new Date(alert.dispositionTime)
      : null,
    dispositionUser: alert.dispositionUser
      ? alert.dispositionUser.displayName
      : "None",
    eventTime: new Date(alert.eventTime),
    eventUuid: alert.eventUuid ? alert.eventUuid : "None",
    insertTime: new Date(alert.insertTime),
    name: alert.name,
    owner: alert.owner ? alert.owner.displayName : "None",
    queue: alert.queue.value,
    tags: alert.tags,
    tool: alert.tool ? alert.tool.value : "None",
    toolInstance: alert.toolInstance ? alert.toolInstance.value : "None",
    type: alert.type.value,
    uuid: alert.uuid,
  };
}

export function groupItemsByQueue<T extends genericObjectRead>(
  arr: T[],
): Record<string, T[]> {
  const itemsByQueue: Record<string, T[]> = {};
  for (const item of arr) {
    if (item.queues) {
      for (const queue of item.queues) {
        if (queue.value in itemsByQueue) {
          itemsByQueue[queue.value].push(item);
        } else {
          itemsByQueue[queue.value] = [item];
        }
      }
    }
  }
  return itemsByQueue;
}
