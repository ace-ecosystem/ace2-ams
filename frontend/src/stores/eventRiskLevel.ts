import { defineStore } from "pinia";
import { eventRiskLevelRead } from "@/models/eventRiskLevel";
import { EventRiskLevel } from "@/services/api/eventRiskLevel";
import { groupItemsByQueue } from "@/etc/helpers";

export const useEventRiskLevelStore = defineStore({
  id: "eventRiskLevelStore",

  state: () => ({
    items: [] as eventRiskLevelRead[],
    itemsByQueue: {} as Record<string, eventRiskLevelRead[]>,
  }),

  getters: {
    allItems(): eventRiskLevelRead[] {
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
      this.items = await EventRiskLevel.readAll();
      this.itemsByQueue = groupItemsByQueue(this.items);
    },
  },
});
