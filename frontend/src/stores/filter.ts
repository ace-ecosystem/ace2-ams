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
      this.$state[payload.filterType] = payload.filters;
      localStorage.setItem("aceFilters", JSON.stringify(this.$state));
    },

    setFilter(payload: {
      filterType: "alerts" | "events";
      filterName: alertFilterNameTypes | eventFilterNameTypes;
      filterValue: alertFilterValues | eventFilterValues;
    }) {
      this.$state[payload.filterType][payload.filterName] = payload.filterValue;
      localStorage.setItem("aceFilters", JSON.stringify(this.$state));
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
