import { defineStore } from "pinia";
import {
  alertFilterParams,
  alertFilterValues,
  alertFilterNameTypes,
} from "@/models/alert";

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
      this.$state[payload.filterType] = payload.filters;
      localStorage.setItem("aceFilters", JSON.stringify(this.$state));
    },

    setFilter(payload: {
      filterType: "alerts";
      filterName: alertFilterNameTypes;
      filterValue: alertFilterValues;
    }) {
      this.$state[payload.filterType][payload.filterName] = payload.filterValue;
      localStorage.setItem("aceFilters", JSON.stringify(this.$state));
    },

    unsetFilter(payload: {
      filterType: "alerts";
      filterName: alertFilterNameTypes;
    }) {
      delete this.$state[payload.filterType][payload.filterName];
      localStorage.setItem("aceFilters", JSON.stringify(this.$state));
    },

    clearAll(payload: { filterType: "alerts" }) {
      this.$state[payload.filterType] = {};
      localStorage.setItem("aceFilters", JSON.stringify(this.$state));
    },
  },
});
