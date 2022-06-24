import { UUID } from "./base";
import { userRead } from "./user";

export interface alertCommentCreate {
  submissionUuid: UUID;
  uuid?: UUID;
  username: string;
  value: string;
  [key: string]: unknown;
}

export interface alertCommentRead {
  insertTime: string;
  submissionUuid: UUID;
  user: userRead;
  uuid: UUID;
  value: string;
}

export interface alertCommentUpdate {
  username: string;
  value: string;
  [key: string]: unknown;
}
