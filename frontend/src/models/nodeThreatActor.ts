import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type nodeThreatActorCreate = genericObjectCreate;

export type nodeThreatActorRead = genericObjectRead;

export interface nodeThreatActorReadPage extends genericObjectReadPage {
  items: nodeThreatActorRead[];
}

export type nodeThreatActorUpdate = genericObjectUpdate;
