import { Component } from "vue";
import { analysisTreeRead } from "./analysis";
import {
  analysisMetadataCreate,
  analysisMetadataRead,
} from "./analysisMetadata";
import { historyUsername, UUID } from "./base";
import { metadataTagRead } from "./metadataTag";
import { nodeCreate, nodeRead, nodeUpdate } from "./node";
import { nodeCommentRead } from "./nodeComment";
import { nodeDetectionPointRead } from "./nodeDetectionPoint";
import { nodeRelationshipRead } from "./nodeRelationship";
import { nodeThreatRead } from "./nodeThreat";
import { nodeThreatActorRead } from "./nodeThreatActor";
import { observableTypeRead } from "./observableType";

export interface dispositionHistoryIndividual {
  disposition: string;
  count: number;
  percent: number;
}

export interface observableCreate extends nodeCreate, historyUsername {
  // The backend API actually allows you to specify a list of AnalysisCreate objects
  // when creating an observable, but we have not exposed that functionality in the GUI (yet).
  analysisMetadata?: analysisMetadataCreate[];
  context?: string;
  expiresOn?: Date;
  forDetection?: boolean;
  parentAnalysisUuid: UUID;
  tags?: string[];
  threatActors?: string[];
  threats?: string[];
  type: string;
  value: string;
  [key: string]: unknown;
}

export interface observableRead extends nodeRead {
  comments: nodeCommentRead[];
  context: string | null;
  detectionPoints: nodeDetectionPointRead[];
  expiresOn: string | null;
  forDetection: boolean;
  observableRelationships: observableRelationshipRead[];
  permanentTags: metadataTagRead[];
  threatActors: nodeThreatActorRead[];
  threats: nodeThreatRead[];
  type: observableTypeRead;
  value: string;
}

export interface observableInAlertRead extends observableRead {
  analysisMetadata: analysisMetadataRead;
  dispositionHistory: dispositionHistoryIndividual[];
}

export interface observableReadPage {
  items: observableRead[];
  limit: number;
  offset: number;
  total: number;
}

export interface observableTreeRead extends observableInAlertRead {
  children: analysisTreeRead[];
  firstAppearance?: boolean;
}

export interface observableUpdate extends nodeUpdate, historyUsername {
  context?: string;
  expiresOn?: Date | null;
  forDetection?: boolean;
  tags?: string[];
  threatActors?: string[];
  threats?: string[];
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
