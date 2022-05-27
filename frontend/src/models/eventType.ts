import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
  queueableObjectCreate,
  queueableObjectRead,
  queueableObjectUpdate,
} from "./base";

export interface eventTypeCreate
  extends genericObjectCreate,
    queueableObjectCreate {}

export interface eventTypeRead extends genericObjectRead, queueableObjectRead {}

export interface eventTypeReadPage extends genericObjectReadPage {
  items: eventTypeRead[];
}

export interface eventTypeUpdate
  extends genericObjectUpdate,
    queueableObjectUpdate {}
