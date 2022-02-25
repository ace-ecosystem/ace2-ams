import { nodeThreatCreate, nodeThreatUpdate } from "./../models/nodeThreat";
import { defineStore } from "pinia";
import { nodeThreatRead } from "@/models/nodeThreat";
import { NodeThreat } from "@/services/api/nodeThreat";
import { UUID } from "@/models/base";
import { groupItemsByQueue } from "@/etc/helpers";

export const useNodeThreatStore = defineStore({
  id: "nodeThreatStore",

  state: () => ({
    items: [] as nodeThreatRead[],
    itemsByQueue: {} as Record<string, nodeThreatRead[]>,
  }),

  getters: {
    allItems(): nodeThreatRead[] {
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
    async create(newThreat: nodeThreatCreate) {
      await NodeThreat.create(newThreat)
        .then(() => {
          this.readAll();
        })
        .catch((error) => {
          throw error;
        });
    },

    async readAll() {
      this.items = await NodeThreat.readAll();
      this.itemsByQueue = groupItemsByQueue(this.items);
    },

    async update(uuid: UUID, data: nodeThreatUpdate) {
      await NodeThreat.update(uuid, data)
        .then(() => {
          this.readAll();
        })
        .catch((error) => {
          throw error;
        });
    },
  },
});
