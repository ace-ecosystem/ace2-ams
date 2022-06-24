import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
  queueableObjectCreate,
  queueableObjectRead,
  queueableObjectUpdate,
} from "./base";

import { threatTypeRead } from "./threatType";

export interface threatCreate
  extends genericObjectCreate,
    queueableObjectCreate {
  types: string[];
}

export interface threatRead extends genericObjectRead, queueableObjectRead {
  types: threatTypeRead[];
}

export interface threatReadPage extends genericObjectReadPage {
  items: threatRead[];
}

export interface threatUpdate
  extends genericObjectUpdate,
    queueableObjectUpdate {
  types?: string[];
}
