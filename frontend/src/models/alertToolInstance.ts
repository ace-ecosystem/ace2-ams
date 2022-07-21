import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type alertToolInstanceCreate = genericObjectCreate;

export type alertToolInstanceRead = genericObjectRead;

export interface alertToolInstanceReadPage extends genericObjectReadPage {
  items: alertToolInstanceRead[];
}

export type alertToolInstanceUpdate = genericObjectUpdate;
