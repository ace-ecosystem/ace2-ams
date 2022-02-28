import { defineStore } from "pinia";
import { nodeThreatActorRead } from "@/models/nodeThreatActor";
import { NodeThreatActor } from "@/services/api/nodeThreatActor";
import { groupItemsByQueue } from "@/etc/helpers";

export const useNodeThreatActorStore = defineStore({
  id: "nodeThreatActorStore",

  state: () => ({
    items: [] as nodeThreatActorRead[],
    itemsByQueue: {} as Record<string, nodeThreatActorRead[]>,
  }),

  getters: {
    allItems(): nodeThreatActorRead[] {
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
      this.items = await NodeThreatActor.readAll();
      this.itemsByQueue = groupItemsByQueue(this.items);
    },
  },
});
