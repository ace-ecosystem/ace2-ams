import { defineStore } from "pinia";
import { observableRead, observableUpdate } from "@/models/observable";
import { ObservableInstance } from "@/services/api/observable";
import { UUID } from "@/models/base";

export const useObservableStore = defineStore({
  id: "observableStore",
  actions: {
    async read(uuid: UUID): Promise<observableRead> {
      return await ObservableInstance.read(uuid).catch((error) => {
        throw error;
      });
    },

    async update(uuid: UUID, data: observableUpdate) {
      await ObservableInstance.update(uuid, data).catch((error) => {
        throw error;
      });
    },
  },
});
