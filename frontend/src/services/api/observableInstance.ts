import {
  observableInstanceCreate,
  observableInstanceRead,
  observableInstanceUpdate,
} from "@/models/observableInstance";
import { UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/observable/instance/";

export const ObservableInstance = {
  create: (
    data: observableInstanceCreate,
    getAfterCreate = false,
  ): Promise<void> => api.create(endpoint, data, getAfterCreate),

  read: (uuid: UUID): Promise<observableInstanceRead> =>
    api.read(`${endpoint}${uuid}`),

  update: (uuid: UUID, data: observableInstanceUpdate): Promise<void> =>
    api.update(`${endpoint}${uuid}`, data),
};
