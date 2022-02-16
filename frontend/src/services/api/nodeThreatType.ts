import {
  nodeThreatTypeCreate,
  nodeThreatTypeRead,
  nodeThreatTypeReadPage,
  nodeThreatTypeUpdate,
} from "@/models/nodeThreatType";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/node/threat/type/";

export const NodeThreatType = {
  create: (data: nodeThreatTypeCreate, getAfterCreate = false): Promise<void> =>
    api.create(endpoint, data, getAfterCreate),

  read: (uuid: UUID): Promise<nodeThreatTypeRead> =>
    api.read(`${endpoint}${uuid}`),

  readAll: (): Promise<nodeThreatTypeRead[]> => api.readAll(endpoint),

  readPage: (params?: pageOptionParams): Promise<nodeThreatTypeReadPage> =>
    api.read(`${endpoint}`, params),

  update: (uuid: UUID, data: nodeThreatTypeUpdate): Promise<void> =>
    api.update(`${endpoint}${uuid}`, data),
};
