import { threatCreate, threatRead, threatUpdate } from "@/models/threat";
import { UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/threat/";

export const Threat = {
  create: (data: threatCreate, getAfterCreate = false): Promise<void> =>
    api.create(endpoint, data, getAfterCreate),

  read: (uuid: UUID): Promise<threatRead> => api.read(`${endpoint}${uuid}`),

  readAll: (): Promise<threatRead[]> => api.readAll(endpoint),

  update: (uuid: UUID, data: threatUpdate): Promise<void> =>
    api.update(`${endpoint}${uuid}`, data),
};
