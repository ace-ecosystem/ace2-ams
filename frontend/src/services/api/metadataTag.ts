import {
  metadataTagCreate,
  metadataTagRead,
  metadataTagReadPage,
  metadataTagUpdate,
} from "@/models/metadataTag";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/metadata/tag/";

export const MetadataTag = {
  create: (data: metadataTagCreate, getAfterCreate = false): Promise<void> =>
    api.create(endpoint, data, getAfterCreate),

  read: (uuid: UUID): Promise<metadataTagRead> =>
    api.read(`${endpoint}${uuid}`),

  readAll: (): Promise<metadataTagRead[]> => api.readAll(endpoint),

  readPage: (params?: pageOptionParams): Promise<metadataTagReadPage> =>
    api.read(`${endpoint}`, params),

  update: (uuid: UUID, data: metadataTagUpdate): Promise<void> =>
    api.update(`${endpoint}${uuid}`, data),
};
