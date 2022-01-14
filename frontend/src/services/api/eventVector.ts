import {
  eventVectorCreate,
  eventVectorRead,
  eventVectorReadPage,
  eventVectorUpdate,
} from "@/models/eventVector";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/event/vector/";

export const EventVector = {
  create: (data: eventVectorCreate, getAfterCreate = false): Promise<void> => {
    return api.create(endpoint, data, getAfterCreate);
  },

  read: (uuid: UUID): Promise<eventVectorRead> => {
    return api.read(`${endpoint}${uuid}`);
  },

  readAll: (): Promise<eventVectorRead[]> => {
    return api.readAll(endpoint);
  },

  readPage: (params?: pageOptionParams): Promise<eventVectorReadPage> => {
    return api.read(`${endpoint}`, params);
  },

  update: (uuid: UUID, data: eventVectorUpdate): Promise<void> => {
    return api.update(`${endpoint}${uuid}`, data);
  },
};
