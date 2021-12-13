import {
  alertToolCreate,
  alertToolRead,
  alertToolReadPage,
  alertToolUpdate,
} from "@/models/alertTool";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/alert/tool/";

export const AlertTool = {
  create: (data: alertToolCreate, getAfterCreate = false): Promise<void> => {
    return api.create(endpoint, data, getAfterCreate);
  },

  read: (uuid: UUID): Promise<alertToolRead> => {
    return api.read(`${endpoint}${uuid}`);
  },

  readAll: (): Promise<alertToolRead[]> => {
    return api.readAll(endpoint);
  },

  readPage: (params?: pageOptionParams): Promise<alertToolReadPage> => {
    return api.read(`${endpoint}`, params);
  },

  update: (uuid: UUID, data: alertToolUpdate): Promise<void> => {
    return api.update(`${endpoint}${uuid}`, data);
  },
};
