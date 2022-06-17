import {
  metadataCreate,
  metadataRead,
  metadataReadPage,
  metadataUpdate,
} from "./metadata";

export type metadataDirectiveCreate = metadataCreate;

export type metadataDirectiveRead = metadataRead;

export interface metadataDirectiveReadPage extends metadataReadPage {
  items: metadataDirectiveRead[];
}

export type metadataDirectiveUpdate = metadataUpdate;
