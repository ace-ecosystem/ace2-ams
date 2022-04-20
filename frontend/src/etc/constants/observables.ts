import UpdateDetectionExpirationVue from "@/components/Observables/ObservableActions/UpdateDetectionExpiration.vue";
import { observableAction, observableTreeRead } from "@/models/observable";
import { ObservableInstance } from "@/services/api/observable";

export const enableDetection: observableAction = {
  label: "Enable Detection",
  description: "Enable observable for future detection",
  icon: "pi pi-check-circle",
  type: "command",
  command: async (obs: observableTreeRead) => {
    return await ObservableInstance.update(obs.uuid, { forDetection: true });
  },
  requirements: (obs: observableTreeRead) => !obs.forDetection,
};

export const disableDetection: observableAction = {
  label: "Disable Detection",
  description: "Disable observable for future detection",
  icon: "pi pi-times-circle",
  type: "command",
  command: async (obs: observableTreeRead) => {
    return await ObservableInstance.update(obs.uuid, { forDetection: false });
  },
  requirements: (obs: observableTreeRead) => obs.forDetection,
};

export const updateDetectionExpiration: observableAction = {
  label: "Update Expiration",
  description: "Update expiration datetime for observable",
  icon: "pi pi-clock",
  type: "modal",
  modal: UpdateDetectionExpirationVue,
  requirements: (obs: observableTreeRead) => obs.forDetection,
};
