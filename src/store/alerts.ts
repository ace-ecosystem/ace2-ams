import alert from "@/services/api/alerts";
import { AlertRead } from "@/models/alert";
import { CommitFunction } from "@/store/index";
import { UUID } from "@/models/base";

const store = {
  namespaced: true,

  state: {
    // currently opened alert
    openAlert: null,
    // last time alerts were fetched with current filter settings
    lastQueriedAlertsTime: null,
    // all alerts returned from current filter settings
    queriedAlerts: [],
  },
  getters: {
    openAlert: (state: { openAlert: AlertRead }) => state.openAlert,
  },
  mutations: {
    SET_OPEN_ALERT(state: { openAlert: AlertRead | null }, alert: AlertRead) {
      state.openAlert = alert;
    },
    SET_QUERIED_ALERTS(
      state: { queriedAlerts: AlertRead[] },
      alerts: AlertRead[],
    ) {
      state.queriedAlerts = alerts;
    },
    SET_QUERY_TIMESTAMP(state: { lastQueriedAlertsTime: number | null }) {
      state.lastQueriedAlertsTime = new Date().getTime();
    },
  },

  actions: {
    createAlert({ commit }: CommitFunction, newAlert: Record<string, unknown>) {
      return alert
        .create(newAlert)
        .then((alert) => {
          commit("SET_OPEN_ALERT", alert);
        })
        .catch((error) => {
          throw error;
        });
    },
    openAlert({ commit }: CommitFunction, alertUUID: UUID) {
      return alert
        .getSingle(alertUUID)
        .then((alert) => {
          commit("SET_OPEN_ALERT", alert);
        })
        .catch((error) => {
          throw error;
        });
    },
    updateAlert(
      { commit }: CommitFunction,
      payload: { oldAlertUUID: UUID; updateData: Record<string, unknown> },
    ) {
      return alert
        .updateSingle(payload.updateData, payload.oldAlertUUID)
        .catch((error) => {
          throw error;
        });
    },
    updateAlerts(
      { commit }: CommitFunction,
      payload: { oldAlertUUIDs: UUID[]; updateData: Record<string, unknown> },
    ) {
      // I have no idea if this is the right way to do this
      // but basically pushing all the requests to update into an array
      const promises = [];
      for (let i = 0; i < payload.oldAlertUUIDs.length; i++) {
        promises.push(
          alert.updateSingle(payload.updateData, payload.oldAlertUUIDs[i]),
        );
      }

      // and then all of those requests are resolved here
      return Promise.all(promises).catch((error) => {
        throw error;
      });

      // reason enough to have an updateMultiple in api?
    },
  },
};

export default store;
