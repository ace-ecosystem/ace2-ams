import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type eventTypeCreate = genericObjectCreate;

export type eventTypeRead = genericObjectRead;

export interface eventTypeReadPage extends genericObjectReadPage {
  items: eventTypeRead[];
}

export type eventTypeUpdate = genericObjectUpdate;
