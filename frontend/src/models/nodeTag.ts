import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type nodeTagCreate = genericObjectCreate;

export type nodeTagRead = genericObjectRead;

export interface nodeTagReadPage extends genericObjectReadPage {
  items: nodeTagRead[];
}

export type nodeTagUpdate = genericObjectUpdate;
