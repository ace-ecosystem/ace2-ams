import { isObject } from "@/etc/helpers";
import {
  eventCreate,
  eventFilterParams,
  eventRead,
  eventReadPage,
  eventUpdate,
} from "@/models/event";
import { UUID } from "@/models/base";
import { BaseApi } from "./base";
import { eventFilters } from "@/etc/constants";

const api = new BaseApi();
const endpoint = "/event/";

export function formatForAPI(
  params: eventFilterParams,
): Record<string, string> {
  const formattedParams = {} as eventFilterParams;
  for (const param in params) {
    let paramValue = params[param] as any;

    //  check if the given param is specific to events and not pageOptionParams, i.e. disposition
    const filterType = eventFilters.find((filter) => {
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

export const Event = {
  create: (data: eventCreate, getAfterCreate = false): Promise<void> => {
    return api.create(endpoint, data, getAfterCreate);
  },

  read: (uuid: UUID): Promise<eventRead> => {
    return api.read(`${endpoint}${uuid}`);
  },

  readAll: (): Promise<eventRead[]> => {
    return api.readAll(endpoint);
  },

  readPage: (params?: eventFilterParams): Promise<eventReadPage> => {
    let formattedParams = {} as eventFilterParams;
    if (params) {
      formattedParams = formatForAPI(params);
    }

    return api.read(`${endpoint}`, formattedParams);
  },

  update: (data: eventUpdate[]): Promise<void> => {
    return api.update(`${endpoint}`, data);
  },
};
