import { UUID } from "@/models/base";
import { NodeBase, NodeCreate, NodeRead, NodeUpdate } from "@/models/node";

interface AlertBase extends NodeBase {
  description?: string;
  eventTime: Date;
  instructions: string;
  name: string;
  owner?: string;
  queue: string;
  tool?: string;
  toolInstance?: string;
  type: string;
}
export interface AlertCreate extends NodeCreate, AlertBase {
  uuid: UUID;
}

// todo
// this may not actually be necessary
// format response object into this? idk
export interface AlertRead extends NodeRead, AlertBase {
  // todo: change to AnalysisRead
  analysis: Record<string, unknown>;
  // todo: change to AlertDispositionRead
  disposition?: string;
  dispositionTime?: Date;
  // todo: change to UserRead
  dispositionUser?: string;
  eventUuid?: UUID;
  insertTime: Date;
  // todo: change to UserRead
  owner?: string;
  // todo: change to AlertQueueRead
  queue: string;
  // todo: change to AlertToolRead
  tool?: string;
  // todo: change to AlertToolInstanceRead
  tool_instance?: string;
  // todo: change to AlertTypeRead
  type: string;
  uuid: UUID;
}

export interface AlertUpdate extends NodeUpdate, AlertBase {
  disposition?: string;
  eventUuid?: UUID;
  queue: string;
  type: string;
}
