import {
  alertCreate,
  alertFilterParams,
  alertReadPage,
  alertTreeRead,
  alertUpdate,
} from "@/models/alert";
import { UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/alert/";

export const Alert = {
  create: (data: alertCreate, getAfterCreate = true): Promise<void> =>
    api.create(endpoint, data, getAfterCreate),

  read: (uuid: UUID): Promise<alertTreeRead> => api.read(`${endpoint}${uuid}`),

  readPage: (params?: alertFilterParams): Promise<alertReadPage> =>
    api.read(`${endpoint}`, params),

  update: (uuid: UUID, data: alertUpdate): Promise<void> =>
    api.update(`${endpoint}${uuid}`, data),
};
