import { defineStore } from "pinia";
import {
  alertFilterParams,
  alertFilterValues,
  alertFilterNameTypes,
} from "@/models/alert";
import {
  eventFilterNameTypes,
  eventFilterParams,
  eventFilterValues,
} from "@/models/event";
import { isValidDate } from "@/etc/validators";

export function isEmpty(value: unknown): boolean {
  if (value === null) {
    return true;
  }
  if (isValidDate(value)) {
    return false;
  }
  if (Array.isArray(value)) {
    return value.length === 0;
  }
  if (typeof value === "object") {
    return Object.keys(value).length == 0;
  }
  return Boolean(!value);
}

export const useFilterStore = defineStore({
  id: "filterStore",

  state: () => ({
    alerts: {} as alertFilterParams,
    events: {} as eventFilterParams,
  }),

  actions: {
    bulkSetFilters(payload: {
      nodeType: "alerts" | "events";
      filters: alertFilterParams | eventFilterParams;
    }) {
      const nonEmptyFilters = {} as alertFilterParams | eventFilterParams;
      for (const [name, valueArray] of Object.entries(payload.filters)) {
        // Remove any falsy/empty values from the filter value array
        const valueArrayEmptiesRemoved = valueArray.filter(
          (value: unknown) => !isEmpty(value),
        );
        // If the value array is empty, skip it entirely
        if (valueArrayEmptiesRemoved.length) {
          nonEmptyFilters[name as string] = valueArrayEmptiesRemoved;
        }
      }

      this.$state[payload.nodeType] = nonEmptyFilters;
      localStorage.setItem("aceFilters", JSON.stringify(this.$state));
    },

    setFilter(payload: {
      nodeType: "alerts" | "events";
      filterName: alertFilterNameTypes | eventFilterNameTypes;
      filterValue: alertFilterValues | eventFilterValues;
    }) {
      // If the filter value is 'empty' (empty string or list), don't add it
      if (!isEmpty(payload.filterValue)) {
        // If there is already a value for this filter type, add it to the list
        if (this.$state[payload.nodeType][payload.filterName]) {
          // If the value is already in the list, don't add it again
          if (
            !this.$state[payload.nodeType][payload.filterName].includes(
              payload.filterValue,
            )
          ) {
            this.$state[payload.nodeType][payload.filterName].push(
              payload.filterValue,
            );
          }
        } else {
          // Otherwise, create a new list with the value
          this.$state[payload.nodeType][payload.filterName] = [
            payload.filterValue,
          ];
        }
        // Update the local storage with the new filters
        localStorage.setItem("aceFilters", JSON.stringify(this.$state));
      }
    },

    unsetFilter(payload: {
      nodeType: "alerts" | "events";
      filterName: alertFilterNameTypes | eventFilterNameTypes;
    }) {
      delete this.$state[payload.nodeType][payload.filterName];
      localStorage.setItem("aceFilters", JSON.stringify(this.$state));
    },

    unsetFilterValue(payload: {
      nodeType: "alerts" | "events";
      filterName: alertFilterNameTypes | eventFilterNameTypes;
      filterValue: alertFilterValues | eventFilterValues;
    }) {
      // Remove the given filterValue from the list of values for this filter type
      this.$state[payload.nodeType][payload.filterName] = this.$state[
        payload.nodeType
      ][payload.filterName].filter(
        (v: alertFilterValues | eventFilterValues) => v !== payload.filterValue,
      );

      // If the list of values for this filter type is empty, remove the filter type entirely
      if (this.$state[payload.nodeType][payload.filterName].length === 0) {
        delete this.$state[payload.nodeType][payload.filterName];
      }

      // Update the local storage with the updated filters
      localStorage.setItem("aceFilters", JSON.stringify(this.$state));
    },

    clearAll(payload: { nodeType: "alerts" | "events" }) {
      this.$state[payload.nodeType] = {};
      localStorage.setItem("aceFilters", JSON.stringify(this.$state));
    },
  },
});
