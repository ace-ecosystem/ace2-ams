import { defineStore } from "pinia";
import { observableTypeRead } from "@/models/observableType";
import { ObservableType } from "@/services/api/observableType";

export const useObservableTypeStore = defineStore({
  id: "observableTypeStore",

  state: () => ({
    items: [] as observableTypeRead[],
  }),

  getters: {
    allItems(): observableTypeRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await ObservableType.readAll();
    },
  },
});
