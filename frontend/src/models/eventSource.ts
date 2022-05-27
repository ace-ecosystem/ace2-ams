import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
  queueableObjectCreate,
  queueableObjectRead,
  queueableObjectUpdate,
} from "./base";

export interface eventSourceCreate
  extends genericObjectCreate,
    queueableObjectCreate {}

export interface eventSourceRead
  extends genericObjectRead,
    queueableObjectRead {}

export interface eventSourceReadPage extends genericObjectReadPage {
  items: eventSourceRead[];
}

export interface eventSourceUpdate
  extends genericObjectUpdate,
    queueableObjectUpdate {}
