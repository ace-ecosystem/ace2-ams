import { defineStore } from "pinia";
import { alertToolInstanceRead } from "@/models/alertToolInstance";
import { AlertToolInstance } from "@/services/api/alertToolInstance";

export const useAlertToolInstanceStore = defineStore({
  id: "alertToolInstanceStore",

  state: () => ({
    items: [] as alertToolInstanceRead[],
  }),

  getters: {
    allItems(): alertToolInstanceRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await AlertToolInstance.readAll();
    },
  },
});
