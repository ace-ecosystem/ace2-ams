import {
  alertTypeCreate,
  alertTypeRead,
  alertTypeReadPage,
  alertTypeUpdate,
} from "@/models/alertType";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/alert/type/";

export const AlertType = {
  create: (data: alertTypeCreate, getAfterCreate = false): Promise<void> =>
    api.create(endpoint, data, getAfterCreate),

  read: (uuid: UUID): Promise<alertTypeRead> => api.read(`${endpoint}${uuid}`),

  readAll: (): Promise<alertTypeRead[]> => api.readAll(endpoint),

  readPage: (params?: pageOptionParams): Promise<alertTypeReadPage> =>
    api.read(`${endpoint}`, params),

  update: (uuid: UUID, data: alertTypeUpdate): Promise<void> =>
    api.update(`${endpoint}${uuid}`, data),
};
