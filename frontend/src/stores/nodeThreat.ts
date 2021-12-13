import { defineStore } from "pinia";
import { nodeThreatRead } from "@/models/nodeThreat";
import { NodeThreat } from "@/services/api/nodeThreat";

export const useNodeThreatStore = defineStore({
  id: "nodeThreatStore",

  state: () => ({
    items: [] as nodeThreatRead[],
  }),

  getters: {
    allItems(): nodeThreatRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await NodeThreat.readAll();
    },
  },
});
