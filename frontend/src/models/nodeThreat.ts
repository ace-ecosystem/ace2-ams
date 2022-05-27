import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
  queueableObjectCreate,
  queueableObjectRead,
  queueableObjectUpdate,
} from "./base";

import { nodeThreatTypeRead } from "./nodeThreatType";

export interface nodeThreatCreate
  extends genericObjectCreate,
    queueableObjectCreate {
  types: string[];
}

export interface nodeThreatRead extends genericObjectRead, queueableObjectRead {
  types: nodeThreatTypeRead[];
}

export interface nodeThreatReadPage extends genericObjectReadPage {
  items: nodeThreatRead[];
}

export interface nodeThreatUpdate
  extends genericObjectUpdate,
    queueableObjectUpdate {
  types?: string[];
}
