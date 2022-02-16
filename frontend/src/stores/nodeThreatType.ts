import { defineStore } from "pinia";
import { nodeThreatTypeRead } from "@/models/nodeThreatType";
import { NodeThreatType } from "@/services/api/nodeThreatType";

export const useNodeThreatTypeStore = defineStore({
  id: "nodeThreatTypeStore",

  state: () => ({
    items: [] as nodeThreatTypeRead[],
  }),

  getters: {
    allItems(): nodeThreatTypeRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await NodeThreatType.readAll();
    },
  },
});
