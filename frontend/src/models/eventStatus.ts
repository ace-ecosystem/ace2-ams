import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
  queueableObjectCreate,
  queueableObjectRead,
  queueableObjectUpdate,
} from "./base";

export interface eventStatusCreate
  extends genericObjectCreate,
    queueableObjectCreate {}

export interface eventStatusRead
  extends genericObjectRead,
    queueableObjectRead {}

export interface eventStatusReadPage extends genericObjectReadPage {
  items: eventStatusRead[];
}

export interface eventStatusUpdate
  extends genericObjectUpdate,
    queueableObjectUpdate {}
