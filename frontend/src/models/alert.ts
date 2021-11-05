import { UUID } from "./base";
import { genericObject } from "./base";

export type alert = {
  analysis: Record<string, any>;
  comments: genericObject[];
  description: string;
  directives: genericObject[];
  disposition: genericObject;
  dispositionTime: Date;
  dispositionUser: genericObject;
  eventTime: Date;
  eventUuid: UUID;
  insertTime: Date;
  instructions: string;
  name: string;
  owner: genericObject;
  queue: genericObject;
  tags: genericObject[];
  threatActor: genericObject;
  threats: genericObject[];
  tool: genericObject;
  toolInstance: genericObject;
  type: genericObject;
  uuid: UUID;
  version: UUID;
};

export type alertGetAll = {
  items: alert[];
  limit: number;
  offset: number;
  total: number;
};
