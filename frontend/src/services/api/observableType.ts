import {
  observableTypeCreate,
  observableTypeRead,
  observableTypeReadPage,
  observableTypeUpdate,
} from "@/models/observableType";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/observable/type/";

export const ObservableType = {
  create: (data: observableTypeCreate, getAfterCreate = false): Promise<void> =>
    api.create(endpoint, data, getAfterCreate),

  read: (uuid: UUID): Promise<observableTypeRead> =>
    api.read(`${endpoint}${uuid}`),

  readAll: (): Promise<observableTypeRead[]> => api.readAll(endpoint),

  readPage: (params?: pageOptionParams): Promise<observableTypeReadPage> =>
    api.read(`${endpoint}`, params),

  update: (uuid: UUID, data: observableTypeUpdate): Promise<void> =>
    api.update(`${endpoint}${uuid}`, data),
};
