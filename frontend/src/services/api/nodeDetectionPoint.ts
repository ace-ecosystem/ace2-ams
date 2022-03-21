import {
  nodeDetectionPointCreate,
  nodeDetectionPointRead,
  nodeDetectionPointUpdate,
} from "@/models/nodeDetectionPoint";
import { UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/node/detection_point/";

export const NodeDetectionPoint = {
  create: (
    data: nodeDetectionPointCreate[],
    getAfterCreate = false,
  ): Promise<void> => api.create(endpoint, data, getAfterCreate),

  read: (uuid: UUID): Promise<nodeDetectionPointRead> =>
    api.read(`${endpoint}${uuid}`),

  update: (uuid: UUID, data: nodeDetectionPointUpdate): Promise<void> =>
    api.update(`${endpoint}${uuid}`, data),
};
