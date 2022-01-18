import {
  eventSourceCreate,
  eventSourceRead,
  eventSourceReadPage,
  eventSourceUpdate,
} from "@/models/eventSource";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/event/source/";

export const EventSource = {
  create: (data: eventSourceCreate, getAfterCreate = false): Promise<void> => {
    return api.create(endpoint, data, getAfterCreate);
  },

  read: (uuid: UUID): Promise<eventSourceRead> => {
    return api.read(`${endpoint}${uuid}`);
  },

  readAll: (): Promise<eventSourceRead[]> => {
    return api.readAll(endpoint);
  },

  readPage: (params?: pageOptionParams): Promise<eventSourceReadPage> => {
    return api.read(`${endpoint}`, params);
  },

  update: (uuid: UUID, data: eventSourceUpdate): Promise<void> => {
    return api.update(`${endpoint}${uuid}`, data);
  },
};
