import { defineStore } from "pinia";
import { eventRead } from "@/models/event";
import { Event } from "@/services/api/event";

export const useEventStore = defineStore({
  id: "eventStore",

  state: () => ({
    items: [] as eventRead[],
  }),

  getters: {
    allItems(): eventRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      // this.items = await Event.readAll();
      this.items = [];
    },
  },
});
