import { defineStore } from "pinia";
import { eventStatusRead } from "@/models/eventStatus";
import { EventStatus } from "@/services/api/eventStatus";

export const useEventStatusStore = defineStore({
  id: "eventStatusStore",

  state: () => ({
    items: [] as eventStatusRead[],
  }),

  getters: {
    allItems(): eventStatusRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await EventStatus.readAll();
    },
  },
});
