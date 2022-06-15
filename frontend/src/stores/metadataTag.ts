import { defineStore } from "pinia";
import { metadataTagRead } from "@/models/metadataTag";
import { MetadataTag } from "@/services/api/metadataTag";

export const useMetadataTagStore = defineStore({
  id: "metadataTagStore",

  state: () => ({
    items: [] as metadataTagRead[],
  }),

  getters: {
    allItems(): metadataTagRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await MetadataTag.readAll();
    },
  },
});
