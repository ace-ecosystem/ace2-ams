import { defineStore } from "pinia";
import { nodeThreatActorRead } from "@/models/nodeThreatActor";
import { NodeThreatActor } from "@/services/api/nodeThreatActor";

export const useNodeThreatActorStore = defineStore({
  id: "nodeThreatActorStore",

  state: () => ({
    items: [] as nodeThreatActorRead[],
  }),

  getters: {
    allItems(): nodeThreatActorRead[] {
      return this.items;
    },
  },

  actions: {
    async readAll() {
      this.items = await NodeThreatActor.readAll();
    },
  },
});
