import { historyUsername, pageOptionParams, UUID } from "./base";
import { alertDispositionRead } from "./alertDisposition";
import { eventPreventionToolRead } from "./eventPreventionTool";
import { eventRemediationRead } from "./eventRemediation";
import { eventSeverityRead } from "./eventSeverity";
import { eventSourceRead } from "./eventSource";
import { eventStatusRead } from "./eventStatus";
import { eventTypeRead } from "./eventType";
import { eventVectorRead } from "./eventVector";
import { metadataTagRead } from "./metadataTag";
import { eventCommentRead } from "./eventComment";
import { threatRead } from "./threat";
import { threatActorRead } from "./threatActor";
import { observableTypeRead } from "./observableType";
import { queueRead } from "./queue";
import { userRead } from "./user";
import { readPage } from "./page";

// High-level event data that will be displayed in Manage Events
export interface eventSummary {
  comments: eventCommentRead[];
  createdTime: Date;
  // disposition: string;
  name: string;
  owner: string;
  preventionTools: string[];
  severity: string;
  status: string;
  tags: metadataTagRead[];
  threatActors?: string[];
  threats?: string[];
  type: string;
  uuid: UUID;
  vectors: string[];
  queue: string;
  remediations: string[];
  [key: string]: unknown;
}

export interface eventCreate extends historyUsername {
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

export interface eventRead {
  alertTime: string | null;
  alertUuids: UUID[];
  allTags: metadataTagRead[];
  analysisTypes: string[];
  autoAlertTime: string | null;
  autoDispositionTime: string | null;
  autoEventTime: string | null;
  autoOwnershipTime: string | null;
  comments: eventCommentRead[];
  containTime: string | null;
  createdTime: string;
  dispositionTime: string | null;
  eventTime: string | null;
  name: string;
  objectType: string;
  owner: userRead | null;
  ownershipTime: string | null;
  preventionTools: eventPreventionToolRead[];
  queue: queueRead;
  remediations: eventRemediationRead[];
  remediationTime: string | null;
  severity: eventSeverityRead | null;
  source: eventSourceRead | null;
  status: eventStatusRead | null;
  tags: metadataTagRead[];
  threatActors: threatActorRead[];
  threats: threatRead[];
  type: eventTypeRead | null;
  uuid: UUID;
  vectors: eventVectorRead[];
  version: UUID;
  [key: string]: unknown;
}

export interface eventReadPage extends readPage {
  items: eventRead[];
}

export interface eventUpdate extends historyUsername {
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
  version?: UUID;
  [key: string]: unknown;
}

export interface eventFilterParams extends pageOptionParams {
  createdAfter?: { included: Date[]; notIncluded: Date[] };
  createdBefore?: { included: Date[]; notIncluded: Date[] };
  disposition?: {
    included: alertDispositionRead[];
    notIncluded: alertDispositionRead[];
  };
  name?: { included: string[]; notIncluded: string[] };
  eventType?: { included: eventTypeRead[]; notIncluded: eventTypeRead[] };
  observable?: {
    included: { category: observableTypeRead; value: string }[];
    notIncluded: { category: observableTypeRead; value: string }[];
  };
  observableTypes?: {
    included: observableTypeRead[][];
    notIncluded: observableTypeRead[][];
  };
  observableValue?: { included: string[]; notIncluded: string[] };
  owner?: { included: userRead[]; notIncluded: userRead[] };
  preventionTools?: {
    included: eventPreventionToolRead[];
    notIncluded: eventPreventionToolRead[];
  };
  queue?: { included: queueRead[]; notIncluded: queueRead[] };
  severity?: {
    included: eventSeverityRead[];
    notIncluded: eventSeverityRead[];
  };
  status?: { included: eventStatusRead[]; notIncluded: eventStatusRead[] };
  threatActors?: {
    included: threatActorRead[];
    notIncluded: threatActorRead[];
  };
  threats?: { included: threatRead[][]; notIncluded: threatRead[][] };
  vectors?: { included: eventVectorRead[]; notIncluded: eventVectorRead[] };
  tags?: { included: string[][]; notIncluded: string[][] };
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
      | threatActorRead
      | threatRead
      | observableTypeRead
      | string
      | userRead
      | {
          category: observableTypeRead;
          value: string;
        }
    )
  | undefined;
