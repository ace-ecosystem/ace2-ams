import { defineStore } from "pinia";
import { eventRemediationRead } from "@/models/eventRemediation";
import { EventRemediation } from "@/services/api/eventRemediation";
import { groupItemsByQueue } from "@/etc/helpers";

export const useEventRemediationStore = defineStore({
  id: "eventRemediationStore",

  state: () => ({
    items: [] as eventRemediationRead[],
    itemsByQueue: {} as Record<string, eventRemediationRead[]>,
  }),

  getters: {
    allItems(): eventRemediationRead[] {
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
      this.items = await EventRemediation.readAll();
      this.itemsByQueue = groupItemsByQueue(this.items);
    },
  },
});
