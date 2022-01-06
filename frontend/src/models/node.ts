import { UUID } from "./base";

export interface nodeCreate {
  uuid?: UUID;
  version?: UUID;
}

interface nodeMetadataDisplay {
  type?: string;
  value?: string;
}

export interface nodeMetadata {
  display?: nodeMetadataDisplay;
}

export interface nodeRead {
  nodeType: string;
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
  version?: UUID;
}

export interface nodeTreeCreate {
  rootNodeUuid: UUID;
  parentTreeUuid?: UUID;
}
