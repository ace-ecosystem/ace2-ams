import { analysisTreeRead } from "./analysis";
import { UUID } from "./base";
import { nodeCreate, nodeRead, nodeTreeCreate, nodeUpdate } from "./node";
import { observableTypeRead } from "./observableType";

export interface observableCreate extends nodeCreate {
  context?: string;
  expiresOn?: Date;
  forDetection?: boolean;
  nodeTree: nodeTreeCreate;
  redirectionUuid?: UUID;
  time?: Date;
  type: string;
  value: string;
  [key: string]: unknown;
}

export interface observableRead extends nodeRead {
  context: string | null;
  expiresOn: Date | null;
  forDetection: boolean;
  redirectionUuid: UUID | null;
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
  parentTreeUuid: UUID | null;
  treeUuid: UUID;
}

export interface observableUpdate extends nodeUpdate {
  context?: string;
  expiresOn?: Date;
  forDetection?: boolean;
  redirectionUuid?: UUID;
  time?: Date;
  type?: string;
  value?: string;
  [key: string]: unknown;
}
