import { analysisRead } from "@/models/analysis";
import { UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/analysis/";

export const Analysis = {
  read: (uuid: UUID): Promise<analysisRead> => api.read(`${endpoint}${uuid}`),
};
