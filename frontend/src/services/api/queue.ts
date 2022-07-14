import { queueCreate, queueRead, queueUpdate } from "@/models/queue";
import { UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/queue/";

export const queue = {
  create: (data: queueCreate, getAfterCreate = false): Promise<void> => {
    return api.create(endpoint, data, getAfterCreate);
  },

  read: (uuid: UUID): Promise<queueRead> => {
    return api.read(`${endpoint}${uuid}`);
  },

  readAll: (): Promise<queueRead[]> => {
    return api.readAll(endpoint);
  },

  update: (uuid: UUID, data: queueUpdate): Promise<void> => {
    return api.update(`${endpoint}${uuid}`, data);
  },
};
