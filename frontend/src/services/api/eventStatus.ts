import {
  eventStatusCreate,
  eventStatusRead,
  eventStatusReadPage,
  eventStatusUpdate,
} from "@/models/eventStatus";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/event/status/";

export const EventStatus = {
  create: (data: eventStatusCreate, getAfterCreate = false): Promise<void> => {
    return api.create(endpoint, data, getAfterCreate);
  },

  read: (uuid: UUID): Promise<eventStatusRead> => {
    return api.read(`${endpoint}${uuid}`);
  },

  readAll: (): Promise<eventStatusRead[]> => {
    return api.readAll(endpoint);
  },

  readPage: (params?: pageOptionParams): Promise<eventStatusReadPage> => {
    return api.read(`${endpoint}`, params);
  },

  update: (uuid: UUID, data: eventStatusUpdate): Promise<void> => {
    return api.update(`${endpoint}${uuid}`, data);
  },
};
