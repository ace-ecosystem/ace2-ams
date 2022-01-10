import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type eventQueueCreate = genericObjectCreate;

export type eventQueueRead = genericObjectRead;

export interface eventQueueReadPage extends genericObjectReadPage {
  items: eventQueueRead[];
}

export type eventQueueUpdate = genericObjectUpdate;
