import { defineStore } from "pinia";
import { eventSourceRead } from "@/models/eventSource";
import { EventSource } from "@/services/api/eventSource";

export const useEventSourceStore = defineStore({
  id: "eventSourceStore",

  state: () => ({
    items: [] as eventSourceRead[],
  }),

  getters: {
    allItems(): eventSourceRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await EventSource.readAll();
    },
  },
});
