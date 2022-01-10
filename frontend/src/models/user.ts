import { UUID } from "./base";
import { alertQueueRead } from "./alertQueue";
import { eventQueueRead } from "./eventQueue";
import { userRoleRead } from "./userRole";

export interface userCreate {
  defaultAlertQueue: string;
  defaultEventQueue: string;
  displayName: string;
  email: string;
  enabled?: boolean;
  roles: string[];
  timezone?: string;
  training?: boolean;
  username: string;
  password: string;
  uuid?: UUID;
  [key: string]: unknown;
}

export interface userRead {
  defaultAlertQueue: alertQueueRead;
  defaultEventQueue: eventQueueRead;
  displayName: string;
  email: string;
  enabled: boolean;
  roles: userRoleRead[];
  timezone: string;
  training: boolean;
  username: string;
  uuid: UUID;
  [key: string]: unknown;
}

export interface userReadPage {
  items: userRead[];
  limit: number;
  offset: number;
  total: number;
}

export interface userUpdate {
  defaultAlertQueue?: string;
  defaultEventQueue?: string;
  displayName?: string;
  email?: string;
  enabled?: boolean;
  roles?: string[];
  timezone?: string;
  training?: boolean;
  username?: string;
  password?: string;
  [key: string]: unknown;
}
