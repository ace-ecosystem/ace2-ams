import { observableTypeMetaData } from "@/models/observableType";
import {
  enableDetection,
  disableDetection,
  updateDetectionExpiration,
  addTag,
  removeTag,
} from "../constants/observables";

type FILE = "file";
type URL = "url";
type IPV4 = "ipv4";

type knownObservables = FILE | URL | IPV4;

type PartialRecord<K extends keyof any, T> = Partial<Record<K, T>>;

export const commonObservableActions = [
  addTag,
  removeTag,
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
    placeholder: "ex. 1.2.3.4",
    validator: (ipv4: string) => {
      const regex = new RegExp(
        "((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(.|$)){4}",
      );
      return regex.test(ipv4);
    },
  },
  url: {
    style: { color: "blue" },
    placeholder: "ex. https://www.google.com",
  },
};
