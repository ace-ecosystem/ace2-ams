import { formatObjectFiltersForAPI } from "@/etc/helpers";
import {
  alertCreate,
  alertFilterParams,
  alertRead,
  alertReadPage,
  alertTreeRead,
  alertUpdate,
} from "@/models/alert";
import { UUID } from "@/models/base";
import { alertHistoryReadPage } from "@/models/history";
import { urlDomainSummary } from "@/models/summaries";
import { validAlertFilters } from "@/etc/constants/alerts";
import { observableInAlertRead } from "@/models/observable";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/alert/";

export const Alert = {
  createAndRead: async (data: alertCreate): Promise<alertTreeRead> =>
    await api.create(endpoint, data, true),

  read: async (uuid: UUID): Promise<alertTreeRead> =>
    await api.read(`${endpoint}${uuid}`),

  readHistory: async (uuid: UUID): Promise<alertHistoryReadPage> =>
    await api.read(`${endpoint}${uuid}/history`),

  readPage: (params?: alertFilterParams): Promise<alertReadPage> => {
    let formattedParams = {} as alertFilterParams;
    if (params) {
      formattedParams = formatObjectFiltersForAPI(validAlertFilters, params);
    }

    return api.read(endpoint, formattedParams);
  },

  readAllPages: async (
    params: alertFilterParams,
  ): Promise<Array<alertRead>> => {
    const formattedParams = formatObjectFiltersForAPI(validAlertFilters, params);
    return api.readAll(endpoint, formattedParams);
  },

  readObservables: async (
    uuids: Array<UUID>,
  ): Promise<observableInAlertRead[]> =>
    await api.baseRequest(`${endpoint}observables`, "POST", { data: uuids }),

  readUrlDomainSummary: async (uuid: UUID): Promise<urlDomainSummary> =>
    await api.read(`${endpoint}${uuid}/summary/url_domain`),

  update: (data: alertUpdate[]): Promise<void> => {
    return api.update(endpoint, data);
  },
};
