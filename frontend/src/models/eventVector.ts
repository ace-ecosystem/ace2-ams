import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
  queueableObjectCreate,
  queueableObjectRead,
  queueableObjectUpdate,
} from "./base";

export interface eventVectorCreate
  extends genericObjectCreate,
    queueableObjectCreate {}

export interface eventVectorRead
  extends genericObjectRead,
    queueableObjectRead {}

export interface eventVectorReadPage extends genericObjectReadPage {
  items: eventVectorRead[];
}

export interface eventVectorUpdate
  extends genericObjectUpdate,
    queueableObjectUpdate {}
