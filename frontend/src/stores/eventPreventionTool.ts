import { defineStore } from "pinia";
import { eventPreventionToolRead } from "@/models/eventPreventionTool";
import { EventPreventionTool } from "@/services/api/eventPreventionTool";
import { groupItemsByQueue } from "@/etc/helpers";

export const useEventPreventionToolStore = defineStore({
  id: "eventPreventionToolStore",

  state: () => ({
    items: [] as eventPreventionToolRead[],
    itemsByQueue: {} as Record<string, eventPreventionToolRead[]>,
  }),

  getters: {
    allItems(): eventPreventionToolRead[] {
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
      this.items = await EventPreventionTool.readAll();
      this.itemsByQueue = groupItemsByQueue(this.items);
    },
  },
});
