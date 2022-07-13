import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type formatCreate = genericObjectCreate;

export type formatRead = genericObjectRead;

export interface formatReadPage extends genericObjectReadPage {
  items: formatRead[];
}

export type formatUpdate = genericObjectUpdate;
