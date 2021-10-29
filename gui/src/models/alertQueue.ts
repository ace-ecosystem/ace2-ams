import { UUID } from "./base";

interface AlertQueueBase {
  description?: string;
  value: string;
}

export interface AlertQueueCreate extends AlertQueueBase {
  uuid: UUID;
}

export interface AlertQueueRead extends AlertQueueBase {
  uuid: UUID;
}

export interface AlertQueueUpdate extends AlertQueueBase {
  value: string;
}
