import alertApi from "@/services/api/alerts";
import { CommitFunction } from "@/store/index";
import { alert } from "@/models/alert";
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
    openAlert: (state: { openAlert: alert }) => state.openAlert,
    queriedAlerts: (state: { queriedAlerts: alert[] }) => state.queriedAlerts,
  },
  mutations: {
    SET_OPEN_ALERT(state: { openAlert: alert | null }, alert: alert) {
      state.openAlert = alert;
    },
    SET_QUERIED_ALERTS(state: { queriedAlerts: alert[] }, alerts: alert[]) {
      state.queriedAlerts = alerts;
    },
    SET_QUERY_TIMESTAMP(state: { lastQueriedAlertsTime: number | null }) {
      state.lastQueriedAlertsTime = new Date().getTime();
    },
  },

  actions: {
    async createAlert({ commit }: CommitFunction, newAlert: any) {
      await alertApi
        .create(newAlert)
        .then((alert) => {
          console.log(alert);
          commit("SET_OPEN_ALERT", alert);
        })
        .catch((error) => {
          throw error;
        });
    },
    async getSingle({ commit }: CommitFunction, alertUUID: UUID) {
      await alertApi
        .getSingle(alertUUID)
        .then((alert) => {
          commit("SET_OPEN_ALERT", alert);
        })
        .catch((error) => {
          throw error;
        });
    },
    async getAll({ commit }: CommitFunction, options: any) {
      await alertApi
        .getAll(options)
        .then((alerts) => {
          const parsedAlerts = [];
          for (const index in alerts.items) {
            const alert = alerts.items[index];
            const parsedAlert = {
              comments: alert.comments,
              disposition: alert.disposition ? alert.disposition.value : "OPEN",
              dispositionTime: alert.dispositionTime
                ? alert.dispositionTime
                : null,
              dispositionUser: alert.dispositionUser
                ? alert.dispositionUser.value
                : "None",
              eventTime: alert.eventTime,
              insertTime: alert.insertTime,
              name: alert.name ? alert.name : "Unnamed",
              observables: alert.analysis.discoveredObservableUuids,
              owner: alert.owner ? alert.owner.value : "None",
              queue: alert.queue.value,
              tags: alert.tags,
              tool: alert.tool ? alert.tool.value : "None",
              type: alert.type ? alert.type.value : "None",
              uuid: alert.uuid,
            };
            parsedAlerts.push(parsedAlert);
          }
          commit("SET_QUERIED_ALERTS", parsedAlerts);
        })
        .catch((error) => {
          throw error;
        });
    },
    async updateAlert(
      { commit }: CommitFunction,
      payload: { oldAlertUUID: UUID; updateData: any },
    ) {
      // once we get around to updating alerts, we will need to update the base api service to have a
      // 'getAfterUpdate' option like there is for 'create'
      // then we can reset the open/queried alert(s)
      //  might need to hadd some options to the vuex portion for that.. idk its down the road
      await alertApi
        .updateSingle(payload.updateData, payload.oldAlertUUID)
        .catch((error) => {
          throw error;
        });
    },
    async updateAlerts(
      { commit }: CommitFunction,
      payload: { oldAlertUUIDs: UUID[]; updateData: any },
    ) {
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
