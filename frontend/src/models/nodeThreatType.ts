import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
  queueableObjectCreate,
  queueableObjectRead,
  queueableObjectUpdate,
} from "./base";

export interface nodeThreatTypeCreate
  extends genericObjectCreate,
    queueableObjectCreate {}

export interface nodeThreatTypeRead
  extends genericObjectRead,
    queueableObjectRead {}

export interface nodeThreatTypeReadPage extends genericObjectReadPage {
  items: nodeThreatTypeRead[];
}

export interface nodeThreatTypeUpdate
  extends genericObjectUpdate,
    queueableObjectUpdate {}
