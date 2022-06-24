import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
  queueableObjectCreate,
  queueableObjectRead,
  queueableObjectUpdate,
} from "./base";

export interface threatTypeCreate
  extends genericObjectCreate,
    queueableObjectCreate {}

export interface threatTypeRead
  extends genericObjectRead,
    queueableObjectRead {}

export interface threatTypeReadPage extends genericObjectReadPage {
  items: threatTypeRead[];
}

export interface threatTypeUpdate
  extends genericObjectUpdate,
    queueableObjectUpdate {}
