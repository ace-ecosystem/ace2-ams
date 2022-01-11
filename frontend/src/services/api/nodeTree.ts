import { nodeRead } from "@/models/node";
import { UUID } from "@/models/base";
import { BaseApi } from "./base";

const api = new BaseApi();
const endpoint = "/node/tree/";

export const NodeTree = {
  readNodesOfNodeTree: (
    uuids: Array<UUID>,
    nodeType: string,
  ): Promise<Array<nodeRead>> =>
    api.baseRequest(`${endpoint}${nodeType}`, "POST", { data: uuids }),
};
