import { defineStore } from "pinia";
import { eventRiskLevelRead } from "@/models/eventRiskLevel";
import { EventRiskLevel } from "@/services/api/eventRiskLevel";

export const useEventRiskLevelStore = defineStore({
  id: "eventRiskLevelStore",

  state: () => ({
    items: [] as eventRiskLevelRead[],
  }),

  getters: {
    allItems(): eventRiskLevelRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await EventRiskLevel.readAll();
    },
  },
});
