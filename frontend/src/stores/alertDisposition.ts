import { defineStore } from "pinia";
import { alertDispositionRead } from "@/models/alertDisposition";
import { AlertDisposition } from "@/services/api/alertDisposition";

export const useAlertDispositionStore = defineStore({
  id: "alertDispositionStore",

  state: () => ({
    items: [] as alertDispositionRead[],
  }),

  getters: {
    allItems(): alertDispositionRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await AlertDisposition.readAll();
    },
  },
});
