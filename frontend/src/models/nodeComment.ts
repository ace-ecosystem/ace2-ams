import { UUID } from "./base";
import { userRead } from "./user";

export interface nodeCommentCreate {
  nodeUuid: UUID;
  user: string;
  uuid?: UUID;
  value: string;
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
}
