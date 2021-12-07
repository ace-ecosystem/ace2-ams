import { UUID } from "./base";
import { eventPreventionToolRead } from "./eventPreventionTool";
import { eventRemediationRead } from "./eventRemediation";
import { eventRiskLevelRead } from "./eventRiskLevel";
import { eventSourceRead } from "./eventSource";
import { eventStatusRead } from "./eventStatus";
import { eventTypeRead } from "./eventType";
import { eventVectorRead } from "./eventVector";
import { nodeCreate, nodeRead, nodeReadPage, nodeUpdate } from "./node";
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
  remediationTime?: Date;
  riskLevel?: string;
  source?: string;
  status?: string;
  type?: string;
  vectors?: string[];
}

export interface eventSummaryRead extends nodeRead {
  alertTime: Date | null;
  alertUuids: UUID[];
  containTime: Date | null;
  creationTime: Date;
  dispositionTime: Date | null;
  eventTime: Date | null;
  name: string;
  owner: userRead | null;
  ownershipTime: Date | null;
  preventionTools: eventPreventionToolRead[];
  remediations: eventRemediationRead[];
  remediationTime: Date | null;
  riskLevel: eventRiskLevelRead | null;
  source: eventSourceRead | null;
  status: eventStatusRead | null;
  type: eventTypeRead | null;
  vectors: eventVectorRead[];
}

export interface eventReadPage extends nodeReadPage {
  items: eventSummaryRead[];
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
  remediationTime?: Date | null;
  riskLevel?: string | null;
  source?: string | null;
  status?: string | null;
  type?: string | null;
  vectors?: string[];
}
