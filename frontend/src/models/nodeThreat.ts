import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

import { nodeThreatTypeRead } from "./nodeThreatType";

export interface nodeThreatCreate extends genericObjectCreate {
  types: string[];
}

export interface nodeThreatRead extends genericObjectRead {
  types: nodeThreatTypeRead[];
}

export interface nodeThreatReadPage extends genericObjectReadPage {
  items: nodeThreatRead[];
}

export interface nodeThreatUpdate extends genericObjectUpdate {
  types?: string[];
}
