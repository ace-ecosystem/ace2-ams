import {
  metadataCreate,
  metadataRead,
  metadataReadPage,
  metadataUpdate,
} from "./metadata";

export type metadataDetectionPointCreate = metadataCreate;

export type metadataDetectionPointRead = metadataRead;

export interface metadataDetectionPointReadPage extends metadataReadPage {
  items: metadataDetectionPointRead[];
}

export type metadataDetectionPointUpdate = metadataUpdate;
