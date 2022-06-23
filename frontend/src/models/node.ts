import { UUID } from "./base";
import { readPage } from "./page";

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
  uuid: UUID;
  version: UUID;
}

export interface nodeReadPage extends readPage {
  items: nodeRead[];
}

export interface nodeUpdate {
  version?: UUID;
}

export interface nodeTreeCreate {
  rootNodeUuid: UUID;
  parentTreeUuid?: UUID;
}
