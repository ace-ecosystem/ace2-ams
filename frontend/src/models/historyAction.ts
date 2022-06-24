import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type historyActionCreate = genericObjectCreate;

export type historyActionRead = genericObjectRead;

export interface historyActionReadPage extends genericObjectReadPage {
  items: historyActionRead[];
}

export type historyActionUpdate = genericObjectUpdate;
