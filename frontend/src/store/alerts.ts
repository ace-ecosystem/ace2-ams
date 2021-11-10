import alertApi from "@/services/api/alerts";
import { CommitFunction } from "@/store/index";
import { alert, alertSummary } from "@/models/alert";
import { UUID } from "@/models/base";
import { getAllParams } from "@/models/api";

export function parseAlertSummary(alert: alert): alertSummary {
  return {
    comments: alert.comments ? alert.comments : [],
    description: alert.description ? alert.description : "",
    disposition: alert.disposition ? alert.disposition.value : "OPEN",
    dispositionTime: alert.dispositionTime ? alert.dispositionTime : null,
    dispositionUser: alert.dispositionUser
      ? alert.dispositionUser.value
      : "None",
    eventTime: alert.eventTime ? alert.eventTime : null,
    insertTime: alert.insertTime ? alert.insertTime : null,
    name: alert.name ? alert.name : "Unnamed",
    observables: alert.analysis ? alert.analysis.discoveredObservableUuids : [],
    owner: alert.owner ? alert.owner.value : "None",
    queue: alert.queue ? alert.queue.value : "None",
    tags: alert.tags ? alert.tags : [],
    tool: alert.tool ? alert.tool.value : "None",
    type: alert.type ? alert.type.value : "",
    uuid: alert.uuid,
  };
}

const store = {
  namespaced: true,

  state: {
    // currently opened alert
    openAlert: null,
    // all alerts returned from current page w/ current filter settings
    visibleQueriedAlerts: [],
    // total number of alerts of all pages
    totalAlerts: 0,
  },
  getters: {
    openAlert: (state: {
      openAlert: alertSummary | null;
      visibleQueriedAlerts: alertSummary[];
      totalAlerts: number;
    }): alertSummary | null => state.openAlert,
    visibleQueriedAlerts: (state: {
      openAlert: alertSummary | null;
      visibleQueriedAlerts: alertSummary[];
      totalAlerts: number;
    }): alertSummary[] => state.visibleQueriedAlerts,
    totalAlerts: (state: {
      openAlert: alertSummary | null;
      visibleQueriedAlerts: alertSummary[];
      totalAlerts: number;
    }): number => state.totalAlerts,
  },
  mutations: {
    SET_OPEN_ALERT(
      state: { openAlert: alertSummary | null },
      alert: alertSummary,
    ): void {
      state.openAlert = alert;
    },
    SET_VISIBLE_QUERIED_ALERTS(
      state: { visibleQueriedAlerts: alertSummary[] },
      alerts: alertSummary[],
    ): void {
      state.visibleQueriedAlerts = alerts;
    },
    SET_TOTAL_ALERTS(state: { totalAlerts: number }, total: number): void {
      state.totalAlerts = total;
    },
  },

  actions: {
    async createAlert(
      { commit }: CommitFunction,
      newAlert: any,
    ): Promise<void> {
      await alertApi
        .create(newAlert)
        .then((alert) => {
          commit("SET_OPEN_ALERT", alert);
        })
        .catch((error) => {
          throw error;
        });
    },
    async getSingle(
      { commit }: CommitFunction,
      alertUUID: UUID,
    ): Promise<void> {
      await alertApi
        .getSingle(alertUUID)
        .then((alert) => {
          commit("SET_OPEN_ALERT", alert);
        })
        .catch((error) => {
          throw error;
        });
    },
    async getAll(
      { commit }: CommitFunction,
      params: getAllParams,
    ): Promise<void> {
      await alertApi
        .getAll(params)
        .then((alerts) => {
          const parsedAlerts = [];
          for (const index in alerts.items) {
            const parsedAlert = parseAlertSummary(alerts.items[index]);
            parsedAlerts.push(parsedAlert);
          }
          commit("SET_VISIBLE_QUERIED_ALERTS", parsedAlerts);
          commit("SET_TOTAL_ALERTS", alerts.total);
          commit("SET_OPEN_ALERT", null);
        })
        .catch((error) => {
          throw error;
        });
    },
    async updateAlert(
      { commit }: CommitFunction,
      payload: { oldAlertUUID: UUID; updateData: any },
    ): Promise<void> {
      // once we get around to updating alerts, we will need to update the base api service to have a
      // 'getAfterUpdate' option like there is for 'create'
      // then we can reset the open/queried alert(s)
      //  might need to hadd some params to the vuex portion for that.. idk its down the road
      await alertApi
        .updateSingle(payload.updateData, payload.oldAlertUUID)
        .catch((error) => {
          throw error;
        });
    },
    async updateAlerts(
      { commit }: CommitFunction,
      payload: { oldAlertUUIDs: UUID[]; updateData: any },
    ): Promise<void> {
      // I have no idea if this is the right way to do this
      // but basically pushing all the requests to update into an array
      const promises = [];
      for (let i = 0; i < payload.oldAlertUUIDs.length; i++) {
        promises.push(
          alertApi.updateSingle(payload.updateData, payload.oldAlertUUIDs[i]),
        );
      }

      // and then all of those requests are resolved here
      await Promise.all(promises).catch((error) => {
        throw error;
      });

      // reason enough to have an updateMultiple in api?
    },
  },
};

export default store;
