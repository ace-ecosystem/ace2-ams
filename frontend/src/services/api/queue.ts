import {
  queueCreate,
  queueRead,
  queueReadPage,
  queueUpdate,
} from "@/models/queue";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/queue/";

export const queue = {
  create: (data: queueCreate, getAfterCreate = false): Promise<void> => {
    return api.create(endpoint, data, getAfterCreate);
  },

  read: (uuid: UUID): Promise<queueRead> => {
    return api.read(`${endpoint}${uuid}`);
  },

  readAll: (): Promise<queueRead[]> => {
    return api.readAll(endpoint);
  },

  readPage: (params?: pageOptionParams): Promise<queueReadPage> => {
    return api.read(`${endpoint}`, params);
  },

  update: (uuid: UUID, data: queueUpdate): Promise<void> => {
    return api.update(`${endpoint}${uuid}`, data);
  },
};
