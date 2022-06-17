import {
  metadataDirectiveCreate,
  metadataDirectiveRead,
  metadataDirectiveReadPage,
  metadataDirectiveUpdate,
} from "@/models/metadataDirective";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/metadata/directive/";

export const MetadataDirective = {
  create: (
    data: metadataDirectiveCreate,
    getAfterCreate = false,
  ): Promise<void> => api.create(endpoint, data, getAfterCreate),

  read: (uuid: UUID): Promise<metadataDirectiveRead> =>
    api.read(`${endpoint}${uuid}`),

  readAll: (): Promise<metadataDirectiveRead[]> => api.readAll(endpoint),

  readPage: (params?: pageOptionParams): Promise<metadataDirectiveReadPage> =>
    api.read(`${endpoint}`, params),

  update: (uuid: UUID, data: metadataDirectiveUpdate): Promise<void> =>
    api.update(`${endpoint}${uuid}`, data),
};
