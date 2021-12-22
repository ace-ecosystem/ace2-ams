import { UUID } from "./base";

export interface nodeCreate {
  uuid?: UUID;
  version?: UUID;
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
