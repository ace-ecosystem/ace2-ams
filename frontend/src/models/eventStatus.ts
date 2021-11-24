import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type eventStatusCreate = genericObjectCreate;

export type eventStatusRead = genericObjectRead;

export interface eventStatusReadPage extends genericObjectReadPage {
  items: eventStatusRead[];
}

export type eventStatusUpdate = genericObjectUpdate;
