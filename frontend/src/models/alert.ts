import { historyUsername, pageOptionParams, UUID } from "./base";
import { alertDispositionRead } from "./alertDisposition";
import { alertToolRead } from "./alertTool";
import { alertToolInstanceRead } from "./alertToolInstance";
import { alertTypeRead } from "./alertType";
import { metadataDetectionPointRead } from "./metadataDetectionPoint";
import { metadataTagRead } from "./metadataTag";
import { alertCommentRead } from "./alertComment";
import { observableCreate, observableTreeRead } from "./observable";
import { observableTypeRead } from "./observableType";
import { queueRead } from "./queue";
import { userRead } from "./user";
import { readPage } from "./page";

export interface alertCreate extends historyUsername {
  alert: boolean;
  description?: string;
  eventTime?: Date;
  insertTime?: Date;
  instructions?: string;
  name: string;
  observables: observableCreate[];
  owner?: string;
  queue: string;
  tags?: string[];
  tool?: string;
  toolInstance?: string;
  type: string;
  [key: string]: unknown;
}

export interface alertRead {
  alert: boolean;
  childAnalysisTags: metadataTagRead[];
  childDetectionPoints: metadataDetectionPointRead[];
  childTags: metadataTagRead[];
  comments: alertCommentRead[];
  description: string | null;
  disposition: alertDispositionRead | null;
  dispositionTime: string | null;
  dispositionUser: userRead | null;
  eventTime: string;
  eventUuid: UUID | null;
  insertTime: string;
  instructions: string | null;
  name: string;
  objectType: string;
  owner: userRead | null;
  ownershipTime: string | null;
  queue: queueRead;
  tags: metadataTagRead[];
  tool: alertToolRead | null;
  toolInstance: alertToolInstanceRead | null;
  type: alertTypeRead;
  uuid: UUID;
  version: UUID;
  [key: string]: unknown;
}

// High-level alert data that will be displayed in Manage Alerts or in an event
export interface alertSummary {
  childAnalysisTags: metadataTagRead[];
  childTags: metadataTagRead[];
  comments: alertCommentRead[];
  description: string;
  disposition: string;
  dispositionTime: string | null;
  dispositionUser: string;
  dispositionWithUserAndTime: string;
  eventTime: string;
  eventUuid: string;
  insertTime: string;
  name: string;
  owner: string;
  ownershipTime: string | null;
  ownerWithTime: string;
  queue: string;
  tags: metadataTagRead[];
  tool: string;
  toolInstance: string;
  type: string;
  uuid: UUID;
}

export interface alertTreeRead extends alertRead {
  children: observableTreeRead[];
  rootAnalysisUuid: UUID;
}

export interface alertReadPage extends readPage {
  items: alertRead[];
}

export interface alertUpdate extends historyUsername {
  description?: string | null;
  disposition?: string;
  eventTime?: Date;
  eventUuid?: UUID | null;
  insertTime?: Date;
  instructions?: string | null;
  owner?: string;
  queue?: string;
  tags?: string[];
  uuid: UUID;
  version?: UUID;
  [key: string]: unknown;
}

export interface alertFilterParams extends pageOptionParams {
  alertType?: { included: alertTypeRead[]; notIncluded: alertTypeRead[] };
  disposition?: {
    included: alertDispositionRead[];
    notIncluded: alertDispositionRead[];
  };
  dispositionUser?: { included: userRead[]; notIncluded: userRead[] };
  dispositionedAfter?: { included: Date[]; notIncluded: Date[] };
  dispositionedBefore?: { included: Date[]; notIncluded: Date[] };
  eventUuid?: { included: UUID[]; notIncluded: UUID[] };
  eventTimeAfter?: { included: Date[]; notIncluded: Date[] };
  eventTimeBefore?: { included: Date[]; notIncluded: Date[] };
  insertTimeAfter?: { included: Date[]; notIncluded: Date[] };
  insertTimeBefore?: { included: Date[]; notIncluded: Date[] };
  name?: { included: string[]; notIncluded: string[] };
  owner?: { included: userRead[]; notIncluded: userRead[] };
  observableType?: {
    included: observableTypeRead[];
    notIncluded: observableTypeRead[];
  };
  queue?: { included: queueRead[]; notIncluded: queueRead[] };
  observableValue?: { included: string[]; notIncluded: string[] };
  tool?: { included: alertToolRead[]; notIncluded: alertToolRead[] };
  toolInstance?: {
    included: alertToolInstanceRead[];
    notIncluded: alertToolInstanceRead[];
  };
  tags?: { included: string[][]; notIncluded: string[][] };
  observable?: {
    included: { category: observableTypeRead; value: string }[];
    notIncluded: { category: observableTypeRead; value: string }[];
  };
  sort?: string;
  [key: string]: any;
}

export type alertFilterNameTypes = Extract<keyof alertFilterParams, string>;
export type alertFilterValues =
  | (
      | string
      | observableTypeRead[]
      | metadataTagRead[]
      | Date
      | {
          category: observableTypeRead;
          value: string;
        }
      | alertDispositionRead
      | userRead
      | queueRead
      | alertToolRead
      | alertToolInstanceRead
      | alertTypeRead
    )
  | undefined;
