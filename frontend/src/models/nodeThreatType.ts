import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type nodeThreatTypeCreate = genericObjectCreate;

export type nodeThreatTypeRead = genericObjectRead;

export interface nodeThreatTypeReadPage extends genericObjectReadPage {
  items: nodeThreatTypeRead[];
}

export type nodeThreatTypeUpdate = genericObjectUpdate;
