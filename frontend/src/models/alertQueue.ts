import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type alertQueueCreate = genericObjectCreate;

export type alertQueueRead = genericObjectRead;

export interface alertQueueReadPage extends genericObjectReadPage {
  items: alertQueueRead[];
}

export type alertQueueUpdate = genericObjectUpdate;
