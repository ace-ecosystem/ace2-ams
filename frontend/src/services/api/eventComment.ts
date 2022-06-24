import {
  eventCommentCreate,
  eventCommentRead,
  eventCommentUpdate,
} from "@/models/eventComment";
import { UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/event/comment/";

export const EventComment = {
  create: (data: eventCommentCreate[], getAfterCreate = false): Promise<void> =>
    api.create(endpoint, data, getAfterCreate),

  read: (uuid: UUID): Promise<eventCommentRead> =>
    api.read(`${endpoint}${uuid}`),

  update: (uuid: UUID, data: eventCommentUpdate): Promise<void> =>
    api.update(`${endpoint}${uuid}`, data),
};
