import { nodeThreatCreate, nodeThreatUpdate } from "./../models/nodeThreat";
import { defineStore } from "pinia";
import { nodeThreatRead } from "@/models/nodeThreat";
import { NodeThreat } from "@/services/api/nodeThreat";
import { UUID } from "@/models/base";

export const useNodeThreatStore = defineStore({
  id: "nodeThreatStore",

  state: () => ({
    items: [] as nodeThreatRead[],
  }),

  getters: {
    allItems(): nodeThreatRead[] {
      return this.items;
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
