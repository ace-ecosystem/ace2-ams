import UpdateDetectionExpirationVue from "@/components/Observables/ObservableActions/UpdateDetectionExpiration.vue";
import TagModalVue from "@/components/Modals/TagModal.vue";
import {
  observableActionModal,
  observableActionCommand,
  observableTreeRead,
} from "@/models/observable";
import { ObservableInstance } from "@/services/api/observable";
import RemoveTagModalVue from "@/components/Modals/RemoveTagModal.vue";

export const enableDetection: observableActionCommand = {
  label: "Enable Detection",
  description: "Enable observable for future detection",
  icon: "pi pi-check-circle",
  type: "command",
  reloadPage: true,
  command: async (obs: observableTreeRead) => {
    return await ObservableInstance.update(obs.uuid, { forDetection: true });
  },
  requirements: (obs: observableTreeRead) => !obs.forDetection,
};

export const disableDetection: observableActionCommand = {
  label: "Disable Detection",
  description: "Disable observable for future detection",
  icon: "pi pi-times-circle",
  type: "command",
  reloadPage: true,
  command: async (obs: observableTreeRead) => {
    return await ObservableInstance.update(obs.uuid, { forDetection: false });
  },
  requirements: (obs: observableTreeRead) => obs.forDetection,
};

export const updateDetectionExpiration: observableActionModal = {
  label: "Update Expiration",
  description: "Update expiration datetime for observable",
  icon: "pi pi-clock",
  type: "modal",
  modal: UpdateDetectionExpirationVue,
  modalName: "UpdateDetectionExpiration",
  requirements: (obs: observableTreeRead) => obs.forDetection,
};

export const addTag: observableActionModal = {
  label: "Add Tag",
  description: "Add a tag to a given observable",
  icon: "pi pi-tag",
  type: "modal",
  modal: TagModalVue,
  modalName: "ObservableTagModal",
};

export const removeTag: observableActionModal = {
  label: "Remove Tag(s)",
  description: "Remove a tag from this observable",
  icon: "pi pi-tag",
  type: "modal",
  modal: RemoveTagModalVue,
  modalName: "ObservableRemoveTagModal",
};
