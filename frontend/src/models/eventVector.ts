import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type eventVectorCreate = genericObjectCreate;

export type eventVectorRead = genericObjectRead;

export interface eventVectorReadPage extends genericObjectReadPage {
  items: eventVectorRead[];
}

export type eventVectorUpdate = genericObjectUpdate;
