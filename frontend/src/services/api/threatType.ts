import {
  threatTypeCreate,
  threatTypeRead,
  threatTypeUpdate,
} from "@/models/threatType";
import { UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/threat/type/";

export const ThreatType = {
  create: (data: threatTypeCreate, getAfterCreate = false): Promise<void> =>
    api.create(endpoint, data, getAfterCreate),

  read: (uuid: UUID): Promise<threatTypeRead> => api.read(`${endpoint}${uuid}`),

  readAll: (): Promise<threatTypeRead[]> => api.readAll(endpoint),

  update: (uuid: UUID, data: threatTypeUpdate): Promise<void> =>
    api.update(`${endpoint}${uuid}`, data),
};
