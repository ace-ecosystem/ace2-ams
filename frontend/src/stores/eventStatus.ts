import { defineStore } from "pinia";
import { eventStatusRead } from "@/models/eventStatus";
import { EventStatus } from "@/services/api/eventStatus";
import { groupItemsByQueue } from "@/etc/helpers";

export const useEventStatusStore = defineStore({
  id: "eventStatusStore",

  state: () => ({
    items: [] as eventStatusRead[],
    itemsByQueue: {} as Record<string, eventStatusRead[]>,
  }),

  getters: {
    allItems(): eventStatusRead[] {
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
      this.items = await EventStatus.readAll();
      this.itemsByQueue = groupItemsByQueue(this.items);
    },
  },
});
