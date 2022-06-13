import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
  queueableObjectCreate,
  queueableObjectRead,
  queueableObjectUpdate,
} from "./base";

export interface eventSeverityCreate
  extends genericObjectCreate,
    queueableObjectCreate {}

export interface eventSeverityRead
  extends genericObjectRead,
    queueableObjectRead {}

export interface eventSeverityReadPage extends genericObjectReadPage {
  items: eventSeverityRead[];
}

export interface eventSeverityUpdate
  extends genericObjectUpdate,
    queueableObjectUpdate {}
