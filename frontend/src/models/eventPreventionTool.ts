import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type eventPreventionToolCreate = genericObjectCreate;

export type eventPreventionToolRead = genericObjectRead;

export interface eventPreventionToolReadPage extends genericObjectReadPage {
  items: eventPreventionToolRead[];
}

export type eventPreventionToolUpdate = genericObjectUpdate;
