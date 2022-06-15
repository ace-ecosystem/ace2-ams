import {
  metadataCreate,
  metadataRead,
  metadataReadPage,
  metadataUpdate,
} from "./metadata";

export type metadataTagCreate = metadataCreate;

export type metadataTagRead = metadataRead;

export interface metadataTagReadPage extends metadataReadPage {
  items: metadataTagRead[];
}

export type metadataTagUpdate = metadataUpdate;
