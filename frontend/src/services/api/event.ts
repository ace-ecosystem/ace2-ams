import { formatNodeFiltersForAPI } from "@/etc/helpers";
import {
  eventCreate,
  eventFilterParams,
  eventRead,
  eventReadPage,
  eventUpdate,
} from "@/models/event";
import { UUID } from "@/models/base";
import { BaseApi } from "./base";
import { eventHistoryReadPage } from "@/models/history";
import { configuration } from "@/etc/configuration";
import { testConfiguration } from "@/etc/configuration/test";

const api = new BaseApi();
const endpoint = "/event/";

const testingModeEnabled = import.meta.env.VITE_TESTING_MODE;
const filters =
  testingModeEnabled === "yes"
    ? testConfiguration.events.eventFilters
    : configuration.events.eventFilters;

export const Event = {
  create: (
    data: eventCreate,
    getAfterCreate = false,
  ): Promise<eventRead | void> => {
    return api.create(endpoint, data, getAfterCreate);
  },

  read: (uuid: UUID): Promise<eventRead> => {
    return api.read(`${endpoint}${uuid}`);
  },

  readHistory: async (uuid: UUID): Promise<eventHistoryReadPage> =>
    await api.read(`${endpoint}${uuid}/history`),

  readPage: (params?: eventFilterParams): Promise<eventReadPage> => {
    let formattedParams = {} as eventFilterParams;
    if (params) {
      formattedParams = formatNodeFiltersForAPI(filters, params);
    }

    return api.read(endpoint, formattedParams);
  },

  readAllPages: (params?: eventFilterParams): Promise<eventRead[]> => {
    let formattedParams = {} as eventFilterParams;
    if (params) {
      formattedParams = formatNodeFiltersForAPI(filters, params);
    }

    return api.readAll(endpoint, formattedParams);
  },

  update: (data: eventUpdate[]): Promise<void> => {
    return api.update(endpoint, data);
  },
};
