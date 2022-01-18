import { defineStore } from "pinia";
import { eventVectorRead } from "@/models/eventVector";
import { EventVector } from "@/services/api/eventVector";

export const useEventVectorStore = defineStore({
  id: "eventVectorStore",

  state: () => ({
    items: [] as eventVectorRead[],
  }),

  getters: {
    allItems(): eventVectorRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await EventVector.readAll();
    },
  },
});
