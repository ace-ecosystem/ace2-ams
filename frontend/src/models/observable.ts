import { analysisTreeRead } from "./analysis";
import { UUID } from "./base";
import {
  nodeCreate,
  nodeMetadata,
  nodeRead,
  nodeTreeCreate,
  nodeUpdate,
} from "./node";
import { nodeCommentRead } from "./nodeComment";
import { nodeDirectiveRead } from "./nodeDirective";
import { nodeTagRead } from "./nodeTag";
import { nodeThreatRead } from "./nodeThreat";
import { nodeThreatActorRead } from "./nodeThreatActor";
import { observableTypeRead } from "./observableType";

export interface observableCreate extends nodeCreate {
  context?: string;
  directives?: string[];
  expiresOn?: Date;
  forDetection?: boolean;
  nodeTree: nodeTreeCreate;
  redirectionUuid?: UUID;
  tags?: string[];
  threatActors?: string[];
  threats?: string[];
  time?: Date;
  type: string;
  value: string;
  [key: string]: unknown;
}

export interface observableRead extends nodeRead {
  comments: nodeCommentRead[];
  context: string | null;
  directives: nodeDirectiveRead[];
  expiresOn: Date | null;
  forDetection: boolean;
  redirectionUuid: UUID | null;
  tags: nodeTagRead[];
  threatActors: nodeThreatActorRead[];
  threats: nodeThreatRead[];
  time: Date;
  type: observableTypeRead;
  value: string;
}

export interface observableReadPage {
  items: observableRead[];
  limit: number;
  offset: number;
  total: number;
}

export interface observableTreeRead extends observableRead {
  children: analysisTreeRead[];
  firstAppearance?: boolean;
  nodeMetadata?: nodeMetadata;
  parentTreeUuid: UUID | null;
  treeUuid: UUID;
}

export interface observableUpdate extends nodeUpdate {
  context?: string;
  directives?: string[];
  expiresOn?: Date;
  forDetection?: boolean;
  redirectionUuid?: UUID;
  tags?: string[];
  threatActors?: string[];
  threats?: string[];
  time?: Date;
  type?: string;
  value?: string;
  [key: string]: unknown;
}
