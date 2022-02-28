import { defineStore } from "pinia";
import { eventTypeRead } from "@/models/eventType";
import { EventType } from "@/services/api/eventType";
import { groupItemsByQueue } from "@/etc/helpers";

export const useEventTypeStore = defineStore({
  id: "eventTypeStore",

  state: () => ({
    items: [] as eventTypeRead[],
    itemsByQueue: {} as Record<string, eventTypeRead[]>,
  }),

  getters: {
    allItems(): eventTypeRead[] {
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
      this.items = await EventType.readAll();
      this.itemsByQueue = groupItemsByQueue(this.items);
    },
  },
});
