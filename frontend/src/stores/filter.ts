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
    },

    setFilter(payload: {
      filterType: "alerts";
      filterName: alertFilterNameTypes;
      filterValue: alertFilterValues;
    }) {
      this.$state[payload.filterType][payload.filterName] = payload.filterValue;
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
