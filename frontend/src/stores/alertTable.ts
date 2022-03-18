import { defineStore } from "pinia";
import { alertFilterParams, alertRead, alertSummary } from "@/models/alert";
import { UUID } from "@/models/base";
import { Alert } from "@/services/api/alert";
import { camelToSnakeCase, parseAlertSummary } from "@/etc/helpers";

export const useAlertTableStore = defineStore({
  id: "alertTableStore",

  state: () => ({
    // all alerts returned from the current page using the current filters
    visibleQueriedItems: [] as alertRead[],

    // total number of alerts from all pages
    totalItems: 0,

    // current sort field
    sortField: "eventTime" as string | null,

    // current sort oder
    sortOrder: "desc" as string | null,

    // current page size
    pageSize: 10,

    // whether the alert table should be reloaded
    requestReload: false,

    // whether alert filters have been loaded from saved state
    stateFiltersLoaded: false,

    // whether alert filters have been loaded from route query
    routeFiltersLoaded: false,
  }),

  getters: {
    allFiltersLoaded(): boolean {
      return this.stateFiltersLoaded && this.routeFiltersLoaded;
    },

    visibleQueriedItemSummaries(): alertSummary[] {
      return this.visibleQueriedItems.map((x) => parseAlertSummary(x));
    },

    visibleQueriedItemsUuids(): UUID[] {
      return this.visibleQueriedItems.map((x) => x.uuid);
    },

    visibleQueriedItemById: (state) => {
      return (alertUuid: UUID) =>
        state.visibleQueriedItems.find((alert) => alert.uuid === alertUuid);
    },

    sortFilter: (state) => {
      if (state.sortField && state.sortOrder) {
        return `${camelToSnakeCase(state.sortField)}|${state.sortOrder}`;
      }
      return null;
    },
  },

  actions: {
    async readPage(params: alertFilterParams) {
      await Alert.readPage(params)
        .then((page) => {
          this.visibleQueriedItems = page.items;
          this.totalItems = page.total;
        })
        .catch((error) => {
          throw error;
        });
    },
    resetSort() {
      this.sortField = "eventTime";
      this.sortOrder = "desc";
    },
  },
});
