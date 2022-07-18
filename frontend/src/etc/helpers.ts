import {
  alertFilterParams,
  alertRead,
  alertSummary,
  alertTreeRead,
} from "@/models/alert";
import { genericQueueableObjectRead, propertyOption } from "@/models/base";
import { eventFilterParams } from "@/models/event";
import { metadataTagRead } from "@/models/metadataTag";
import { isValidDate, isObject, isValidDateString } from "@/etc/validators";
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

export const scrollTo = (id: string | null, animate = false) => {
  if (id) {
    const obj = document.getElementById(id);

    if (obj) {
      obj.scrollIntoView({ behavior: "smooth", block: "center" });

      if (animate) {
        obj.animate(
          [
            {
              backgroundColor: "yellow",
            },
          ],
          {
            duration: 300,
            iterations: 3,
          },
        );
      }
    }
  }
};

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

export function prettyPrintDateTime(
  datetime: string | Date | null,
  timezone?: string,
): string {
  if (!datetime) return "None";

  // Convert the datetime to a string if it is a Date object.
  if (datetime instanceof Date) {
    datetime = datetime.toISOString();
  }

  // If the datetime is not a valid date string, return it as-is.
  if (!isValidDateString(datetime)) {
    return datetime;
  }

  // Return the formatted datetime string according to the given timezone (or UTC).
  const tz = timezone || "UTC";
  return `${new Date(datetime).toLocaleString("en-US", {
    timeZone: tz,
  })} ${tz}`;
}

//https://stackoverflow.com/a/62447533
const snakeCase = (s: string) => {
  return s
    .replace(/\d+/g, " ")
    .split(/ |\B(?=[A-Z])/)
    .map((word: string) => word.toLowerCase())
    .join("_");
};

export function parseFilters(
  queryFilters: Record<string, string | string[]>,
  availableFilters: readonly propertyOption[],
): alertFilterParams | eventFilterParams {
  const parsedFilters: Record<
    string,
    {
      included: any[];
      notIncluded: any[];
      [key: string]: any[];
    }
  > = {};

  // parse each filter
  for (const filterName in queryFilters) {
    let list = "included";
    let parsedFilterName = filterName;
    // Convert to snakeCase so we can check for 'not' without accidentally matching filters that may start with 'not', ex. 'notableFeatures' :P
    if (snakeCase(filterName).startsWith("not_")) {
      list = "notIncluded"; // If the filter is a 'not' filter, we need to add it to the notIncluded array
      parsedFilterName = filterName.replace("not", ""); // Remove the 'not' from the filter name so we can use it as a key in the parsedFilters object
      parsedFilterName = `${parsedFilterName[0].toLowerCase()}${parsedFilterName.slice(
        1,
      )}`; // Then lowercase the first letter of the filter name
    }

    // first get the filter object so you can validate the filter exists and use its metadata
    let filterNameObject = availableFilters.find((filter) => {
      return filter.name === parsedFilterName;
    });
    filterNameObject = filterNameObject ? filterNameObject : undefined;

    // if the filter doesn't exist, skip it
    if (!filterNameObject) {
      continue;
    }

    const filterValueUnparsedArray = Array.isArray(queryFilters[filterName])
      ? queryFilters[filterName]
      : [queryFilters[filterName]];

    for (const value of filterValueUnparsedArray) {
      // format filterValue for GUI if method available
      const filterValue = filterNameObject.parseStringRepr
        ? filterNameObject.parseStringRepr(value as any)
        : value;

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
          if (store && Array.isArray(filterValue)) {
            for (const value of filterValue) {
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
          filterValueParsed = filterValueParsed.length
            ? filterValueParsed
            : null;
          break;

        case inputTypes.CHIPS:
          // array of strings, handled in parseFormattedFilterString
          filterValueParsed = filterValue;
          break;

        case inputTypes.SELECT:
          // look item up in store
          if (store) {
            filterValueParsed = store.allItems.find(
              (element: Record<string, unknown>) => {
                return element[filterValueProperty] === filterValue;
              },
            );
          }

          if (
            !filterValueParsed &&
            filterNameObject.nullOptions?.nullableFilter &&
            filterValue ===
              filterNameObject.nullOptions?.nullOption[filterValueProperty]
          ) {
            filterValueParsed = filterNameObject.nullOptions?.nullOption;
          }
          break;

        case inputTypes.DATE:
          // Date string, handled in parseFormattedFilterString
          filterValueParsed = isValidDate(filterValue) ? filterValue : null;
          break;

        case inputTypes.INPUT_TEXT:
          // does not need parsing
          filterValueParsed = filterValue;
          break;

        case inputTypes.CATEGORIZED_VALUE:
          // look up category value in store, sub-value stays untouched
          if (store && isObject(filterValue)) {
            const unparsedCategory = filterValue.category;
            const category = store.allItems.find(
              (element: Record<string, unknown>) => {
                return element[filterValueProperty] === unparsedCategory;
              },
            );
            filterValueParsed = {
              category: category,
              value: filterValue.value,
            };
          }
          break;

        // Unsupported filter types will be ignored
        default:
          console.log(
            `Unsupported filter type found: ${filterNameObject.type}`,
          );
          continue;
      }

      // If filter value was successfully parsed add it to the new filter object
      if (filterValueParsed) {
        if (!parsedFilters[parsedFilterName]) {
          parsedFilters[parsedFilterName] = {
            included: [],
            notIncluded: [],
          };
        }
        parsedFilters[parsedFilterName][list].push(filterValueParsed);
      }
    }
  }
  return parsedFilters;
}

export function formatObjectFiltersForAPI(
  availableFilters: readonly propertyOption[],
  params: alertFilterParams | eventFilterParams,
): Record<string, string> | Record<string, number> {
  const formattedParams = {} as alertFilterParams;
  for (const param in params) {
    const paramValue = params[param] as {
      included: any[];
      notIncluded: any[];
      [key: string]: any[];
    };

    //  check if the given param is specific to object and not pageOptionParams, i.e. disposition
    const filterType = availableFilters.find((filter) => {
      return filter.name === param;
    });

    // if so, check if the params values need to be formatted, and replace with the newly formatted values
    if (filterType) {
      for (const listType of ["included", "notIncluded"]) {
        let formattedParamValue = paramValue[listType];

        // First check if there is a method provided to get string representation
        if (filterType.stringRepr) {
          formattedParamValue = formattedParamValue.map(
            filterType.stringRepr,
          ) as never;
          // Otherwise check if the param's value is a specific property
        } else if (
          filterType.valueProperty &&
          Array.isArray(formattedParamValue) &&
          formattedParamValue.every(isObject)
        ) {
          formattedParamValue = formattedParamValue.map(
            (v: any) => v[filterType.valueProperty as string],
          );
        }

        if (formattedParamValue.length) {
          if (listType === "included") {
            formattedParams[param] = formattedParamValue;
          } else {
            formattedParams[
              `not${param.charAt(0).toUpperCase()}${param.slice(1)}`
            ] = formattedParamValue;
          }
        }
      }
    } else {
      formattedParams[param] = paramValue;
    }
  }
  return formattedParams;
}

export function getAllAlertTags(
  alert: alertRead | alertSummary | alertTreeRead,
): Array<metadataTagRead> {
  const allTags = alert.tags
    .concat(alert.childAnalysisTags)
    .concat(alert.childTags);

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
    childTags: alert.childTags,
    comments: alert.comments,
    description: alert.description ? alert.description : "",
    disposition: alert.disposition ? alert.disposition.value : "OPEN",
    dispositionTime: alert.dispositionTime
      ? prettyPrintDateTime(alert.dispositionTime)
      : null,
    dispositionUser: alert.dispositionUser
      ? alert.dispositionUser.displayName
      : "None",
    dispositionWithUserAndTime:
      alert.disposition && alert.dispositionUser && alert.dispositionTime
        ? `${alert.disposition.value} by ${
            alert.dispositionUser.displayName
          } @ ${prettyPrintDateTime(alert.dispositionTime)}`
        : "OPEN",
    eventTime: prettyPrintDateTime(alert.eventTime),
    eventUuid: alert.eventUuid ? alert.eventUuid : "None",
    insertTime: prettyPrintDateTime(alert.insertTime),
    name: alert.name,
    owner: alert.owner ? alert.owner.displayName : "None",
    ownershipTime: alert.ownershipTime
      ? prettyPrintDateTime(alert.ownershipTime)
      : null,
    ownerWithTime:
      alert.owner && alert.ownershipTime
        ? `${alert.owner.displayName} @ ${prettyPrintDateTime(
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

export function findClosestMatchingString(
  strings: string[],
  searchString: string,
): string | null {
  // Check if the searchString itself is in the list
  if (strings.includes(searchString)) {
    return searchString;
  }
  // Check if a substring of the searchString is in the list
  while (searchString.includes(" - ")) {
    if (strings.includes(searchString)) {
      return searchString;
    }
    const spliceIndex = searchString.lastIndexOf(" - ");
    searchString = searchString.slice(0, spliceIndex);
  }
  // Check if the 'smallest' substring of the searchString is in the list
  if (strings.includes(searchString)) {
    return searchString;
  }
  return null;
}
