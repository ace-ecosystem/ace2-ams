import {
  threatActorCreate,
  threatActorRead,
  threatActorUpdate,
} from "@/models/threatActor";
import { UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/threat_actor/";

export const ThreatActor = {
  create: (data: threatActorCreate, getAfterCreate = false): Promise<void> =>
    api.create(endpoint, data, getAfterCreate),

  read: (uuid: UUID): Promise<threatActorRead> =>
    api.read(`${endpoint}${uuid}`),

  readAll: (): Promise<threatActorRead[]> => api.readAll(endpoint),

  update: (uuid: UUID, data: threatActorUpdate): Promise<void> =>
    api.update(`${endpoint}${uuid}`, data),
};
