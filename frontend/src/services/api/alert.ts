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

export function formatForAPI(
  params: alertFilterParams,
): Record<string, string> {
  const formattedParams = {} as alertFilterParams;
  for (const param in params) {
    let paramValue = params[param] as unknown;

    //  check if the given param is specific to alerts and not pageOptionParams, i.e. disposition
    const filterType = alertFilters.find((filter) => {
      return filter.name === param;
    });

    // if so, check if the param's value needs to be formatted, and replace with the newly formatted val
    if (filterType && filterType.formatForAPI) {
      paramValue = filterType.formatForAPI(paramValue) as never;
    }

    formattedParams[param] = paramValue;
  }
  return formattedParams;
}

export const Alert = {
  createAndRead: async (data: alertCreate): Promise<alertTreeRead> =>
    await api.create(endpoint, data, true),

  read: async (uuid: UUID): Promise<alertTreeRead> =>
    await api.read(`${endpoint}${uuid}`),

  readPage: (params?: alertFilterParams): Promise<alertReadPage> => {
    let formattedParams = {} as alertFilterParams;
    if (params) {
      formattedParams = formatForAPI(params);
    }

    return api.read(`${endpoint}`, formattedParams);
  },

  update: (data: alertUpdate[]): Promise<void> =>
    api.update(`${endpoint}`, data),
};
