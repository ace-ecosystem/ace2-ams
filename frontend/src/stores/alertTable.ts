import { defineStore } from "pinia";
import { alertFilterParams, alertRead, alertSummary } from "@/models/alert";
import { UUID } from "@/models/base";
import { Alert } from "@/services/api/alert";
import { camelToSnakeCase } from "@/etc/helpers";

export function parseAlertSummary(alert: alertRead): alertSummary {
  return {
    childTags: alert.childTags,
    comments: alert.comments,
    description: alert.description ? alert.description : "",
    disposition: alert.disposition ? alert.disposition.value : "OPEN",
    dispositionTime: alert.dispositionTime ? alert.dispositionTime : null,
    dispositionUser: alert.dispositionUser
      ? alert.dispositionUser.displayName
      : "None",
    eventTime: alert.eventTime,
    insertTime: alert.insertTime,
    name: alert.name,
    owner: alert.owner ? alert.owner.displayName : "None",
    queue: alert.queue.value,
    tags: alert.tags,
    tool: alert.tool ? alert.tool.value : "None",
    type: alert.type.value,
    uuid: alert.uuid,
  };
}

export const useAlertTableStore = defineStore({
  id: "alertTableStore",

  state: () => ({
    // all alerts returned from the current page using the current filters
    visibleQueriedItems: [] as alertRead[],

    // total number of alerts from all pages
    totalItems: 0,

    // whether the alert table should be reloaded
    requestReload: false,

    // current sort field
    sortField: "eventTime",

    // current sort oder
    sortOrder: "desc" as string | null,

    // current page size
    pageSize: 10,
  }),

  getters: {
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
