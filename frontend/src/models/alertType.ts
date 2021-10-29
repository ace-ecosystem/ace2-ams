import { UUID } from "./base";

interface AlertTypeBase {
  description?: string;
  value: string;
}

export interface AlertTypeCreate extends AlertTypeBase {
  uuid: UUID;
}

export interface AlertTypeRead extends AlertTypeBase {
  uuid: UUID;
}

export interface AlertTypeUpdate extends AlertTypeBase {
  value: string;
}
