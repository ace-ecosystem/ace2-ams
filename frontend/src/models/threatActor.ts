import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
  queueableObjectCreate,
  queueableObjectRead,
  queueableObjectUpdate,
} from "./base";

export interface threatActorCreate
  extends genericObjectCreate,
    queueableObjectCreate {}

export interface threatActorRead
  extends genericObjectRead,
    queueableObjectRead {}

export interface threatActorReadPage extends genericObjectReadPage {
  items: threatActorRead[];
}

export interface threatActorUpdate
  extends genericObjectUpdate,
    queueableObjectUpdate {}
