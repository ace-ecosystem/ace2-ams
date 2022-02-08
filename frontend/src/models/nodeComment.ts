import { UUID } from "./base";
import { userRead } from "./user";

export interface nodeCommentCreate {
  nodeUuid: UUID;
  uuid?: UUID;
  value: string;
  [key: string]: unknown;
}

export interface nodeCommentRead {
  insertTime: Date;
  nodeUuid: UUID;
  user: userRead;
  uuid: UUID;
  value: string;
}

export interface nodeCommentUpdate {
  uuid: UUID;
  value: string;
  [key: string]: unknown;
}
