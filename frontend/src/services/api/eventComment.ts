import { commentCreate, commentRead, commentUpdate } from "@/models/comment";
import { UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/event/comment/";

export const EventComment = {
  create: (data: commentCreate[], getAfterCreate = false): Promise<void> =>
    api.create(endpoint, data, getAfterCreate),

  read: (uuid: UUID): Promise<commentRead> => api.read(`${endpoint}${uuid}`),

  update: (uuid: UUID, data: commentUpdate): Promise<void> =>
    api.update(`${endpoint}${uuid}`, data),
};
