import { tagCreate, tagRead, tagReadPage, tagUpdate } from "@/models/tag";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/tag/";

export const Tag = {
  create: (data: tagCreate, getAfterCreate = false): Promise<void> =>
    api.create(endpoint, data, getAfterCreate),

  read: (uuid: UUID): Promise<tagRead> => api.read(`${endpoint}${uuid}`),

  readAll: (): Promise<tagRead[]> => api.readAll(endpoint),

  readPage: (params?: pageOptionParams): Promise<tagReadPage> =>
    api.read(`${endpoint}`, params),

  update: (uuid: UUID, data: tagUpdate): Promise<void> =>
    api.update(`${endpoint}${uuid}`, data),
};