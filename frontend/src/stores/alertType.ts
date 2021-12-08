import { defineStore } from "pinia";
import { alertTypeRead } from "@/models/alertType";
import { AlertType } from "@/services/api/alertType";

export const useAlertTypeStore = defineStore({
  id: "alertTypeStore",

  state: () => ({
    items: [] as alertTypeRead[],
  }),

  getters: {
    allItems(): alertTypeRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await AlertType.readAll();
    },
  },
});
