import {
  eventCreate,
  eventRead,
  eventReadPage,
  eventUpdate,
} from "@/models/event";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/event/";

export const Event = {
  create: (data: eventCreate, getAfterCreate = false): Promise<void> => {
    return api.create(endpoint, data, getAfterCreate);
  },

  read: (uuid: UUID): Promise<eventRead> => {
    return api.read(`${endpoint}${uuid}`);
  },

  readAll: (): Promise<eventRead[]> => {
    return api.readAll(endpoint);
  },

  readPage: (params?: pageOptionParams): Promise<eventReadPage> => {
    return api.read(`${endpoint}`, params);
  },

  update: (data: eventUpdate[]): Promise<void> => {
    return api.update(`${endpoint}`, data);
  },
};
