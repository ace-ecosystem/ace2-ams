import { observableTypeMetaData } from "@/models/observableType";
import {
  enableDetection,
  disableDetection,
  adjustDetectionExpiration,
} from "../../constants/observables";

type FILE = "file";
type URL = "url";
type IPV4 = "ipv4";

type knownObservables = FILE | URL | IPV4;

type PartialRecord<K extends keyof any, T> = Partial<Record<K, T>>;

export const commonObservableActions = [
  enableDetection,
  disableDetection,
  adjustDetectionExpiration,
];

export const observableMetadata: PartialRecord<
  knownObservables,
  observableTypeMetaData
> = {
  file: {
    actions: [{ items: [] }],
    style: { color: "red" },
  },
  ipv4: {
    actions: [{ items: [] }],
    style: { color: "blue" },
  },
};
