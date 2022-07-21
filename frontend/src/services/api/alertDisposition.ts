import {
  alertDispositionCreate,
  alertDispositionRead,
  alertDispositionReadPage,
  alertDispositionUpdate,
} from "@/models/alertDisposition";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/alert/disposition/";

export const AlertDisposition = {
  create: (
    data: alertDispositionCreate,
    getAfterCreate = false,
  ): Promise<void> => {
    return api.create(endpoint, data, getAfterCreate);
  },

  read: (uuid: UUID): Promise<alertDispositionRead> => {
    return api.read(`${endpoint}${uuid}`);
  },

  readAll: (): Promise<alertDispositionRead[]> => {
    return api.readAll(endpoint);
  },

  readPage: (params?: pageOptionParams): Promise<alertDispositionReadPage> => {
    return api.read(`${endpoint}`, params);
  },

  update: (uuid: UUID, data: alertDispositionUpdate): Promise<void> => {
    return api.update(`${endpoint}${uuid}`, data);
  },
};
