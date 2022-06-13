import {
  eventSeverityCreate,
  eventSeverityRead,
  eventSeverityReadPage,
  eventSeverityUpdate,
} from "@/models/eventSeverity";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/event/severity/";

export const EventSeverity = {
  create: (
    data: eventSeverityCreate,
    getAfterCreate = false,
  ): Promise<void> => {
    return api.create(endpoint, data, getAfterCreate);
  },

  read: (uuid: UUID): Promise<eventSeverityRead> => {
    return api.read(`${endpoint}${uuid}`);
  },

  readAll: (): Promise<eventSeverityRead[]> => {
    return api.readAll(endpoint);
  },

  readPage: (params?: pageOptionParams): Promise<eventSeverityReadPage> => {
    return api.read(`${endpoint}`, params);
  },

  update: (uuid: UUID, data: eventSeverityUpdate): Promise<void> => {
    return api.update(`${endpoint}${uuid}`, data);
  },
};
