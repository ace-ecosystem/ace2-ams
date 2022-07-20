import {
  metadataCreate,
  metadataRead,
  metadataReadPage,
  metadataUpdate,
} from "./metadata";

export type metadataCriticalPointCreate = metadataCreate;

export type metadataCriticalPointRead = metadataRead;

export interface metadataCriticalPointReadPage extends metadataReadPage {
  items: metadataCriticalPointRead[];
}

export type metadataCriticalPointUpdate = metadataUpdate;
