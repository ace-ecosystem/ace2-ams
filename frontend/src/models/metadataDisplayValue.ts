import {
  metadataCreate,
  metadataRead,
  metadataReadPage,
  metadataUpdate,
} from "./metadata";

export type metadataDisplayValueCreate = metadataCreate;

export type metadataDisplayValueRead = metadataRead;

export interface metadataDisplayValueReadPage extends metadataReadPage {
  items: metadataDisplayValueRead[];
}

export type metadataDisplayValueUpdate = metadataUpdate;
