import { defineStore } from "pinia";
import {
  alertCreate,
  alertFilterParams,
  alertSummaryRead,
  alertTableSummary,
  alertUpdate,
} from "@/models/alert";
import { Alert } from "@/services/api/alert";

export const useAlertStore = defineStore({
  id: "alertStore",

  state: () => ({
    // currently opened alert
    openAlert: null,

    // all alerts returned from the current page using the current filters
    visibleQueriedAlerts: [],

    // total number of alerts from all pages
    totalAlerts: 0,
  }),

  getters: {
    openAlert(): boolean {
      return this.openAlert;
    },
  },

  actions: {
    async readAll() {
      this.items = await AlertQueue.readAll();
    },
  },
});
