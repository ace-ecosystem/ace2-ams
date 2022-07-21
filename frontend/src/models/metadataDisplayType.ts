import {
  metadataCreate,
  metadataRead,
  metadataReadPage,
  metadataUpdate,
} from "./metadata";

export type metadataDisplayTypeCreate = metadataCreate;

export type metadataDisplayTypeRead = metadataRead;

export interface metadataDisplayTypeReadPage extends metadataReadPage {
  items: metadataDisplayTypeRead[];
}

export type metadataDisplayTypeUpdate = metadataUpdate;
