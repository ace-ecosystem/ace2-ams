import { defineStore } from "pinia";
import { eventTypeRead } from "@/models/eventType";
import { EventType } from "@/services/api/eventType";

export const useEventTypeStore = defineStore({
  id: "eventTypeStore",

  state: () => ({
    items: [] as eventTypeRead[],
  }),

  getters: {
    allItems(): eventTypeRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await EventType.readAll();
    },
  },
});
