import {
  nodeCommentCreate,
  nodeCommentRead,
  nodeCommentUpdate,
} from "@/models/nodeComment";
import { UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/node/comment/";

export const NodeComment = {
  create: (data: nodeCommentCreate, getAfterCreate = false): Promise<void> =>
    api.create(endpoint, data, getAfterCreate),

  read: (uuid: UUID): Promise<nodeCommentRead> =>
    api.read(`${endpoint}${uuid}`),

  readAll: (): Promise<nodeCommentRead[]> => api.readAll(endpoint),

  update: (uuid: UUID, data: nodeCommentUpdate): Promise<void> =>
    api.update(`${endpoint}${uuid}`, data),
};
