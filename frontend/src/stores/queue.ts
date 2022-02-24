import { defineStore } from "pinia";
import { queueRead } from "@/models/queue";
import { queue } from "@/services/api/queue";

export const useQueueStore = defineStore({
  id: "queueStore",

  state: () => ({
    items: [] as queueRead[],
  }),

  getters: {
    allItems(): queueRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await queue.readAll();
    },
  },
});
