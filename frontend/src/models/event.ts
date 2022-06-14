import { historyUsername, pageOptionParams, UUID } from "./base";
import { alertDispositionRead } from "./alertDisposition";
import { eventPreventionToolRead } from "./eventPreventionTool";
import { eventRemediationRead } from "./eventRemediation";
import { eventSeverityRead } from "./eventSeverity";
import { eventSourceRead } from "./eventSource";
import { eventStatusRead } from "./eventStatus";
import { eventTypeRead } from "./eventType";
import { eventVectorRead } from "./eventVector";
import { nodeCreate, nodeRead, nodeReadPage, nodeUpdate } from "./node";
import { nodeCommentRead } from "./nodeComment";
import { nodeThreatRead } from "./nodeThreat";
import { nodeThreatActorRead } from "./nodeThreatActor";
import { observableTypeRead } from "./observableType";
import { queueRead } from "./queue";
import { tagRead } from "./tag";
import { userRead } from "./user";

// High-level event data that will be displayed in Manage Events
export interface eventSummary {
  comments: nodeCommentRead[];
  createdTime: Date;
  // disposition: string;
  name: string;
  owner: string;
  preventionTools: string[];
  severity: string;
  status: string;
  tags: tagRead[];
  threatActors?: string[];
  threats?: string[];
  type: string;
  uuid: UUID;
  vectors: string[];
  queue: string;
  remediations: string[];
  [key: string]: unknown;
}

export interface eventCreate extends nodeCreate, historyUsername {
  alertTime?: Date;
  containTime?: Date;
  dispositionTime?: Date;
  eventTime?: Date;
  name: string;
  owner?: string;
  ownershipTime?: Date;
  preventionTools?: string[];
  queue: string;
  remediationTime?: Date;
  severity?: string;
  source?: string;
  status: string;
  tags?: string[];
  threatActors?: string[];
  threats?: string[];
  type?: string;
  vectors?: string[];
  [key: string]: unknown;
}

export interface eventRead extends nodeRead {
  alertTime: Date | null;
  alertUuids: UUID[];
  analysisTypes: string[];
  autoAlertTime: Date | null;
  autoDispositionTime: Date | null;
  autoEventTime: Date | null;
  autoOwnershipTime: Date | null;
  comments: nodeCommentRead[];
  containTime: Date | null;
  createdTime: Date;
  dispositionTime: Date | null;
  eventTime: Date | null;
  name: string;
  owner: userRead | null;
  ownershipTime: Date | null;
  preventionTools: eventPreventionToolRead[];
  queue: queueRead;
  remediations: eventRemediationRead[];
  remediationTime: Date | null;
  severity: eventSeverityRead | null;
  source: eventSourceRead | null;
  status: eventStatusRead | null;
  tags: tagRead[];
  threatActors: nodeThreatActorRead[];
  threats: nodeThreatRead[];
  type: eventTypeRead | null;
  vectors: eventVectorRead[];
  [key: string]: unknown;
}

export interface eventReadPage extends nodeReadPage {
  items: eventRead[];
}

export interface eventUpdate extends nodeUpdate, historyUsername {
  alertTime?: Date | null;
  containTime?: Date | null;
  dispositionTime?: Date | null;
  eventTime?: Date | null;
  name?: string;
  owner?: string | null;
  ownershipTime?: Date | null;
  preventionTools?: string[];
  queue?: string;
  remediationTime?: Date | null;
  severity?: string | null;
  source?: string | null;
  status?: string | null;
  tags?: string[];
  threatActors?: string[];
  threats?: string[];
  type?: string | null;
  uuid: UUID;
  vectors?: string[];
  [key: string]: unknown;
}

export interface eventFilterParams extends pageOptionParams {
  createdAfter?: Date;
  createdBefore?: Date;
  disposition?: alertDispositionRead;
  eventType?: eventTypeRead;
  name?: string;
  observable?: { category: observableTypeRead; value: string };
  observableTypes?: observableTypeRead[];
  observableValue?: string;
  owner?: userRead;
  preventionTool?: eventPreventionToolRead;
  queue?: queueRead;
  severity?: eventSeverityRead;
  status?: eventStatusRead;
  tags?: string[];
  threatActor?: nodeThreatActorRead;
  threats?: nodeThreatRead[];
  vector?: eventVectorRead;
  [key: string]: any;
}

export type eventFilterNameTypes = Extract<keyof eventFilterParams, string>;

export type eventFilterValues =
  | (
      | alertDispositionRead
      | Date
      | eventPreventionToolRead
      | queueRead
      | eventSeverityRead
      | eventStatusRead
      | eventTypeRead
      | eventVectorRead
      | nodeThreatActorRead
      | nodeThreatRead
      | observableTypeRead
      | string
      | userRead
      | {
          category: observableTypeRead;
          value: string;
        }
    )
  | undefined;
