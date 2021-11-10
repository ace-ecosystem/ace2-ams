import { genericObject, genericGetAll } from "./base";
import { alert, alertGetAll } from "./alert";

export type anyGetSingle = genericObject & alert;
export type anyGetAll = genericGetAll & alertGetAll;
export type getAllParams = { limit: number; offset: number };
