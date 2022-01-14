import { defineStore } from "pinia";
import { eventQueueRead } from "@/models/eventQueue";
import { EventQueue } from "@/services/api/eventQueue";

export const useEventQueueStore = defineStore({
  id: "eventQueueStore",

  state: () => ({
    items: [] as eventQueueRead[],
  }),

  getters: {
    allItems(): eventQueueRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await EventQueue.readAll();
    },
  },
});
