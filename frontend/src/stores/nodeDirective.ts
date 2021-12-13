import { defineStore } from "pinia";
import { nodeDirectiveRead } from "@/models/nodeDirective";
import { NodeDirective } from "@/services/api/nodeDirective";

export const useNodeDirectiveStore = defineStore({
  id: "nodeDirectiveStore",

  state: () => ({
    items: [] as nodeDirectiveRead[],
  }),

  getters: {
    allItems(): nodeDirectiveRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await NodeDirective.readAll();
    },
  },
});
