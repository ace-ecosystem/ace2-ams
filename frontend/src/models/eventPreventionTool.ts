import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
  queueableObjectCreate,
  queueableObjectRead,
  queueableObjectUpdate,
} from "./base";

export interface eventPreventionToolCreate
  extends genericObjectCreate,
    queueableObjectCreate {}

export interface eventPreventionToolRead
  extends genericObjectRead,
    queueableObjectRead {}

export interface eventPreventionToolReadPage extends genericObjectReadPage {
  items: eventPreventionToolRead[];
}

export interface eventPreventionToolUpdate
  extends genericObjectUpdate,
    queueableObjectUpdate {}
