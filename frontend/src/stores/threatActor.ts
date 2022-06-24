import { defineStore } from "pinia";
import { threatActorRead } from "@/models/threatActor";
import { ThreatActor } from "@/services/api/threatActor";
import { groupItemsByQueue } from "@/etc/helpers";

export const useThreatActorStore = defineStore({
  id: "threatActorStore",

  state: () => ({
    items: [] as threatActorRead[],
    itemsByQueue: {} as Record<string, threatActorRead[]>,
  }),

  getters: {
    allItems(): threatActorRead[] {
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
      this.items = await ThreatActor.readAll();
      this.itemsByQueue = groupItemsByQueue(this.items);
    },
  },
});
