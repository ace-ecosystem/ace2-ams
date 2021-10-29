import { UUID } from "@/models/base";

interface UserBase {
  defaultAlertQueue?: string;
  displayName?: string;
  email?: string;
  enabled?: boolean;
  roles?: Array<string>;
  timezone?: string;
  username?: string;
}

export interface UserCreate extends UserBase {
  password: string;
  uuid: UUID;
}

export interface UserRead extends UserBase {
  // todo: change to AlertQueueRead
  defaultAlertQueue: string;
  // todo: change to UserRoleRead
  roles: Array<string>;
  uuid: UUID;
}

export interface UserUpdate extends UserBase {
  defaultAlertQueue?: string;
  displayName?: string;
  email?: string;
  enabled?: boolean;
  password?: string;
  roles?: Array<string>;
  timezone?: string;
  username?: string;
}
