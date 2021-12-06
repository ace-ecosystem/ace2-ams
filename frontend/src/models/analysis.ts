import { UUID } from "./base";
import { nodeCreate, nodeRead, nodeTreeCreate, nodeUpdate } from "./node";
import {
  analysisModuleTypeNodeTreeRead,
  analysisModuleTypeRead,
} from "./analysisModuleType";

export interface analysisCreate extends nodeCreate {
  alertUuid: UUID;
  analysisModuleType?: UUID;
  details?: Record<string, unknown>;
  errorMessage?: string;
  nodeTree: nodeTreeCreate;
  stackTrace?: string;
  summary?: string;
}

export interface analysisRead extends nodeRead {
  alertUuid: UUID;
  analysisModuleType: analysisModuleTypeRead;
  details: Record<string, unknown> | null;
  errorMessage: string | null;
  stackTrace: string | null;
  summary: string | null;
}

export interface analysisTreeRead {
  analysisModuleType: analysisModuleTypeNodeTreeRead;
  parentTreeUuid: UUID | null;
  treeUuid: UUID;
  uuid: UUID;
}

export interface analysisUpdate extends nodeUpdate {
  analysisModuleType?: UUID;
  details?: Record<string, unknown> | null;
  errorMessage?: string | null;
  stackTrace?: string | null;
  summary?: string | null;
}
