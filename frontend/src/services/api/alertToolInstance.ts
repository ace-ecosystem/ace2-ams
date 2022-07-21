import {
  alertToolInstanceCreate,
  alertToolInstanceRead,
  alertToolInstanceReadPage,
  alertToolInstanceUpdate,
} from "@/models/alertToolInstance";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/alert/tool/instance/";

export const AlertToolInstance = {
  create: (
    data: alertToolInstanceCreate,
    getAfterCreate = false,
  ): Promise<void> => {
    return api.create(endpoint, data, getAfterCreate);
  },

  read: (uuid: UUID): Promise<alertToolInstanceRead> => {
    return api.read(`${endpoint}${uuid}`);
  },

  readAll: (): Promise<alertToolInstanceRead[]> => {
    return api.readAll(endpoint);
  },

  readPage: (params?: pageOptionParams): Promise<alertToolInstanceReadPage> => {
    return api.read(`${endpoint}`, params);
  },

  update: (uuid: UUID, data: alertToolInstanceUpdate): Promise<void> => {
    return api.update(`${endpoint}${uuid}`, data);
  },
};
