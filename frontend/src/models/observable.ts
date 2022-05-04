import { Component } from "vue";
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
import { nodeDetectionPointRead } from "./nodeDetectionPoint";
import { nodeDirectiveRead } from "./nodeDirective";
import { nodeRelationshipRead } from "./nodeRelationship";
import { nodeTagRead } from "./nodeTag";
import { nodeThreatRead } from "./nodeThreat";
import { nodeThreatActorRead } from "./nodeThreatActor";
import { observableTypeRead } from "./observableType";

export interface observableCreate extends nodeCreate {
  context?: string;
  directives?: string[];
  expiresOn?: Date;
  forDetection?: boolean;
  nodeTree?: nodeTreeCreate;
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
  detectionPoints: nodeDetectionPointRead[];
  directives: nodeDirectiveRead[];
  expiresOn: Date | null;
  forDetection: boolean;
  observableRelationships: observableRelationshipRead[];
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
  expiresOn?: Date | null;
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

export interface observableRelationshipRead extends nodeRelationshipRead {
  relatedNode: observableRead;
}

export type observableAction = {
  type: "url" | "command" | "modal";
  label: string;
  description: string;
  icon: string;
  requirements?: (obs: observableTreeRead) => boolean;
};

export interface observableActionUrl extends observableAction {
  type: "url";
  url: string;
}
export interface observableActionCommand extends observableAction {
  type: "command";
  reloadPage: boolean;
  command: (obs: observableTreeRead) => unknown;
}

export interface observableActionModal extends observableAction {
  type: "modal";
  modal: Component;
  modalName: string;
}

export type observableActionSubTypes =
  | observableActionUrl
  | observableActionCommand
  | observableActionModal;

export type observableActionSection = {
  items: observableActionSubTypes[];
  label?: string;
};
