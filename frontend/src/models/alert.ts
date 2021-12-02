import { alertFilters, alertFilterNames } from "@/etc/constants";
import { pageOptionParams, UUID } from "./base";
import { nodeCreate, nodeRead, nodeReadPage, nodeUpdate } from "./node";
import { alertDispositionRead } from "./alertDisposition";
import { alertQueueRead } from "./alertQueue";
import { alertToolRead } from "./alertTool";
import { alertToolInstanceRead } from "./alertToolInstance";
import { alertTypeRead } from "./alertType";
import { observableInstanceRead } from "./observableInstance";
import { userRead } from "./user";
import { nodeCommentRead } from "./nodeComment";
import { nodeTagRead } from "./nodeTag";

export interface alertCreate extends nodeCreate {
  description?: string;
  eventTime?: Date;
  insertTime?: Date;
  instructions?: string;
  name: string;
  observableInstances: { type: string; value: string }[];
  owner?: string;
  queue: string;
  tool?: string;
  toolInstance?: string;
  type: string;
  [key: string]: unknown;
}

export interface alertSummaryRead extends nodeRead {
  description: string | null;
  disposition: alertDispositionRead | null;
  dispositionTime: Date | null;
  dispositionUser: userRead | null;
  eventTime: Date;
  eventUuid: UUID | null;
  insertTime: Date;
  instructions: string | null;
  name: string;
  owner: userRead | null;
  queue: alertQueueRead;
  tool: alertToolRead | null;
  toolInstance: alertToolInstanceRead | null;
  type: alertTypeRead;
}

// High-level alert data that will be displayed in Manage Alerts or in an event
export interface alertTableSummary {
  comments: nodeCommentRead[];
  description: string;
  disposition: string;
  dispositionTime: Date | null;
  dispositionUser: string;
  eventTime: Date;
  insertTime: Date;
  name: string;
  owner: string;
  queue: string;
  tags: nodeTagRead[];
  tool: string;
  type: string;
  uuid: UUID;
}

export interface alertTreeRead {
  alert: alertSummaryRead;
  analyses: {
    analysisModuleType: { uuid: UUID; value: string };
    parentUuid: UUID | null;
    uuid: UUID;
  }[];
  observableInstances: observableInstanceRead[];
}

export interface alertReadPage extends nodeReadPage {
  items: alertSummaryRead[];
}

export interface alertUpdate extends nodeUpdate {
  description?: string | null;
  disposition?: string;
  eventTime?: Date;
  eventUuid?: UUID;
  insertTime?: Date;
  instructions?: string | null;
  owner?: string;
  queue?: string;
  [key: string]: unknown;
}

export interface alertFilterParams extends pageOptionParams {
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
  sort?: string;
  tags?: string[];
  threatActor?: string;
  threats?: string[];
  tool?: string;
  toolInstance?: string;
  type?: string;
}

export type alertFilterNameTypes = keyof alertFilterParams;
export type alertFilterValues =
  | (string & string[] & Date & { type: string; value: string })
  | undefined;

export type alertFilterOption = {
  readonly name: alertFilterNameTypes;
  readonly label: string;
  readonly type: string;
  readonly options?: string;
  readonly optionValue?: string;
  readonly formatForAPI?: (filter: any) => string;
};