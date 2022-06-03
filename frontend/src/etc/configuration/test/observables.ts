import TagModalVue from "@/components/Modals/TagModal.vue";
import {
  observableActionCommand,
  observableActionModal,
  observableTreeRead,
} from "@/models/observable";
import { observableTypeMetaData } from "@/models/observableType";
import {
  enableDetection,
  disableDetection,
  updateDetectionExpiration,
} from "../../constants/observables";

type FILE = "file";
type URL = "url";
type IPV4 = "ipv4";

type knownObservables = FILE | URL | IPV4;

type PartialRecord<K extends keyof any, T> = Partial<Record<K, T>>;

export const testModalAction: observableActionModal = {
  label: "Test Action",
  description: "Test Modal Action",
  icon: "pi pi-tag",
  type: "modal",
  modal: TagModalVue,
  modalName: "testModal",
};

export const commonObservableActions = [
  testModalAction,
  enableDetection,
  disableDetection,
  updateDetectionExpiration,
];

const ipv4SpecificObservableAction: observableActionCommand = {
  type: "command",
  label: "IPV4 Command",
  description: "Test command",
  icon: "pi pi=check",
  reloadPage: false,
  command: (obs: observableTreeRead) => {
    console.log(obs.uuid);
  },
};

export const observableMetadata: PartialRecord<
  knownObservables,
  observableTypeMetaData
> = {
  file: {
    style: { color: "red" },
  },
  ipv4: {
    actions: [{ items: [ipv4SpecificObservableAction], label: "Subheader" }],
    style: { color: "blue" },
    placeholder: "ex. 1.2.3.4",
    validator: (ipv4: string) => {
      const regex = new RegExp(
        "((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(.|$)){4}",
      );
      return regex.test(ipv4);
    },
  },
};
