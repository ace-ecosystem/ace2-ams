import { Component } from "vue";
import { analysisTreeRead } from "./analysis";
import {
  analysisMetadataCreate,
  analysisMetadataRead,
} from "./analysisMetadata";
import { historyUsername, UUID } from "./base";
import { metadataTagRead } from "./metadataTag";
import { observableRelationshipRead } from "./observableRelationship";
import { observableTypeRead } from "./observableType";

export interface observableDispositionHistoryIndividual {
  disposition: string;
  count: number;
  percent: number;
}

export interface observableMatchingEventIndividual {
  status: string;
  count: number;
}

export interface observableCreateBase extends historyUsername {
  // The backend API actually allows you to specify a list of AnalysisCreate objects
  // when creating an observable, but we have not exposed that functionality in the GUI (yet).
  analysisMetadata?: analysisMetadataCreate[];
  context?: string;
  expiresOn?: Date;
  forDetection?: boolean;
  tags?: string[];
  type: string;
  value: string;
  whitelisted?: boolean;
  [key: string]: unknown;
}

export interface observableCreate extends observableCreateBase {
  parentAnalysisUuid: UUID;
  [key: string]: unknown;
}

export type observableCreateInAlert = observableCreateBase;

export interface observableRead {
  context: string | null;
  expiresOn: string | null;
  forDetection: boolean;
  objectType: string;
  observableRelationships: observableRelationshipRead[];
  tags: metadataTagRead[];
  type: observableTypeRead;
  uuid: UUID;
  value: string;
  version: UUID;
  whitelisted: boolean;
}

export interface observableInAlertRead extends observableRead {
  analysisMetadata: analysisMetadataRead;
  dispositionHistory: observableDispositionHistoryIndividual[];
  matchingEvents: observableMatchingEventIndividual[];
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

export interface observableUpdate extends historyUsername {
  context?: string;
  expiresOn?: Date | null;
  forDetection?: boolean;
  tags?: string[];
  type?: string;
  value?: string;
  version?: UUID;
  whitelisted?: boolean;
  [key: string]: unknown;
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
