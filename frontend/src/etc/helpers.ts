import {
  alertFilterParams,
  alertRead,
  alertSummary,
  alertTreeRead,
} from "@/models/alert";
import { genericQueueableObjectRead, propertyOption } from "@/models/base";
import { eventFilterParams } from "@/models/event";
import { metadataTagRead } from "@/models/metadataTag";
import { isValidDate, isObject } from "@/etc/validators";
import { inputTypes } from "@/etc/constants/base";

export const camelToSnakeCase = (str: string): string =>
  str.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);

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

export function prettyPrintDateString(
  dateString: string,
  timezone?: string,
): string {
  const tz = timezone || "UTC";
  return `${new Date(dateString).toLocaleString("en-US", {
    timeZone: tz,
  })} ${tz}`;
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
    let paramValue = params[param] as unknown;

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
  alert: alertRead | alertSummary | alertTreeRead,
): Array<metadataTagRead> {
  const allTags = alert.tags
    .concat(alert.childAnalysisTags)
    .concat(alert.childPermanentTags);

  // Return a sorted and deduplicated list of the tags based on the tag value.
  return [...new Map(allTags.map((v) => [v.uuid, v])).values()].sort((a, b) =>
    a.value > b.value ? 1 : -1,
  );
}

export function getAlertLink(alert: alertRead | alertSummary): string {
  return "/alert/" + alert.uuid;
}

export function parseAlertSummary(alert: alertRead): alertSummary {
  return {
    childAnalysisTags: alert.childAnalysisTags,
    childPermanentTags: alert.childPermanentTags,
    comments: alert.comments,
    description: alert.description ? alert.description : "",
    disposition: alert.disposition ? alert.disposition.value : "OPEN",
    dispositionTime: alert.dispositionTime
      ? prettyPrintDateString(alert.dispositionTime)
      : null,
    dispositionUser: alert.dispositionUser
      ? alert.dispositionUser.displayName
      : "None",
    dispositionWithUserAndTime:
      alert.disposition && alert.dispositionUser && alert.dispositionTime
        ? `${alert.disposition.value} by ${
            alert.dispositionUser.displayName
          } @ ${new Date(alert.dispositionTime).toISOString()}`
        : "OPEN",
    eventTime: prettyPrintDateString(alert.eventTime),
    eventUuid: alert.eventUuid ? alert.eventUuid : "None",
    insertTime: prettyPrintDateString(alert.insertTime),
    name: alert.name,
    owner: alert.owner ? alert.owner.displayName : "None",
    ownershipTime: alert.ownershipTime
      ? prettyPrintDateString(alert.ownershipTime)
      : null,
    ownerWithTime:
      alert.owner && alert.ownershipTime
        ? `${alert.owner.displayName} @ ${prettyPrintDateString(
            alert.ownershipTime,
          )}`
        : "None",
    queue: alert.queue.value,
    tags: alert.tags,
    tool: alert.tool ? alert.tool.value : "None",
    toolInstance: alert.toolInstance ? alert.toolInstance.value : "None",
    type: alert.type.value,
    uuid: alert.uuid,
  };
}

export function groupItemsByQueue<T extends genericQueueableObjectRead>(
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
