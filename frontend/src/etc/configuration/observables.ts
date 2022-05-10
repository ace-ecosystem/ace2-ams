import { observableTypeMetaData } from "@/models/observableType";
import {
  enableDetection,
  disableDetection,
  updateDetectionExpiration,
  addTag,
} from "../constants/observables";

type FILE = "file";
type URL = "url";
type IPV4 = "ipv4";

type knownObservables = FILE | URL | IPV4;

type PartialRecord<K extends keyof any, T> = Partial<Record<K, T>>;

export const commonObservableActions = [
  addTag,
  enableDetection,
  disableDetection,
  updateDetectionExpiration,
];

export const observableMetadata: PartialRecord<
  knownObservables,
  observableTypeMetaData
> = {
  file: {
    style: { color: "red" },
  },
  ipv4: {
    style: { color: "blue" },
  },
};
