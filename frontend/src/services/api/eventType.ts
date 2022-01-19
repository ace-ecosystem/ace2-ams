import {
  eventTypeCreate,
  eventTypeRead,
  eventTypeReadPage,
  eventTypeUpdate,
} from "@/models/eventType";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/event/type/";

export const EventType = {
  create: (data: eventTypeCreate, getAfterCreate = false): Promise<void> => {
    return api.create(endpoint, data, getAfterCreate);
  },

  read: (uuid: UUID): Promise<eventTypeRead> => {
    return api.read(`${endpoint}${uuid}`);
  },

  readAll: (): Promise<eventTypeRead[]> => {
    return api.readAll(endpoint);
  },

  readPage: (params?: pageOptionParams): Promise<eventTypeReadPage> => {
    return api.read(`${endpoint}`, params);
  },

  update: (uuid: UUID, data: eventTypeUpdate): Promise<void> => {
    return api.update(`${endpoint}${uuid}`, data);
  },
};
