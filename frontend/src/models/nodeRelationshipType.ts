import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type nodeRelationshipTypeCreate = genericObjectCreate;

export type nodeRelationshipTypeRead = genericObjectRead;

export interface nodeRelationshipTypeReadPage extends genericObjectReadPage {
  items: nodeRelationshipTypeRead[];
}

export type nodeRelationshipTypeUpdate = genericObjectUpdate;
