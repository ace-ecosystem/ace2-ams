import { defineStore } from "pinia";
import {
  alertFilterParams,
  alertFilterValues,
  alertFilterNameTypes,
} from "@/models/alert";

export function isEmpty(value: unknown): boolean {
  if (value === null) {
    return true;
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
  }),

  actions: {
    bulkSetFilters(payload: {
      filterType: "alerts";
      filters: alertFilterParams;
    }) {
      const nonEmptyFilters = Object.fromEntries(
        Object.entries(payload.filters).filter(([_, v]) => !isEmpty(v)),
      );
      this.$state[payload.filterType] = nonEmptyFilters;
    },

    setFilter(payload: {
      filterType: "alerts";
      filterName: alertFilterNameTypes;
      filterValue: alertFilterValues;
    }) {
      if (!isEmpty(payload.filterValue)) {
        this.$state[payload.filterType][payload.filterName] =
          payload.filterValue;
      }
    },

    unsetFilter(payload: {
      filterType: "alerts";
      filterName: alertFilterNameTypes;
    }) {
      delete this.$state[payload.filterType][payload.filterName];
    },

    clearAll(payload: { filterType: "alerts" }) {
      this.$state[payload.filterType] = {};
    },
  },
});
