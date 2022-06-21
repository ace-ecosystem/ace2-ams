import { UUID } from "./base";

export interface nodeDetectionPointCreate {
  nodeUuid: UUID;
  uuid?: UUID;
  value: string;
  [key: string]: unknown;
}

export interface nodeDetectionPointRead {
  insertTime: string;
  nodeUuid: UUID;
  uuid: UUID;
  value: string;
}

export interface nodeDetectionPointUpdate {
  uuid: UUID;
  value: string;
  [key: string]: unknown;
}
