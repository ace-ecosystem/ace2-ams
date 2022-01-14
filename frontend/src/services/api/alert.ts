import { alertFilters } from "@/etc/constants";
import { isObject } from "@/etc/helpers";
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
    let paramValue = params[param] as any;

    //  check if the given param is specific to alerts and not pageOptionParams, i.e. disposition
    const filterType = alertFilters.find((filter) => {
      return filter.name === param;
    });

    // if so, check if the param's value needs to be formatted, and replace with the newly formatted val
    if (filterType) {
      // First check if there is a method provided to get string representation
      if (filterType.stringRepr) {
        paramValue = filterType.stringRepr(paramValue) as never;
        // Otherwise check if the param's value is a specific property
      } else if (filterType.valueProperty && isObject(paramValue)) {
        paramValue = paramValue[filterType.valueProperty];
      }
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
