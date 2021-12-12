import {
  nodeThreatActorCreate,
  nodeThreatActorRead,
  nodeThreatActorReadPage,
  nodeThreatActorUpdate,
} from "@/models/nodeThreatActor";
import { pageOptionParams, UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/node/threat_actor/";

export const NodeThreatActor = {
  create: (
    data: nodeThreatActorCreate,
    getAfterCreate = false,
  ): Promise<void> => api.create(endpoint, data, getAfterCreate),

  read: (uuid: UUID): Promise<nodeThreatActorRead> =>
    api.read(`${endpoint}${uuid}`),

  readAll: (): Promise<nodeThreatActorRead[]> => api.readAll(endpoint),

  readPage: (params?: pageOptionParams): Promise<nodeThreatActorReadPage> =>
    api.read(`${endpoint}`, params),

  update: (uuid: UUID, data: nodeThreatActorUpdate): Promise<void> =>
    api.update(`${endpoint}${uuid}`, data),
};
