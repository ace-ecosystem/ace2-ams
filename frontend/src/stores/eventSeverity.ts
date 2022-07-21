import { defineStore } from "pinia";
import { eventSeverityRead } from "@/models/eventSeverity";
import { EventSeverity } from "@/services/api/eventSeverity";
import { groupItemsByQueue } from "@/etc/helpers";

export const useEventSeverityStore = defineStore({
  id: "eventSeverityStore",

  state: () => ({
    items: [] as eventSeverityRead[],
    itemsByQueue: {} as Record<string, eventSeverityRead[]>,
  }),

  getters: {
    allItems(): eventSeverityRead[] {
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
      this.items = await EventSeverity.readAll();
      this.itemsByQueue = groupItemsByQueue(this.items);
    },
  },
});
