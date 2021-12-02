import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type observableTypeCreate = genericObjectCreate;

export type observableTypeRead = genericObjectRead;

export interface observableTypeReadPage extends genericObjectReadPage {
  items: observableTypeRead[];
}

export type observableTypeUpdate = genericObjectUpdate;
