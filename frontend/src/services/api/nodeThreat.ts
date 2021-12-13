import {
  nodeThreatCreate,
  nodeThreatRead,
  nodeThreatReadPage,
  nodeThreatUpdate,
} from "@/models/nodeThreat";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/node/threat/";

export const NodeThreat = {
  create: (data: nodeThreatCreate, getAfterCreate = false): Promise<void> =>
    api.create(endpoint, data, getAfterCreate),

  read: (uuid: UUID): Promise<nodeThreatRead> => api.read(`${endpoint}${uuid}`),

  readAll: (): Promise<nodeThreatRead[]> => api.readAll(endpoint),

  readPage: (params?: pageOptionParams): Promise<nodeThreatReadPage> =>
    api.read(`${endpoint}`, params),

  update: (uuid: UUID, data: nodeThreatUpdate): Promise<void> =>
    api.update(`${endpoint}${uuid}`, data),
};
