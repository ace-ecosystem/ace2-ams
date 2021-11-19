import { genericObject, genericGetAll } from "./base";
import { alert, alertGetAll, alertFilterParams } from "./alert";

export type anyGetSingle = genericObject & alert;
export type anyGetAll = genericGetAll & alertGetAll;
export type pageOptionParams = { limit: number; offset: number };
export type getAllParams = pageOptionParams & alertFilterParams;
