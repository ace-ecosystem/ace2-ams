import {
  nodeTagCreate,
  nodeTagRead,
  nodeTagReadPage,
  nodeTagUpdate,
} from "@/models/nodeTag";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/node/tag/";

export const NodeTag = {
  create: (data: nodeTagCreate, getAfterCreate = false): Promise<void> =>
    api.create(endpoint, data, getAfterCreate),

  read: (uuid: UUID): Promise<nodeTagRead> => api.read(`${endpoint}${uuid}`),

  readAll: (): Promise<nodeTagRead[]> => api.readAll(endpoint),

  readPage: (params?: pageOptionParams): Promise<nodeTagReadPage> =>
    api.read(`${endpoint}`, params),

  update: (uuid: UUID, data: nodeTagUpdate): Promise<void> =>
    api.update(`${endpoint}${uuid}`, data),
};
