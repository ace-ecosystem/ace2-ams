import { threatCreate, threatUpdate } from "@/models/threat";
import { defineStore } from "pinia";
import { threatRead } from "@/models/threat";
import { Threat } from "@/services/api/threat";
import { UUID } from "@/models/base";
import { groupItemsByQueue } from "@/etc/helpers";

export const useThreatStore = defineStore({
  id: "threatStore",

  state: () => ({
    items: [] as threatRead[],
    itemsByQueue: {} as Record<string, threatRead[]>,
  }),

  getters: {
    allItems(): threatRead[] {
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
    async create(newThreat: threatCreate) {
      await Threat.create(newThreat)
        .then(() => {
          this.readAll();
        })
        .catch((error) => {
          throw error;
        });
    },

    async readAll() {
      this.items = await Threat.readAll();
      this.itemsByQueue = groupItemsByQueue(this.items);
    },

    async update(uuid: UUID, data: threatUpdate) {
      await Threat.update(uuid, data)
        .then(() => {
          this.readAll();
        })
        .catch((error) => {
          throw error;
        });
    },
  },
});
