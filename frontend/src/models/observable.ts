import { UUID } from "./base";
import { observableTypeRead } from "./observableType";

export interface observableCreate {
  expiresOn?: Date;
  forDetection: boolean;
  type: string;
  uuid?: UUID;
  value: string;
}

export interface observableRead {
  expiresOn: Date | null;
  forDetection: boolean;
  type: observableTypeRead;
  uuid: UUID;
  value: string;
}

export interface observableReadPage {
  items: observableRead[];
  limit: number;
  offset: number;
  total: number;
}

export interface observableUpdate {
  expiresOn?: Date;
  forDetection?: boolean;
  type?: string;
  value?: string;
}
