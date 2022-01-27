import { eventRead } from "@/models/event";
import { eventPreventionToolRead } from "@/models/eventPreventionTool";
import { eventQueueRead } from "@/models/eventQueue";
import { eventRemediationRead } from "@/models/eventRemediation";
import { eventRiskLevelRead } from "@/models/eventRiskLevel";
import { eventSourceRead } from "@/models/eventSource";
import { eventStatusRead } from "@/models/eventStatus";
import { eventTypeRead } from "@/models/eventType";
import { eventVectorRead } from "@/models/eventVector";
import { nodeCommentRead } from "@/models/nodeComment";
import { nodeTagRead } from "@/models/nodeTag";
import { nodeThreatRead } from "@/models/nodeThreat";
import { nodeThreatActorRead } from "@/models/nodeThreatActor";
import { userRead } from "@/models/user";
import { genericObjectFactory } from "./genericObject";
import { userFactory } from "./user";

export const eventFactory = (
  comments: nodeCommentRead[] = [],
  name = "Test Event",
  tags: nodeTagRead[] = [],
  uuid = "testEvent1",
  alertTime: Date | null = null,
  alertUuids = [],
  containTime: Date | null = null,
  creationTime: Date = new Date("2020-01-01"),
  dispositionTime: Date | null = null,
  eventTime: Date | null = null,
  owner: userRead = userFactory(),
  ownershipTime: Date | null = null,
  preventionTools: eventPreventionToolRead[] = [],
  queue: eventQueueRead = genericObjectFactory(),
  remediations: eventRemediationRead[] = [],
  remediationTime: Date | null = null,
  riskLevel: eventRiskLevelRead | null = null,
  source: eventSourceRead | null = null,
  status: eventStatusRead | null = null,
  threatActors: nodeThreatActorRead[] = [],
  threats: nodeThreatRead[] = [],
  type: eventTypeRead | null = null,
  vectors: eventVectorRead[] = [],
  nodeType = "",
  version = "testEventVersion1",
): eventRead => ({
  comments: comments,
  name: name,
  tags: tags,
  uuid: uuid,
  alertTime: alertTime,
  alertUuids: alertUuids,
  containTime: containTime,
  creationTime: creationTime,
  dispositionTime: dispositionTime,
  eventTime: eventTime,
  owner: owner,
  ownershipTime: ownershipTime,
  preventionTools: preventionTools,
  queue: queue,
  remediations: remediations,
  remediationTime: remediationTime,
  riskLevel: riskLevel,
  source: source,
  status: status,
  threatActors: threatActors,
  threats: threats,
  type: type,
  vectors: vectors,
  nodeType: nodeType,
  version: version,
});
