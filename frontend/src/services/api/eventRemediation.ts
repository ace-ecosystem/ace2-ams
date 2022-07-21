import {
  eventRemediationCreate,
  eventRemediationRead,
  eventRemediationReadPage,
  eventRemediationUpdate,
} from "@/models/eventRemediation";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/event/remediation/";

export const EventRemediation = {
  create: (
    data: eventRemediationCreate,
    getAfterCreate = false,
  ): Promise<void> => {
    return api.create(endpoint, data, getAfterCreate);
  },

  read: (uuid: UUID): Promise<eventRemediationRead> => {
    return api.read(`${endpoint}${uuid}`);
  },

  readAll: (): Promise<eventRemediationRead[]> => {
    return api.readAll(endpoint);
  },

  readPage: (params?: pageOptionParams): Promise<eventRemediationReadPage> => {
    return api.read(`${endpoint}`, params);
  },

  update: (uuid: UUID, data: eventRemediationUpdate): Promise<void> => {
    return api.update(`${endpoint}${uuid}`, data);
  },
};
