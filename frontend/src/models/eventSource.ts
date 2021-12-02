import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type eventSourceCreate = genericObjectCreate;

export type eventSourceRead = genericObjectRead;

export interface eventSourceReadPage extends genericObjectReadPage {
  items: eventSourceRead[];
}

export type eventSourceUpdate = genericObjectUpdate;
