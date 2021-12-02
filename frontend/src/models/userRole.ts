import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";

export type userRoleCreate = genericObjectCreate;

export type userRoleRead = genericObjectRead;

export interface userRoleReadPage extends genericObjectReadPage {
  items: userRoleRead[];
}

export type userRoleUpdate = genericObjectUpdate;
