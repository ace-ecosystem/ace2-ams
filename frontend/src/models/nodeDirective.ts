import { UUID } from "./base";

interface NodeDirectiveBase {
  description?: string;
  value: string;
}

export interface NodeDirectiveCreate extends NodeDirectiveBase {
  uuid: UUID;
}

export interface NodeDirectiveRead extends NodeDirectiveBase {
  uuid: UUID;
}

export interface NodeDirectiveUpdate extends NodeDirectiveBase {
  value: string;
}
