import { defineStore } from "pinia";
import { metadataDirectiveRead } from "@/models/metadataDirective";
import { MetadataDirective } from "@/services/api/metadataDirective";

export const useMetadataDirectiveStore = defineStore({
  id: "metadataDirectiveStore",

  state: () => ({
    items: [] as metadataDirectiveRead[],
  }),

  getters: {
    allItems(): metadataDirectiveRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await MetadataDirective.readAll();
    },
  },
});
