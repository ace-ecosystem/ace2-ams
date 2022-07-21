import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
  queueableObjectCreate,
  queueableObjectRead,
  queueableObjectUpdate,
} from "./base";

export interface eventRemediationCreate
  extends genericObjectCreate,
    queueableObjectCreate {}

export interface eventRemediationRead
  extends genericObjectRead,
    queueableObjectRead {}

export interface eventRemediationReadPage extends genericObjectReadPage {
  items: eventRemediationRead[];
}

export interface eventRemediationUpdate
  extends genericObjectUpdate,
    queueableObjectUpdate {}
