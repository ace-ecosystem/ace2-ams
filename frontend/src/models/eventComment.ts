import { UUID } from "./base";
import { userRead } from "./user";

export interface eventCommentCreate {
  eventUuid: UUID;
  uuid?: UUID;
  username: string;
  value: string;
  [key: string]: unknown;
}

export interface eventCommentRead {
  insertTime: string;
  eventUuid: UUID;
  user: userRead;
  uuid: UUID;
  value: string;
}

export interface eventCommentUpdate {
  username: string;
  value: string;
  [key: string]: unknown;
}
