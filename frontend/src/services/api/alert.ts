import { alertFilters } from "@/etc/constants";
import { formatNodeFiltersForAPI } from "@/etc/helpers";
import {
  alertCreate,
  alertFilterParams,
  alertRead,
  alertReadPage,
  alertSummary,
  alertTreeRead,
  alertUpdate,
} from "@/models/alert";
import { UUID } from "@/models/base";
import { nodeTagRead } from "@/models/nodeTag";
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

    return api.read(endpoint, formattedParams);
  },

  readAllPages: async (
    params: alertFilterParams,
  ): Promise<Array<alertRead>> => {
    const formattedParams = formatNodeFiltersForAPI(alertFilters, params);
    return api.readAll(endpoint, formattedParams);
  },

  update: (data: alertUpdate[]): Promise<void> => api.update(endpoint, data),
};

export function parseAlertSummary(
  alert: alertRead | alertTreeRead,
): alertSummary {
  return {
    childTags: alert.childTags,
    comments: alert.comments,
    description: alert.description ? alert.description : "",
    disposition: alert.disposition ? alert.disposition.value : "OPEN",
    dispositionTime: alert.dispositionTime ? alert.dispositionTime : null,
    dispositionUser: alert.dispositionUser
      ? alert.dispositionUser.displayName
      : "None",
    eventTime: alert.eventTime,
    eventUuid: alert.eventUuid ? alert.eventUuid : "None",
    insertTime: alert.insertTime,
    name: alert.name,
    owner: alert.owner ? alert.owner.displayName : "None",
    queue: alert.queue.value,
    tags: alert.tags,
    tool: alert.tool ? alert.tool.value : "None",
    toolInstance: alert.toolInstance ? alert.toolInstance.value : "None",
    type: alert.type.value,
    uuid: alert.uuid,
  };
}

export function getAllTags(alert: alertRead | alertTreeRead): nodeTagRead[] {
  const allTags = alert.tags.concat(alert.childTags);

  // Return a sorted and deduplicated list of the tags based on the tag UUID.
  return [...new Map(allTags.map((v) => [v.uuid, v])).values()].sort((a, b) =>
    a.value > b.value ? 1 : -1,
  );
}
