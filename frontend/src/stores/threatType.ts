import { defineStore } from "pinia";
import { threatTypeRead } from "@/models/threatType";
import { ThreatType } from "@/services/api/threatType";

export const useThreatTypeStore = defineStore({
  id: "threatTypeStore",

  state: () => ({
    items: [] as threatTypeRead[],
  }),

  getters: {
    allItems(): threatTypeRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await ThreatType.readAll();
    },
  },
});
