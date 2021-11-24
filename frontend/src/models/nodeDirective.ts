import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type nodeDirectiveCreate = genericObjectCreate;

export type nodeDirectiveRead = genericObjectRead;

export interface nodeDirectiveReadPage extends genericObjectReadPage {
  items: nodeDirectiveRead[];
}

export type nodeDirectiveUpdate = genericObjectUpdate;
