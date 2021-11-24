import { UUID } from "./base";
import { nodeCreate, nodeRead, nodeUpdate } from "./node";
import { observableRead } from "./observable";

export interface observableInstanceCreate extends nodeCreate {
  alertUuid: UUID;
  context?: string;
  parentUuid: UUID;
  redirectionUuid?: UUID;
  time?: Date;
  type: string;
  value: string;
  [key: string]: unknown;
}

export interface observableInstanceRead extends nodeRead {
  alertUuid: UUID;
  context: string | null;
  observable: observableRead;
  parentUuid: UUID;
  redirectionUuid: UUID | null;
  time: Date;
}

export interface observableInstanceUpdate extends nodeUpdate {
  context?: string;
  redirectionUuid?: UUID;
  time?: Date;
  [key: string]: unknown;
}
