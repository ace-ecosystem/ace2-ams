import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type metadataCreate = genericObjectCreate;

export interface metadataRead extends genericObjectRead {
  metadataType: string;
}

export interface metadataReadPage extends genericObjectReadPage {
  items: metadataRead[];
}

export type metadataUpdate = genericObjectUpdate;
