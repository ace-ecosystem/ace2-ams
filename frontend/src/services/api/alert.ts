import { alertFilters } from "@/etc/constants";
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
  create: (data: alertCreate, getAfterCreate = true): Promise<void> =>
    api.create(endpoint, data, getAfterCreate),

  read: (uuid: UUID): Promise<alertTreeRead> => api.read(`${endpoint}${uuid}`),

  readPage: (params?: alertFilterParams): Promise<alertReadPage> => {
    if (params) {
      for (const param in params) {
        const paramValue = params[param] as unknown;

        //  check if the given param is specific to alerts and not pageOptionParams, i.e. disposition
        const filterType = alertFilters.find((filter) => {
          return filter.name === param;
        });

        // if so, check if the param's value needs to be formatted, and replace with the newly formatted val
        if (filterType && filterType.formatForAPI) {
          if (filterType.formatForAPI) {
            params[param] = filterType.formatForAPI(paramValue) as never;
          }
        }
      }
    }

    return api.read(`${endpoint}`, params);
  },

  update: (uuid: UUID, data: alertUpdate): Promise<void> =>
    api.update(`${endpoint}${uuid}`, data),
};
