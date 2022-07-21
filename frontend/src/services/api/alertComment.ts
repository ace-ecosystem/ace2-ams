import {
  alertCommentCreate,
  alertCommentRead,
  alertCommentUpdate,
} from "@/models/alertComment";
import { UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/alert/comment/";

export const AlertComment = {
  create: (data: alertCommentCreate[], getAfterCreate = false): Promise<void> =>
    api.create(endpoint, data, getAfterCreate),

  read: (uuid: UUID): Promise<alertCommentRead> =>
    api.read(`${endpoint}${uuid}`),

  update: (uuid: UUID, data: alertCommentUpdate): Promise<void> =>
    api.update(`${endpoint}${uuid}`, data),
};
