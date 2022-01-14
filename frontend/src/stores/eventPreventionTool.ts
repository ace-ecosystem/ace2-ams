import { defineStore } from "pinia";
import { eventPreventionToolRead } from "@/models/eventPreventionTool";
import { EventPreventionTool } from "@/services/api/eventPreventionTool";

export const useEventPreventionToolStore = defineStore({
  id: "eventPreventionToolStore",

  state: () => ({
    items: [] as eventPreventionToolRead[],
  }),

  getters: {
    allItems(): eventPreventionToolRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await EventPreventionTool.readAll();
    },
  },
});
