import { historyUsername, pageOptionParams, UUID } from "./base";
import { nodeCreate, nodeRead, nodeReadPage, nodeUpdate } from "./node";
import { alertDispositionRead } from "./alertDisposition";
import { alertToolRead } from "./alertTool";
import { alertToolInstanceRead } from "./alertToolInstance";
import { alertTypeRead } from "./alertType";
import { metadataDetectionPointRead } from "./metadataDetectionPoint";
import { metadataTagRead } from "./metadataTag";
import { nodeCommentRead } from "./nodeComment";
import { observableCreate, observableTreeRead } from "./observable";
import { observableTypeRead } from "./observableType";
import { nodeThreatActorRead } from "./nodeThreatActor";
import { nodeThreatRead } from "./nodeThreat";
import { queueRead } from "./queue";
import { userRead } from "./user";

export interface alertCreate extends nodeCreate, historyUsername {
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
  threatActors?: string[];
  threats?: string[];
  tool?: string;
  toolInstance?: string;
  type: string;
  [key: string]: unknown;
}

export interface alertRead extends nodeRead {
  alert: boolean;
  childAnalysisTags: metadataTagRead[];
  childDetectionPoints: metadataDetectionPointRead[];
  childTags: metadataTagRead[];
  childThreatActors: nodeThreatActorRead[];
  childThreats: nodeThreatRead[];
  comments: nodeCommentRead[];
  description: string | null;
  disposition: alertDispositionRead | null;
  dispositionTime: string | null;
  dispositionUser: userRead | null;
  eventTime: string;
  eventUuid: UUID | null;
  insertTime: string;
  instructions: string | null;
  name: string;
  owner: userRead | null;
  ownershipTime: string | null;
  queue: queueRead;
  tags: metadataTagRead[];
  threatActors: nodeThreatActorRead[];
  threats: nodeThreatRead[];
  tool: alertToolRead | null;
  toolInstance: alertToolInstanceRead | null;
  type: alertTypeRead;
  [key: string]: unknown;
}

// High-level alert data that will be displayed in Manage Alerts or in an event
export interface alertSummary {
  childAnalysisTags: metadataTagRead[];
  childTags: metadataTagRead[];
  comments: nodeCommentRead[];
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

export interface alertReadPage extends nodeReadPage {
  items: alertRead[];
}

export interface alertUpdate extends nodeUpdate, historyUsername {
  description?: string | null;
  disposition?: string;
  eventTime?: Date;
  eventUuid?: UUID | null;
  insertTime?: Date;
  instructions?: string | null;
  owner?: string;
  queue?: string;
  tags?: string[];
  threatActors?: string[];
  threats?: string[];
  uuid: UUID;
  [key: string]: unknown;
}

export interface alertFilterParams extends pageOptionParams {
  alertType?: alertTypeRead[];
  disposition?: alertDispositionRead[];
  dispositionUser?: userRead[];
  dispositionedAfter?: Date[];
  dispositionedBefore?: Date[];
  eventUuid?: string[];
  eventTimeAfter?: Date[];
  eventTimeBefore?: Date[];
  insertTimeAfter?: Date[];
  insertTimeBefore?: Date[];
  name?: string[];
  observable?: { category: observableTypeRead; value: string }[];
  observableTypes?: observableTypeRead[][];
  observableValue?: string[];
  owner?: userRead[];
  queue?: queueRead[];
  sort?: string;
  tags?: string[][];
  threatActor?: nodeThreatActorRead[];
  threats?: nodeThreatRead[][];
  tool?: alertToolRead[];
  toolInstance?: alertToolInstanceRead[];
  [key: string]: any;
}

export type alertFilterNameTypes = Extract<keyof alertFilterParams, string>;
export type alertFilterValues =
  | (
      | string
      | observableTypeRead[]
      | nodeThreatRead[]
      | metadataTagRead[]
      | Date
      | {
          category: observableTypeRead;
          value: string;
        }
      | alertDispositionRead
      | userRead
      | queueRead
      | nodeThreatActorRead
      | alertToolRead
      | alertToolInstanceRead
      | alertTypeRead
    )
  | undefined;
