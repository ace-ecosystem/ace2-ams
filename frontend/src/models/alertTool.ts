import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type alertToolCreate = genericObjectCreate;

export type alertToolRead = genericObjectRead;

export interface alertToolReadPage extends genericObjectReadPage {
  items: alertToolRead[];
}

export type alertToolUpdate = genericObjectUpdate;
