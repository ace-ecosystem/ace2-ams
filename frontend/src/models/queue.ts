import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type queueCreate = genericObjectCreate;

export type queueRead = genericObjectRead;

export interface queueReadPage extends genericObjectReadPage {
  items: queueRead[];
}

export type queueUpdate = genericObjectUpdate;
