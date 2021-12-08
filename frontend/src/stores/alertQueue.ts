import { defineStore } from "pinia";
import { alertQueueRead } from "@/models/alertQueue";
import { AlertQueue } from "@/services/api/alertQueue";

export const alertQueueStore = defineStore({
  id: "alertQueueStore",

  state: () => ({
    items: [] as alertQueueRead[],
  }),

  getters: {
    allItems(): alertQueueRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await AlertQueue.readAll();
    },
  },
});
