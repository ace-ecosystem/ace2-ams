import { UUID } from "./base";
import { nodeRead } from "./node";
import { nodeRelationshipTypeRead } from "./nodeRelationshipType";

export interface nodeRelationshipCreate {
  nodeUuid: UUID;
  relatedNodeUuid: UUID;
  type: string;
  uuid?: UUID;
  [key: string]: unknown;
}

export interface nodeRelationshipRead {
  nodeUuid: UUID;
  relatedNode: nodeRead;
  uuid: UUID;
  type: nodeRelationshipTypeRead;
}
