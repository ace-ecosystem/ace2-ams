import { defineStore } from "pinia";
import { alertFilters } from "@/etc/constants";
import {
  alertFilterParams,
  alertFilterValues,
  alertFilterNameTypes,
} from "@/models/alert";

function validFilter(filterType: "alerts", filterName: string): boolean {
  const filters = filterType == "alerts" ? alertFilters : [];
  const valid = filters.filter((filter) => filter.name == filterName);
  return valid.length ? true : false;
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
      for (const filter in payload.filters) {
        this.setFilter({
          filterType: payload.filterType,
          filterName: filter,
          filterValue: payload.filters[filter],
        });
      }
    },

    setFilter(payload: {
      filterType: "alerts";
      filterName: alertFilterNameTypes;
      filterValue: alertFilterValues;
    }) {
      if (validFilter(payload.filterType, payload.filterName)) {
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
      this.$state[payload.filterType] = {} as alertFilterParams;
    },
  },
});
