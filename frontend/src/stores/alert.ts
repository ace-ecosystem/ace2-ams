import { defineStore } from "pinia";

import {
  alertCreate,
  alertSummary,
  alertTreeRead,
  alertUpdate,
} from "@/models/alert";
import { UUID } from "@/models/base";
import { Alert, parseAlertSummary } from "@/services/api/alert";

export const useAlertStore = defineStore({
  id: "alertStore",

  state: () => ({
    openAlert: null as unknown as alertTreeRead,

    // whether the alert should be reloaded
    requestReload: false,
  }),

  getters: {
    openAlertSummary(): alertSummary | null {
      if (this.openAlert) {
        return parseAlertSummary(this.openAlert);
      }
      return null;
    },
  },

  actions: {
    async create(newAlert: alertCreate) {
      await Alert.createAndRead(newAlert)
        .then((alert) => {
          this.openAlert = alert;
        })
        .catch((error) => {
          throw error;
        });
    },

    async read(uuid: UUID) {
      await Alert.read(uuid)
        .then((alert) => {
          this.openAlert = alert;
        })
        .catch((error) => {
          throw error;
        });
    },

    async update(data: alertUpdate[]) {
      // once we get around to updating alerts, we will need to update the base api service to have a
      // 'getAfterUpdate' option like there is for 'create'
      // then we can reset the open/queried alert(s)
      await Alert.update(data).catch((error) => {
        throw error;
      });
    },
  },
});
