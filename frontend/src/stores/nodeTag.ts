import { defineStore } from "pinia";
import { nodeTagRead } from "@/models/nodeTag";
import { NodeTag } from "@/services/api/nodeTag";

export const useNodeTagStore = defineStore({
  id: "nodeTagStore",

  state: () => ({
    items: [] as nodeTagRead[],
  }),

  getters: {
    allItems(): nodeTagRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await NodeTag.readAll();
    },
  },
});
