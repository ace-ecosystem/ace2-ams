import { formatNodeFiltersForAPI } from "@/etc/helpers";
import {
  eventCreate,
  eventFilterParams,
  eventRead,
  eventReadPage,
  eventUpdate,
} from "@/models/event";
import {
  emailSummary,
  emailHeadersBody,
  detectionPointSummary,
  observableSummary,
  userSummary,
  urlDomainSummary,
} from "@/models/eventSummaries";
import { UUID } from "@/models/base";
import { BaseApi } from "./base";
import { eventHistoryReadPage } from "@/models/history";

const api = new BaseApi();
const endpoint = "/event/";

import { validEventFilters } from "@/etc/constants/events";

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

  readObservableSummary: async (uuid: UUID): Promise<observableSummary[]> =>
    await api.read(`${endpoint}${uuid}/summary/observable`),

  readUserSummary: async (uuid: UUID): Promise<userSummary[]> =>
    await api.read(`${endpoint}${uuid}/summary/user`),

  readUrlDomainSummary: async (uuid: UUID): Promise<urlDomainSummary[]> =>
    await api.read(`${endpoint}${uuid}/summary/url_domain`),

  readEmailSummary: async (uuid: UUID): Promise<emailSummary[]> =>
    await api.read(`${endpoint}${uuid}/summary/email`),

  readEmailHeadersAndBody: async (uuid: UUID): Promise<emailHeadersBody[]> =>
    await api.read(`${endpoint}${uuid}/summary/email_headers_body`),

  readDetectionSummary: async (uuid: UUID): Promise<detectionPointSummary[]> =>
    await api.read(`${endpoint}${uuid}/summary/detection_point`),

  readPage: (params?: eventFilterParams): Promise<eventReadPage> => {
    let formattedParams = {} as eventFilterParams;
    if (params) {
      formattedParams = formatNodeFiltersForAPI(validEventFilters, params);
    }

    return api.read(endpoint, formattedParams);
  },

  readAllPages: (params?: eventFilterParams): Promise<eventRead[]> => {
    let formattedParams = {} as eventFilterParams;
    if (params) {
      formattedParams = formatNodeFiltersForAPI(validEventFilters, params);
    }

    return api.readAll(endpoint, formattedParams);
  },

  update: (data: eventUpdate[]): Promise<void> => {
    return api.update(endpoint, data);
  },
};
