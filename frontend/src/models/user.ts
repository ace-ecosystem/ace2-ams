import { UUID } from "./base";
import { alertQueueRead } from "./alertQueue";
import { userRoleRead } from "./userRole";

export interface userCreate {
  defaultAlertQueue: string;
  displayName: string;
  email: string;
  enabled?: boolean;
  roles: string[];
  timezone?: string;
  username: string;
  password: string;
  uuid?: UUID;
  [key: string]: unknown;
}

export interface userRead {
  defaultAlertQueue: alertQueueRead;
  displayName: string;
  email: string;
  enabled: boolean;
  roles: userRoleRead[];
  timezone: string;
  username: string;
  uuid: UUID;
}

export interface userReadPage {
  items: userRead[];
  limit: number;
  offset: number;
  total: number;
}

export interface userUpdate {
  defaultAlertQueue?: string;
  displayName?: string;
  email?: string;
  enabled?: boolean;
  roles?: string[];
  timezone?: string;
  username?: string;
  password?: string;
  [key: string]: unknown;
}
