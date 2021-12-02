import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type alertTypeCreate = genericObjectCreate;

export type alertTypeRead = genericObjectRead;

export interface alertTypeReadPage extends genericObjectReadPage {
  items: alertTypeRead[];
}

export type alertTypeUpdate = genericObjectUpdate;
