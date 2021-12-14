import {
  analysisCreate,
  analysisRead,
  analysisUpdate,
} from "@/models/analysis";
import { UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/analysis/";

export const Analysis = {
  create: (data: analysisCreate, getAfterCreate = false): Promise<void> =>
    api.create(endpoint, data, getAfterCreate),

  read: (uuid: UUID): Promise<analysisRead> => api.read(`${endpoint}${uuid}`),

  update: (uuid: UUID, data: analysisUpdate): Promise<void> =>
    api.update(`${endpoint}${uuid}`, data),
};
