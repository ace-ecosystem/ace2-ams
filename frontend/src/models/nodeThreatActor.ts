import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
  queueableObjectCreate,
  queueableObjectRead,
  queueableObjectUpdate,
} from "./base";

export interface nodeThreatActorCreate
  extends genericObjectCreate,
    queueableObjectCreate {}

export interface nodeThreatActorRead
  extends genericObjectRead,
    queueableObjectRead {}

export interface nodeThreatActorReadPage extends genericObjectReadPage {
  items: nodeThreatActorRead[];
}

export interface nodeThreatActorUpdate
  extends genericObjectUpdate,
    queueableObjectUpdate {}
