import { defineStore } from "pinia";
import { eventVectorRead } from "@/models/eventVector";
import { EventVector } from "@/services/api/eventVector";
import { groupItemsByQueue } from "@/etc/helpers";

export const useEventVectorStore = defineStore({
  id: "eventVectorStore",

  state: () => ({
    items: [] as eventVectorRead[],
    itemsByQueue: {} as Record<string, eventVectorRead[]>,
  }),

  getters: {
    allItems(): eventVectorRead[] {
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
      this.items = await EventVector.readAll();
      this.itemsByQueue = groupItemsByQueue(this.items);
    },
  },
});
