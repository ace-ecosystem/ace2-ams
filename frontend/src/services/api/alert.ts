import { alertFilters } from "@/etc/constants";
import { formatNodeFiltersForAPI } from "@/etc/helpers";
import {
  alertCreate,
  alertFilterParams,
  alertReadPage,
  alertTreeRead,
  alertUpdate,
} from "@/models/alert";
import { UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/alert/";

export const Alert = {
  createAndRead: async (data: alertCreate): Promise<alertTreeRead> =>
    await api.create(endpoint, data, true),

  read: async (uuid: UUID): Promise<alertTreeRead> =>
    await api.read(`${endpoint}${uuid}`),

  readPage: (params?: alertFilterParams): Promise<alertReadPage> => {
    let formattedParams = {} as alertFilterParams;
    if (params) {
      formattedParams = formatNodeFiltersForAPI(alertFilters, params);
    }

    return api.read(`${endpoint}`, formattedParams);
  },

  update: (data: alertUpdate[]): Promise<void> =>
    api.update(`${endpoint}`, data),
};
