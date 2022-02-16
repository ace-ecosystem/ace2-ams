import { defineStore } from "pinia";
import { eventRemediationRead } from "@/models/eventRemediation";
import { EventRemediation } from "@/services/api/eventRemediation";

export const useEventRemediationStore = defineStore({
  id: "eventRemediationStore",

  state: () => ({
    items: [] as eventRemediationRead[],
  }),

  getters: {
    allItems(): eventRemediationRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await EventRemediation.readAll();
    },
  },
});
