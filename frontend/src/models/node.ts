import { UUID } from "./base";
import { nodeCommentRead } from "./nodeComment";
import { nodeDirectiveRead } from "./nodeDirective";
import { nodeTagRead } from "./nodeTag";
import { nodeThreatActorRead } from "./nodeThreatActor";
import { nodeThreatRead } from "./nodeThreat";

export interface nodeCreate {
  directives?: string[];
  tags?: string[];
  threatActor?: string;
  threats?: string[];
  uuid?: UUID;
  version?: UUID;
}

export interface nodeRead {
  comments: nodeCommentRead[];
  directives: nodeDirectiveRead[];
  nodeType: string;
  tags: nodeTagRead[];
  threatActor: nodeThreatActorRead | null;
  threats: nodeThreatRead[];
  uuid: UUID;
  version: UUID;
}

export interface nodeReadPage {
  items: nodeRead[];
  limit: number;
  offset: number;
  total: number;
}

export interface nodeUpdate {
  directives?: string[];
  tags?: string[];
  threatActor?: string;
  threats?: string[];
  version: UUID;
}

export interface nodeTreeCreate {
  rootNodeUuid: UUID;
  parentTreeUuid?: UUID;
}
