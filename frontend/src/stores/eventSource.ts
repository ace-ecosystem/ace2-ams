import { defineStore } from "pinia";
import { eventSourceRead } from "@/models/eventSource";
import { EventSource } from "@/services/api/eventSource";
import { groupItemsByQueue } from "@/etc/helpers";

export const useEventSourceStore = defineStore({
  id: "eventSourceStore",

  state: () => ({
    items: [] as eventSourceRead[],
    itemsByQueue: {} as Record<string, eventSourceRead[]>,
  }),

  getters: {
    allItems(): eventSourceRead[] {
      return this.items;
    },
    getItemsByQueue() {
      return (queue: string) => {
        if (queue in this.itemsByQueue) {
          return this.itemsByQueue[queue];
        }
        return [];
      };
    },
  },

  actions: {
    async readAll() {
      this.items = await EventSource.readAll();
      this.itemsByQueue = groupItemsByQueue(this.items);
    },
  },
});
