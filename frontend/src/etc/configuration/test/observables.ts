import { observableAction } from "@/models/observable";
import { observableTypeMetaData } from "@/models/observableType";
import { observableTreeReadFactory } from "@mocks/observable";
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

export const commonObservableActions = [
  enableDetection,
  disableDetection,
  updateDetectionExpiration,
];

const ipv4SpecificObservableAction: observableAction = {
  type: "command",
  label: "IPV4 Command",
  description: "Test command",
  icon: "pi pi=check",
  command: (obs) => {
    console.log(obs.uuid);
  },
};

export const observableMetadata: PartialRecord<
  knownObservables,
  observableTypeMetaData
> = {
  file: {
    actions: [{ items: [] }],
    style: { color: "red" },
  },
  ipv4: {
    actions: [{ items: [ipv4SpecificObservableAction], label: "Subheader" }],
    style: { color: "blue" },
  },
};
