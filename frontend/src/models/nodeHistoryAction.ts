import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type nodeHistoryActionCreate = genericObjectCreate;

export type nodeHistoryActionRead = genericObjectRead;

export interface nodeHistoryActionReadPage extends genericObjectReadPage {
  items: nodeHistoryActionRead[];
}

export type nodeHistoryActionUpdate = genericObjectUpdate;
