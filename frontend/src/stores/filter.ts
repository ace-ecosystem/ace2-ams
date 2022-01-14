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
import { isValidDate } from "@/etc/helpers";

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
      filterType: "alerts" | "events";
      filters: alertFilterParams | eventFilterParams;
    }) {
      const nonEmptyFilters = Object.fromEntries(
        Object.entries(payload.filters).filter(([_, v]) => !isEmpty(v)),
      );
      this.$state[payload.filterType] = nonEmptyFilters;
      localStorage.setItem("aceFilters", JSON.stringify(this.$state));
    },

    setFilter(payload: {
      filterType: "alerts" | "events";
      filterName: alertFilterNameTypes | eventFilterNameTypes;
      filterValue: alertFilterValues | eventFilterValues;
    }) {
      if (!isEmpty(payload.filterValue)) {
        this.$state[payload.filterType][payload.filterName] =
          payload.filterValue;
        localStorage.setItem("aceFilters", JSON.stringify(this.$state));
      }
    },

    unsetFilter(payload: {
      filterType: "alerts" | "events";
      filterName: alertFilterNameTypes | eventFilterNameTypes;
    }) {
      delete this.$state[payload.filterType][payload.filterName];
      localStorage.setItem("aceFilters", JSON.stringify(this.$state));
    },

    clearAll(payload: { filterType: "alerts" | "events" }) {
      this.$state[payload.filterType] = {};
      localStorage.setItem("aceFilters", JSON.stringify(this.$state));
    },
  },
});
