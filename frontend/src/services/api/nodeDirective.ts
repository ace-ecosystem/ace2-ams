import {
  nodeDirectiveCreate,
  nodeDirectiveRead,
  nodeDirectiveReadPage,
  nodeDirectiveUpdate,
} from "@/models/nodeDirective";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/node/directive/";

export const NodeDirective = {
  create: (data: nodeDirectiveCreate, getAfterCreate = false): Promise<void> =>
    api.create(endpoint, data, getAfterCreate),

  read: (uuid: UUID): Promise<nodeDirectiveRead> =>
    api.read(`${endpoint}${uuid}`),

  readAll: (): Promise<nodeDirectiveRead[]> => api.readAll(endpoint),

  readPage: (params?: pageOptionParams): Promise<nodeDirectiveReadPage> =>
    api.read(`${endpoint}`, params),

  update: (uuid: UUID, data: nodeDirectiveUpdate): Promise<void> =>
    api.update(`${endpoint}${uuid}`, data),
};
