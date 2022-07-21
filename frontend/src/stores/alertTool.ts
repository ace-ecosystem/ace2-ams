import { defineStore } from "pinia";
import { alertToolRead } from "@/models/alertTool";
import { AlertTool } from "@/services/api/alertTool";

export const useAlertToolStore = defineStore({
  id: "alertToolStore",

  state: () => ({
    items: [] as alertToolRead[],
  }),

  getters: {
    allItems(): alertToolRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await AlertTool.readAll();
    },
  },
});
