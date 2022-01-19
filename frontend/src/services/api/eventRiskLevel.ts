import {
  eventRiskLevelCreate,
  eventRiskLevelRead,
  eventRiskLevelReadPage,
  eventRiskLevelUpdate,
} from "@/models/eventRiskLevel";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/event/risk_level/";

export const EventRiskLevel = {
  create: (
    data: eventRiskLevelCreate,
    getAfterCreate = false,
  ): Promise<void> => {
    return api.create(endpoint, data, getAfterCreate);
  },

  read: (uuid: UUID): Promise<eventRiskLevelRead> => {
    return api.read(`${endpoint}${uuid}`);
  },

  readAll: (): Promise<eventRiskLevelRead[]> => {
    return api.readAll(endpoint);
  },

  readPage: (params?: pageOptionParams): Promise<eventRiskLevelReadPage> => {
    return api.read(`${endpoint}`, params);
  },

  update: (uuid: UUID, data: eventRiskLevelUpdate): Promise<void> => {
    return api.update(`${endpoint}${uuid}`, data);
  },
};
