import { defineStore } from "pinia";
import { tagRead } from "@/models/tag";
import { Tag } from "@/services/api/tag";

export const useTagStore = defineStore({
  id: "tagStore",

  state: () => ({
    items: [] as tagRead[],
  }),

  getters: {
    allItems(): tagRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await Tag.readAll();
    },
  },
});
