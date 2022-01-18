import {
  eventPreventionToolCreate,
  eventPreventionToolRead,
  eventPreventionToolReadPage,
  eventPreventionToolUpdate,
} from "@/models/eventPreventionTool";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/event/prevention_tool/";

export const EventPreventionTool = {
  create: (
    data: eventPreventionToolCreate,
    getAfterCreate = false,
  ): Promise<void> => {
    return api.create(endpoint, data, getAfterCreate);
  },

  read: (uuid: UUID): Promise<eventPreventionToolRead> => {
    return api.read(`${endpoint}${uuid}`);
  },

  readAll: (): Promise<eventPreventionToolRead[]> => {
    return api.readAll(endpoint);
  },

  readPage: (
    params?: pageOptionParams,
  ): Promise<eventPreventionToolReadPage> => {
    return api.read(`${endpoint}`, params);
  },

  update: (uuid: UUID, data: eventPreventionToolUpdate): Promise<void> => {
    return api.update(`${endpoint}${uuid}`, data);
  },
};
