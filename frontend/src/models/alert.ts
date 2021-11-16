import { alertFilters } from "@/etc/constants";
import { UUID } from "./base";
import { genericObject } from "./base";

export type alert = {
  analysis?: Record<string, any>;
  comments?: genericObject[];
  description?: string;
  directives?: genericObject[];
  disposition?: genericObject;
  dispositionTime?: Date;
  dispositionUser?: genericObject;
  eventTime?: Date;
  eventUuid?: UUID;
  insertTime?: Date;
  instructions?: string;
  name?: string;
  owner?: genericObject;
  queue?: genericObject;
  tags?: genericObject[];
  threatActor?: genericObject;
  threats?: genericObject[];
  tool?: genericObject;
  toolInstance?: genericObject;
  type?: genericObject;
  uuid: UUID;
  version?: UUID;
};

// High-level alert data that will be displayed in Manage Alerts or in an event
export type alertSummary = {
  comments: genericObject[];
  description: string;
  disposition: genericObject | string;
  dispositionTime: Date | null;
  dispositionUser: genericObject | string;
  eventTime: Date | null;
  insertTime: Date | null;
  name: string;
  observables: genericObject[];
  owner: genericObject | string;
  queue: genericObject | string;
  tags: genericObject[];
  tool: genericObject | string;
  type: genericObject | string;
  uuid: UUID;
};

export type alertGetAll = {
  items: alert[];
  limit: number;
  offset: number;
  total: number;
};

export type alertFilterParams = {
  disposition?: string;
  dispositionUser?: string;
  dispositionedAfter?: Date;
  dispositionedBefore?: Date;
  eventUuid?: string;
  eventTimeAfter?: Date;
  eventTimeBefore?: Date;
  insertTimeAfter?: Date;
  insertTimeBefore?: Date;
  name?: string;
  observable?: { type: string; value: string };
  observableTypes?: string[];
  observableValue?: string;
  owner?: string;
  queue?: string;
  tags?: string[];
  threatActor?: string;
  threats?: string[];
  tool?: string;
  toolInstance?: string;
  type?: string;
};

export type alertFilterTypes = typeof alertFilters[number];
export type alertFilterValues =
  | (string & string[] & Date & { type: string; value: string })
  | undefined;
