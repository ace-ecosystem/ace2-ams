import {
  eventQueueCreate,
  eventQueueRead,
  eventQueueReadPage,
  eventQueueUpdate,
} from "@/models/eventQueue";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/event/queue/";

export const EventQueue = {
  create: (data: eventQueueCreate, getAfterCreate = false): Promise<void> => {
    return api.create(endpoint, data, getAfterCreate);
  },

  read: (uuid: UUID): Promise<eventQueueRead> => {
    return api.read(`${endpoint}${uuid}`);
  },

  readAll: (): Promise<eventQueueRead[]> => {
    return api.readAll(endpoint);
  },

  readPage: (params?: pageOptionParams): Promise<eventQueueReadPage> => {
    return api.read(`${endpoint}`, params);
  },

  update: (uuid: UUID, data: eventQueueUpdate): Promise<void> => {
    return api.update(`${endpoint}${uuid}`, data);
  },
};
