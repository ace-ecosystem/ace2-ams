import { UUID } from "./base";
import { eventPreventionToolRead } from "./eventPreventionTool";
import { eventQueueRead } from "./eventQueue";
import { eventRemediationRead } from "./eventRemediation";
import { eventRiskLevelRead } from "./eventRiskLevel";
import { eventSourceRead } from "./eventSource";
import { eventStatusRead } from "./eventStatus";
import { eventTypeRead } from "./eventType";
import { eventVectorRead } from "./eventVector";
import { nodeCreate, nodeRead, nodeReadPage, nodeUpdate } from "./node";
import { nodeCommentRead } from "./nodeComment";
import { nodeTagRead } from "./nodeTag";
import { nodeThreatRead } from "./nodeThreat";
import { nodeThreatActorRead } from "./nodeThreatActor";
import { userRead } from "./user";

export interface eventCreate extends nodeCreate {
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
  riskLevel?: string;
  source?: string;
  status?: string;
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
  comments: nodeCommentRead[];
  containTime: Date | null;
  creationTime: Date;
  dispositionTime: Date | null;
  eventTime: Date | null;
  name: string;
  owner: userRead | null;
  ownershipTime: Date | null;
  preventionTools: eventPreventionToolRead[];
  queue: eventQueueRead;
  remediations: eventRemediationRead[];
  remediationTime: Date | null;
  riskLevel: eventRiskLevelRead | null;
  source: eventSourceRead | null;
  status: eventStatusRead | null;
  tags: nodeTagRead[];
  threatActors: nodeThreatActorRead[];
  threats: nodeThreatRead[];
  type: eventTypeRead | null;
  vectors: eventVectorRead[];
}

export interface eventReadPage extends nodeReadPage {
  items: eventRead[];
}

export interface eventUpdate extends nodeUpdate {
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
  riskLevel?: string | null;
  source?: string | null;
  status?: string | null;
  tags?: string[];
  threatActors?: string[];
  threats?: string[];
  type?: string | null;
  vectors?: string[];
  [key: string]: unknown;
}
