import {
  metadataCreate,
  metadataRead,
  metadataReadPage,
  metadataUpdate,
} from "./metadata";

export type tagCreate = metadataCreate;

export type tagRead = metadataRead;

export interface tagReadPage extends metadataReadPage {
  items: tagRead[];
}

export type tagUpdate = metadataUpdate;
