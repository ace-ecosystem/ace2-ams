import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type observableRelationshipTypeCreate = genericObjectCreate;

export type observableRelationshipTypeRead = genericObjectRead;

export interface observableRelationshipTypeReadPage extends genericObjectReadPage {
  items: observableRelationshipTypeRead[];
}

export type observableRelationshipTypeUpdate = genericObjectUpdate;
