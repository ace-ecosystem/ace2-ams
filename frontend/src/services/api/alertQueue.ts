import {
  alertQueueCreate,
  alertQueueRead,
  alertQueueReadPage,
  alertQueueUpdate,
} from "@/models/alertQueue";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/alert/queue/";

export const AlertQueue = {
  create: (data: alertQueueCreate, getAfterCreate = false): Promise<void> => {
    return api.create(endpoint, data, getAfterCreate);
  },

  read: (uuid: UUID): Promise<alertQueueRead> => {
    return api.read(`${endpoint}${uuid}`);
  },

  readAll: (): Promise<alertQueueRead[]> => {
    return api.readAll(endpoint);
  },

  readPage: (params?: pageOptionParams): Promise<alertQueueReadPage> => {
    return api.read(`${endpoint}`, params);
  },

  update: (uuid: UUID, data: alertQueueUpdate): Promise<void> => {
    return api.update(`${endpoint}${uuid}`, data);
  },
};
