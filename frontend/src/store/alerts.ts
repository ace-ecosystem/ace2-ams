import { Alert } from "@/services/api/alert";
import { CommitFunction } from "@/store/index";
import {
  alertCreate,
  alertFilterParams,
  alertSummaryRead,
  alertTableSummary,
  alertUpdate,
} from "@/models/alert";
import { UUID } from "@/models/base";

export function parseAlertSummary(alert: alertSummaryRead): alertTableSummary {
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
      openAlert: alertSummaryRead | null;
      visibleQueriedAlerts: alertTableSummary[];
      totalAlerts: number;
    }): alertSummaryRead | null => state.openAlert,
    visibleQueriedAlerts: (state: {
      openAlert: alertSummaryRead | null;
      visibleQueriedAlerts: alertTableSummary[];
      totalAlerts: number;
    }): alertTableSummary[] => state.visibleQueriedAlerts,
    visibleQueriedAlertsUuids: (state: {
      openAlert: alertSummaryRead | null;
      visibleQueriedAlerts: alertTableSummary[];
      totalAlerts: number;
    }): UUID[] => {
      const allAlertUuids = [];
      for (let i = 0; i < state.visibleQueriedAlerts.length; i++) {
        allAlertUuids.push(state.visibleQueriedAlerts[i].uuid);
      }
      return allAlertUuids;
    },
    totalAlerts: (state: {
      openAlert: alertSummaryRead | null;
      visibleQueriedAlerts: alertTableSummary[];
      totalAlerts: number;
    }): number => state.totalAlerts,
  },
  mutations: {
    SET_OPEN_ALERT(
      state: { openAlert: alertSummaryRead | null },
      alert: alertSummaryRead,
    ): void {
      state.openAlert = alert;
    },
    SET_VISIBLE_QUERIED_ALERTS(
      state: { visibleQueriedAlerts: alertTableSummary[] },
      alerts: alertTableSummary[],
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
      newAlert: alertCreate,
    ): Promise<void> {
      await Alert.create(newAlert)
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
      await Alert.read(alertUUID)
        .then((alert) => {
          commit("SET_OPEN_ALERT", alert);
        })
        .catch((error) => {
          throw error;
        });
    },
    async getPage(
      { commit }: CommitFunction,
      params: alertFilterParams,
    ): Promise<void> {
      await Alert.readPage(params)
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
      payload: { oldAlertUUID: UUID; updateData: alertUpdate },
    ): Promise<void> {
      // once we get around to updating alerts, we will need to update the base api service to have a
      // 'getAfterUpdate' option like there is for 'create'
      // then we can reset the open/queried alert(s)
      //  might need to hadd some params to the vuex portion for that.. idk its down the road
      await Alert.update(payload.oldAlertUUID, payload.updateData).catch(
        (error) => {
          throw error;
        },
      );
    },
    async updateAlerts(
      { commit }: CommitFunction,
      payload: { oldAlertUUIDs: UUID[]; updateData: alertUpdate },
    ): Promise<void> {
      // I have no idea if this is the right way to do this
      // but basically pushing all the requests to update into an array
      const promises = [];
      for (let i = 0; i < payload.oldAlertUUIDs.length; i++) {
        promises.push(
          Alert.update(payload.oldAlertUUIDs[i], payload.updateData),
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
