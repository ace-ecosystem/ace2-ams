import { defineStore } from "pinia";

import {
  alertCreate,
  alertSummary,
  alertTreeRead,
  alertUpdate,
} from "@/models/alert";
import { observableInAlertRead } from "@/models/observable";
import { UUID } from "@/models/base";
import { Alert } from "@/services/api/alert";
import { parseAlertSummary } from "@/etc/helpers";

export const useAlertStore = defineStore({
  id: "alertStore",

  state: () => ({
    open: null as unknown as alertTreeRead,

    // whether the alert should be reloaded
    requestReload: false,
  }),

  getters: {
    openAlertSummary(): alertSummary | null {
      if (this.open) {
        return parseAlertSummary(this.open);
      }
      return null;
    },
  },

  actions: {
    async create(newAlert: alertCreate) {
      await Alert.createAndRead(newAlert)
        .then((alert) => {
          this.open = alert;
        })
        .catch((error) => {
          throw error;
        });
    },

    async read(uuid: UUID) {
      await Alert.read(uuid)
        .then((alert) => {
          this.open = alert;
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
