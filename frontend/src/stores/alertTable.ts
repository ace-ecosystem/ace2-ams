import { defineStore } from "pinia";
import { alertFilterParams, alertRead, alertSummary } from "@/models/alert";
import { UUID } from "@/models/base";
import { Alert } from "@/services/api/alert";

export function parseAlertSummary(alert: alertRead): alertSummary {
  return {
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
    visibleQueriedAlerts: [] as alertRead[],

    // total number of alerts from all pages
    totalAlerts: 0,

    // whether the alert table should be reloaded
    requestReload: false,
  }),

  getters: {
    visibleQueriedAlertSummaries(): alertSummary[] {
      return this.visibleQueriedAlerts.map((x) => parseAlertSummary(x));
    },

    visibleQueriedAlertsUuids(): UUID[] {
      return this.visibleQueriedAlerts.map((x) => x.uuid);
    },

    visibleQueriedAlertById: (state) => {
      return (alertUuid: UUID) =>
        state.visibleQueriedAlerts.find((alert) => alert.uuid === alertUuid);
    },
  },

  actions: {
    async readPage(params: alertFilterParams) {
      await Alert.readPage(params)
        .then((page) => {
          this.visibleQueriedAlerts = page.items;
          this.totalAlerts = page.total;
        })
        .catch((error) => {
          throw error;
        });
    },
  },
});
