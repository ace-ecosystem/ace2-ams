import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type eventRemediationCreate = genericObjectCreate;

export type eventRemediationRead = genericObjectRead;

export interface eventRemediationReadPage extends genericObjectReadPage {
  items: eventRemediationRead[];
}

export type eventRemediationUpdate = genericObjectUpdate;
