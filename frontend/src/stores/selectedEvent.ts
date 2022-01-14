import { defineStore } from "pinia";

import { UUID } from "@/models/base";

export const useSelectedEventStore = defineStore({
  id: "selectedEventStore",

  state: () => ({
    selected: [] as UUID[],
  }),

  getters: {
    anySelected(): boolean {
      return this.selected.length > 0;
    },

    multipleSelected(): boolean {
      return this.selected.length > 1;
    },
  },

  actions: {
    select(uuid: UUID) {
      this.selected.push(uuid);
    },

    selectAll(uuids: UUID[]) {
      this.selected = uuids;
    },

    unselect(uuid: UUID) {
      this.selected = this.selected.filter((u) => u !== uuid);
    },

    unselectAll() {
      this.selected = [];
    },
  },
});
