import { defineStore } from "pinia";
import {
  alertFilterParams,
  alertRead,
  alertSummary,
  alertUpdate,
} from "@/models/alert";
import { UUID } from "@/models/base";
import { Alert } from "@/services/api/alert";

export function parseAlertSummary(alert: alertRead): alertSummary {
  return {
    comments: alert.comments ? alert.comments : [],
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
    queue: alert.queue ? alert.queue.value : "None",
    tags: alert.tags ? alert.tags : [],
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
  }),

  getters: {
    visibleQueriedAlertSummaries(): alertSummary[] {
      return this.visibleQueriedAlerts.map((x) => parseAlertSummary(x));
    },

    visibleQueriedAlertsUuids(): UUID[] {
      return this.visibleQueriedAlerts.map((x) => x.uuid);
    },
  },

  actions: {
    async readPage(params: alertFilterParams) {
      await Alert.readPage(params)
        .then((page) => {
          this.$state.visibleQueriedAlerts = page.items;
          this.$state.totalAlerts = page.total;
        })
        .catch((error) => {
          throw error;
        });
    },

    async update(uuid: UUID, data: alertUpdate) {
      // once we get around to updating alerts, we will need to update the base api service to have a
      // 'getAfterUpdate' option like there is for 'create'
      // then we can reset the open/queried alert(s)
      await Alert.update(uuid, data).catch((error) => {
        throw error;
      });
    },

    async updateMultiple(uuids: UUID[], data: alertUpdate) {
      const promises = [];
      for (let i = 0; i < uuids.length; i++) {
        promises.push(Alert.update(uuids[i], data));
      }

      // and then all of those requests are resolved here
      await Promise.all(promises).catch((error) => {
        throw error;
      });

      // reason enough to have an updateMultiple in api?
    },
  },
});
