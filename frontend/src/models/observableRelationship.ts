import { UUID } from "./base";
import { observableRead } from "./observable";
import { observableRelationshipTypeRead } from "./observableRelationshipType";

export interface observableRelationshipCreate {
  observableUuid: UUID;
  relatedObservableUuid: UUID;
  type: string;
  uuid?: UUID;
  [key: string]: unknown;
}

export interface observableRelationshipRead {
  observableUuid: UUID;
  relatedObservable: observableRead;
  uuid: UUID;
  type: observableRelationshipTypeRead;
}
